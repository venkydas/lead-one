# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'role', 'date_joined', 'is_active')
    list_filter = ('role', 'is_active', 'date_joined')
    search_fields = ('email', 'name')
    ordering = ('email',)
    readonly_fields = ('date_joined',)  # <-- This makes it view-only!
    fieldsets = (
        (None, {'fields': ('email', 'password', 'role')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),  # date_joined is not here
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'role', 'password1', 'password2'),
        }),
    )
