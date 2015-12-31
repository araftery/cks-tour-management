from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _

from core.setting_validators import setting_validators


class Setting(models.Model):
    name = models.CharField(max_length=500)
    value = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, null=True, blank=True)
    time_set = models.DateTimeField()
    order_num = models.IntegerField()

    value_type_choices = ['int', 'float', 'string', 'bool', 'email', 'semester_or_never']
    value_type_choice_tuples = [(i, i) for i in value_type_choices]

    value_type = models.CharField(choices=value_type_choice_tuples, max_length=50)

    def __unicode__(self):
        return u'{}: {}'.format(self.name, self.value)

    def save(self, *args, **kwargs):
        # avoid ciruclar import
        from core.utils import now

        now_obj = now()
        self.time_set = now_obj

        if not self.pk:
            # object is new, just save it
            return super(Setting, self).save(*args, **kwargs)
        else:
            # don't save it, create a new object instead
            Setting.objects.create(name=self.name, value=self.value, description=self.description, order_num=self.order_num, value_type=self.value_type, time_set=now_obj)

    def clean(self):
        value = self.value
        try:
            validation = setting_validators[self.value_type](value)
            if validation['valid'] is True:
                value = validation['value']
            else:
                errors = []
                for error in validation['errors']:
                    errors.append(ValidationError(_(error), code='invalid'))
                raise ValidationError({'value': errors})
        except (IndexError, KeyError):
            raise ValidationError({'value': _('Invalid value.')}, code='invalid')
