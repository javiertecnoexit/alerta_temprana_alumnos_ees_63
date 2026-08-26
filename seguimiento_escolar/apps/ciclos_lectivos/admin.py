from django.contrib import admin

from .models import CicloLectivo


@admin.register(CicloLectivo)
class CicloLectivoAdmin(admin.ModelAdmin):
    list_display = ("anio", "estado", "fecha_inicio", "fecha_fin", "activo")
    list_filter = ("estado", "activo")
    search_fields = ("anio",)
    readonly_fields = ("creado_en", "actualizado_en")