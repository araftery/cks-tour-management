from django.contrib import admin

from profiles.models import Person
from profiles.forms import PersonForm


class PersonAdmin(admin.ModelAdmin):
    form = PersonForm
    list_display = ('first_name', 'last_name', 'email', 'harvard_email', 'user', 'phone', 'year', 'member_since_year', 'position', 'site_admin', 'house', 'notes',)
    ordering = ('-year', 'last_name', 'first_name',)

admin.site.register(Person, PersonAdmin)
