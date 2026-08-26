from django.contrib import admin

from .models import Alumno, AsignacionAlumnoCurso


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ("apellido", "nombre", "dni", "estado")
    list_filter = ("estado",)
    search_fields = ("apellido", "nombre", "dni")


@admin.register(AsignacionAlumnoCurso)
class AsignacionAlumnoCursoAdmin(admin.ModelAdmin):
    list_display = ("alumno", "curso", "ciclo_lectivo", "condicion", "fecha_inicio", "activa")
    list_filter = ("condicion", "activa", "ciclo_lectivo")
    search_fields = ("alumno__apellido", "alumno__nombre")