from django.contrib import admin

from .models import AsignacionDocente, Curso, Horario, Materia, Turno


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activo")
    list_filter = ("activo",)


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("anio", "division", "turno", "ciclo_lectivo", "activo")
    list_filter = ("turno", "ciclo_lectivo", "activo")
    search_fields = ("anio", "division")
    list_select_related = ("turno", "ciclo_lectivo")


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activa")
    search_fields = ("nombre",)
    list_filter = ("activa",)


@admin.register(AsignacionDocente)
class AsignacionDocenteAdmin(admin.ModelAdmin):
    list_display = (
        "docente",
        "materia",
        "curso",
        "tipo",
        "fecha_inicio",
        "fecha_fin",
        "activa",
    )
    list_filter = ("tipo", "activa", "curso")
    search_fields = ("docente__username", "materia__nombre")
    # autocomplete_fields en 'docente' requiere search_fields en UsuarioAdmin
    # (apps/usuarios no se modifica en esta tarea), por eso solo materia y curso.
    autocomplete_fields = ("materia", "curso")


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ("asignacion_docente", "dia_semana", "hora_inicio", "hora_fin")
    list_filter = ("dia_semana",)
