from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Submit, Div, Layout

from profiles.forms import ActiveMemberField
from shifts.models import Shift


class ShiftForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ShiftForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'control-label'
        self.helper.html5_required = True
        self.fields['person'] = ActiveMemberField()
        self.fields['person'].required = False
        self.fields['source'] = forms.ChoiceField(choices=Shift.source_choices)
        self.fields['time'] = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'datepicker'}, format="%m/%d/%Y %I:%M %p"), input_formats=["%m/%d/%Y %I:%M %p"])

        self.helper.form_action = './'

        self.helper.layout = Layout(
            Field('time'),
            Field('notes', placeholder="These notes will be sent to the member in the shift reminder email. Include location or other special instructions here."),
            Field('person', css_class="selectize"),
            Field('source'),
            Field('missed'),
            Field('late'),
            Field('counts_for_requirements'),
            Field('length'),

            Div(
                Submit('submit', 'Submit', css_class="btn btn-danger"),
            ),
        )

    class Meta:
        model = Shift
        fields = ('time', 'notes', 'person', 'source', 'missed', 'late', 'counts_for_requirements', 'length',)
