from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import *

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_active', 'is_superuser')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields':('password', 'slug','avatar',)}),
        ('Personal Info', {'fields':('email',)}),
        ('Permissions',{'fields':('is_superuser', 'is_active')}),
    )
    
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name',]

@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ['user', 'name']