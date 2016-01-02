from django.contrib import admin

from tours.models import Tour, CanceledDay, DefaultTour, InitializedMonth, OpenMonth

# Register your models here.


class TourAdmin(admin.ModelAdmin):
    list_display = ('source', 'time', 'guide', 'length', 'notes', 'missed', 'late', 'default_tour',)


class DefaultTourAdmin(admin.ModelAdmin):
    list_display = ('source', 'hour', 'minute', 'day_num', 'length', 'notes')


class OpenMonthAdmin(admin.ModelAdmin):
    list_display = ('month', 'year', 'closes',)


admin.site.register(Tour, TourAdmin)
admin.site.register(CanceledDay)
admin.site.register(DefaultTour, DefaultTourAdmin)
admin.site.register(InitializedMonth)
admin.site.register(OpenMonth, OpenMonthAdmin)
