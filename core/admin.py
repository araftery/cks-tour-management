from django.contrib import admin

from core.models import Setting


class SettingAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'description', 'order_num')
    ordering = ('order_num', '-time_set',)

admin.site.register(Setting, SettingAdmin)
