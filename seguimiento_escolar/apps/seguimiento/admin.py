from django.contrib import admin

from .models import Intervencion, PreceptorTurno, SolicitudInfo


@admin.register(PreceptorTurno)
class PreceptorTurnoAdmin(admin.ModelAdmin):
    list_display = ("preceptor", "turno")
    list_filter = ("turno",)
    search_fields = ("preceptor__username", "preceptor__first_name", "preceptor__last_name")


@admin.register(SolicitudInfo)
class SolicitudInfoAdmin(admin.ModelAdmin):
    list_display = (
        "alumno",
        "solicitante",
        "estado",
        "fecha_solicitud",
        "fecha_respuesta",
    )
    list_filter = ("estado",)
    search_fields = ("alumno__apellido", "alumno__nombre", "motivo")


@admin.register(Intervencion)
class IntervencionAdmin(admin.ModelAdmin):
    list_display = ("alumno", "responsable", "tipo", "fecha")
    list_filter = ("tipo",)
    search_fields = ("alumno__apellido", "alumno__nombre", "descripcion")
