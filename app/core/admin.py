"""
Django admin customization
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# future proofing for translations
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""
    ordering = ['id']
    list_display = ['email', 'name']

    fieldsets = (
        # None is the title of the section
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        # last_login is automatically updated by Django
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ('last_login',)
    add_fieldsets = (
        (None, {
            # wide is a CSS class to make the input spacing wider
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),  # with tuples, the comma is required after the last element
    )


# register the User model with the custom UserAdmin
admin.site.register(models.User, UserAdmin)
# register the Recipe model with the default admin
admin.site.register(models.Recipe)
# register the Tag model with the default admin
admin.site.register(models.Tag)
# register the Ingredient model with the default admin
admin.site.register(models.Ingredient)
