from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Submit, Div, Layout

from profiles.forms import ActiveMemberField
from tours.models import Tour
from tours import utils as tours_utils


class TourForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TourForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        # self.helper.form_id = 'article_form'
        # self.helper.form_name = 'article_form'
        self.helper.label_class = 'control-label'
        self.helper.html5_required = True
        self.fields['guide'] = ActiveMemberField()
        self.fields['source'] = forms.ChoiceField(choices=Tour.source_choices)
        self.fields['time'] = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'datepicker'}, format="%m/%d/%Y %I:%M %p"), input_formats=["%m/%d/%Y %I:%M %p"])

        self.helper.layout = Layout(
            Field('time'),
            Field('notes', placeholder="These notes will be sent to the tour guide in the tour reminder email. Include location or other special instructions here."),
            Field('guide', css_class="selectize"),
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
        model = Tour
        fields = ('time', 'notes', 'guide', 'source', 'missed', 'late', 'counts_for_requirements', 'length',)


class MonthEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MonthEditForm, self).__init__(*args, **kwargs)
        self.fields['guide'] = ActiveMemberField()

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('guide', css_class='selectize'),
        )

    class Meta:
        model = Tour
        fields = ('guide',)


class ChooseMonthForm(forms.Form):
    month = forms.ChoiceField(choices=tours_utils.get_initialize_month_choices())

    def __init__(self, *args, **kwargs):
        super(ChooseMonthForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'form-horizontal'
        #self.helper.form_id = 'article_form'
        #self.helper.form_name = 'article_form'
        self.helper.label_class = 'control-label'
        self.helper.html5_required = True

        self.helper.layout = Layout(
            Field('month', css_class='js-month'),
            Div(
                Submit('submit', 'Submit', css_class="btn btn-danger"),
            ),
    )
