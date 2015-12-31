from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from core.models import Setting
from core.setting_validators import setting_validators


class SettingForm(forms.ModelForm):

    def clean_value(self):
        value = self.cleaned_data.get('value')
        try:
            validation = setting_validators[self.instance.type](value)
            if validation['valid'] is True:
                value = validation['value']
            else:
                errors = []
                for error in validation['errors']:
                    errors.append(ValidationError(_(error), code='invalid'))
                raise ValidationError(errors)
        except (IndexError, KeyError):
            raise ValidationError(_('Invalid value.'), code='invalid')

        return value

    class Meta:
        model = Setting
        fields = ('value',)


SettingFormSet = forms.modelformset_factory(Setting, fields=('value',), extra=0)
