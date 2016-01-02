from django.contrib import admin

from shifts.models import Shift

# Register your models here.


class ShiftAdmin(admin.ModelAdmin):
    list_display = ('source', 'time', 'person', 'length', 'notes', 'missed', 'late',)


admin.site.register(Shift, ShiftAdmin)
