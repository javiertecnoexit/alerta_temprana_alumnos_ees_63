from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "rol", "is_staff")
    list_filter = ("rol", "is_staff", "is_superuser", "is_active", "groups")

    fieldsets = UserAdmin.fieldsets + (
        ("Rol institucional", {"fields": ("rol",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Rol institucional", {"fields": ("rol",)}),
    )