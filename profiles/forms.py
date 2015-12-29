from django import forms
from django.forms import ModelChoiceField

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

        self.fields['notes'] = forms.Textarea()
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

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'email', 'harvard_email', 'phone', 'year', 'member_since_year', 'position', 'site_admin', 'house', 'notes',)


class SpecialRequirementsForm(forms.ModelForm):
    def __init__(self, year, semester, person, *args, **kwargs):
        super(SpecialRequirementsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'control-label'
        self.helper.html5_required = True

        self.fields['tours_required'].placeholder = 'Leave empty for default'
        self.fields['shifts_required'].placeholder = 'Leave empty for default'

        self.fields['year'].value = year
        self.fields['semester'].value = semester
        self.fields['person'].value = person

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
