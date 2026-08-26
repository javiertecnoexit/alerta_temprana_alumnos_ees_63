from django.contrib import admin

from .models import CatalogoObservacion, Observacion


@admin.register(CatalogoObservacion)
class CatalogoObservacionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "familia", "caracter", "activo", "version")
    list_filter = ("familia", "caracter", "activo")
    search_fields = ("nombre",)
    readonly_fields = ("creado_en", "version")


@admin.register(Observacion)
class ObservacionAdmin(admin.ModelAdmin):
    list_display = (
        "alumno",
        "catalogo",
        "docente",
        "materia",
        "curso",
        "fecha_hora",
        "anulada",
    )
    list_filter = ("anulada", "catalogo__familia", "curso")
    search_fields = ("alumno__apellido", "alumno__nombre")
    readonly_fields = ("creado_en",)