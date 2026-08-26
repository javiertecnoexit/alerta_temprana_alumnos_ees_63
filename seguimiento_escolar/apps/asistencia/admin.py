from django.contrib import admin

from .models import RegistroAsistencia


@admin.register(RegistroAsistencia)
class RegistroAsistenciaAdmin(admin.ModelAdmin):
    list_display = ("alumno", "curso", "materia", "fecha", "estado", "docente")
    list_filter = ("estado", "fecha", "curso")
    search_fields = ("alumno__apellido", "alumno__nombre")