from django.db import models


class Setting(models.Model):
    name = models.CharField(max_length=500)
    value = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, null=True, blank=True)
    time_set = models.DateTimeField()
    order_num = models.IntegerField()

    value_type_choices = ['int', 'float', 'string', 'bool', 'email', 'semester_or_none']
    value_type_choice_tuples = [(i, i) for i in value_type_choices]

    value_type = models.CharField(choices=value_type_choice_tuples, max_length=50)

    def __unicode__(self):
        return u'{}: {}'.format(self.name, self.value)
