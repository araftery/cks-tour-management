from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings
from django.db.models import Q
from django.forms import ModelChoiceField
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Submit, Div, Layout

from profiles.models import Person, OverrideRequirement


class ActiveMemberField(ModelChoiceField):
    def __init__(self, *args, **kwargs):
        super(ActiveMemberField, self).__init__(queryset=Person.objects.current_members().active(), empty_label='Unclaimed', *args, **kwargs)

    def label_from_instance(self, obj):
        return obj.full_name


class PersonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'control-label'
        self.helper.html5_required = True

        self.fields['notes'].widget = forms.Textarea()
        self.fields['email'].label = 'Primary email'
        self.fields['phone'].label = 'Phone number'
        self.fields['member_since_year'].label = 'Member of CKS since year'
        self.fields['year'].label = 'Graduation year'

        self.helper.layout = Layout(
            Field('first_name'),
            Field('last_name'),
            Field('email'),
            Field('harvard_email'),
            Field('phone'),
            Field('year'),
            Field('member_since_year'),
            Field('position'),
            Field('site_admin'),
            Field('house'),
            Field('notes'),

            Div(
                Submit('submit', 'Submit', css_class="btn btn-danger"),
            ),
        )

    def clean_harvard_email(self):
        harvard_email = self.cleaned_data.get('harvard_email')

        if harvard_email is None:
            raise ValidationError(_('A Harvard email is required.'), code='invalid')

        harvard_email = harvard_email.strip().lower()

        if harvard_email == '':
            raise ValidationError(_('A Harvard email is required.'), code='invalid')

        # make sure it's a valid email address
        validate_email(harvard_email)

        # make sure no existing users have this address
        qs = Person.objects.filter(Q(email=harvard_email) | Q(harvard_email=harvard_email))
        if self.instance.pk is not None:
            qs = qs.exclude(pk=self.instance.pk)

        if qs:
            raise ValidationError(_('A member with this email address already exists.'), code='invalid')

        # make sure it's a valid harvard address
        try:
            if harvard_email.split('@', 1)[1] not in settings.VALID_HARVARD_DOMAINS:
                raise ValidationError(('Please enter a valid @college email address.'), code='invalid')
        except IndexError:
            raise ValidationError(('Please enter a valid @college email address.'), code='invalid')

        return harvard_email

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'email', 'harvard_email', 'phone', 'year', 'member_since_year', 'position', 'site_admin', 'house', 'notes',)


class SpecialRequirementsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SpecialRequirementsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'control-label'
        self.helper.html5_required = True

        self.fields['tours_required'].placeholder = 'Leave empty for default'
        self.fields['shifts_required'].placeholder = 'Leave empty for default'

        self.helper.layout = Layout(
            Field('tours_required'),
            Field('shifts_required'),
            Field('year', type='hidden'),
            Field('semester', type='hidden'),
            Field('person', type='hidden'),

            Div(
                Submit('submit', 'Submit', css_class="btn btn-info"),
            ),
        )

    class Meta:
        model = OverrideRequirement
        fields = ('year', 'semester', 'person', 'tours_required', 'shifts_required')
