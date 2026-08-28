from django.urls import path

from . import views

app_name = "administracion"

urlpatterns = [
    path("", views.index, name="index"),

    # Alumnos
    path("alumnos/", views.alumnos_lista, name="alumnos_lista"),
    path("alumnos/nuevo/", views.alumno_crear, name="alumno_crear"),
    path("alumnos/confirmar/", views.alumno_confirmar, name="alumno_confirmar"),
    path("alumnos/<int:alumno_id>/editar/", views.alumno_editar, name="alumno_editar"),
    path("alumnos/confirmar-editar/", views.alumno_confirmar_editar, name="alumno_confirmar_editar"),
    path("alumnos/<int:alumno_id>/baja/", views.alumno_baja, name="alumno_baja"),

    # Docentes
    path("docentes/", views.docentes_lista, name="docentes_lista"),
    path("docentes/nuevo/", views.docente_crear, name="docente_crear"),
    path("docentes/confirmar/", views.docente_confirmar, name="docente_confirmar"),
    path("docentes/<int:docente_id>/editar/", views.docente_editar, name="docente_editar"),
    path("docentes/confirmar-editar/", views.docente_confirmar_editar, name="docente_confirmar_editar"),
    path("docentes/<int:docente_id>/baja/", views.docente_baja, name="docente_baja"),

    # Materias
    path("materias/", views.materias_lista, name="materias_lista"),
    path("materias/nueva/", views.materia_crear, name="materia_crear"),
    path("materias/confirmar/", views.materia_confirmar, name="materia_confirmar"),
    path("materias/<int:materia_id>/editar/", views.materia_editar, name="materia_editar"),
    path("materias/confirmar-editar/", views.materia_confirmar_editar, name="materia_confirmar_editar"),
    path("materias/<int:materia_id>/baja/", views.materia_baja, name="materia_baja"),

    # Turnos
    path("turnos/", views.turnos_lista, name="turnos_lista"),
    path("turnos/nuevo/", views.turno_crear, name="turno_crear"),
    path("turnos/confirmar/", views.turno_confirmar, name="turno_confirmar"),
    path("turnos/<int:turno_id>/editar/", views.turno_editar, name="turno_editar"),
    path("turnos/confirmar-editar/", views.turno_confirmar_editar, name="turno_confirmar_editar"),
    path("turnos/<int:turno_id>/baja/", views.turno_baja, name="turno_baja"),

    # Cursos
    path("cursos/", views.cursos_lista, name="cursos_lista"),
    path("cursos/nuevo/", views.curso_crear, name="curso_crear"),
    path("cursos/confirmar/", views.curso_confirmar, name="curso_confirmar"),
    path("cursos/<int:curso_id>/editar/", views.curso_editar, name="curso_editar"),
    path("cursos/confirmar-editar/", views.curso_confirmar_editar, name="curso_confirmar_editar"),
    path("cursos/<int:curso_id>/baja/", views.curso_baja, name="curso_baja"),

    # Ciclos lectivos
    path("ciclos/", views.ciclos_lista, name="ciclos_lista"),
    path("ciclos/nuevo/", views.ciclo_crear, name="ciclo_crear"),
    path("ciclos/confirmar/", views.ciclo_confirmar, name="ciclo_confirmar"),
    path("ciclos/<int:ciclo_id>/editar/", views.ciclo_editar, name="ciclo_editar"),
    path("ciclos/confirmar-editar/", views.ciclo_confirmar_editar, name="ciclo_confirmar_editar"),

    # Asignaciones docentes
    path("asignaciones/", views.asignaciones_lista, name="asignaciones_lista"),
    path("asignaciones/nueva/", views.asignacion_crear, name="asignacion_crear"),
    path("asignaciones/confirmar/", views.asignacion_confirmar, name="asignacion_confirmar"),
    path("asignaciones/<int:asignacion_id>/editar/", views.asignacion_editar, name="asignacion_editar"),
    path("asignaciones/confirmar-editar/", views.asignacion_confirmar_editar, name="asignacion_confirmar_editar"),
    path("asignaciones/<int:asignacion_id>/baja/", views.asignacion_baja, name="asignacion_baja"),

    # Horarios
    path("horarios/", views.horarios_lista, name="horarios_lista"),
    path("horarios/nuevo/", views.horario_crear, name="horario_crear"),
    path("horarios/confirmar/", views.horario_confirmar, name="horario_confirmar"),
    path("horarios/<int:horario_id>/editar/", views.horario_editar, name="horario_editar"),
    path("horarios/confirmar-editar/", views.horario_confirmar_editar, name="horario_confirmar_editar"),
    path("horarios/<int:horario_id>/eliminar/", views.horario_eliminar, name="horario_eliminar"),

    # Asignaciones alumno-curso
    path(
        "asignaciones-alumnos/",
        views.asignaciones_alumnos_lista,
        name="asignaciones_alumnos_lista",
    ),
    path(
        "asignaciones-alumnos/nueva/",
        views.asignacion_alumno_crear,
        name="asignacion_alumno_crear",
    ),
    path(
        "asignaciones-alumnos/confirmar/",
        views.asignacion_alumno_confirmar,
        name="asignacion_alumno_confirmar",
    ),
    path(
        "asignaciones-alumnos/<int:asignacion_id>/editar/",
        views.asignacion_alumno_editar,
        name="asignacion_alumno_editar",
    ),
    path(
        "asignaciones-alumnos/confirmar-editar/",
        views.asignacion_alumno_confirmar_editar,
        name="asignacion_alumno_confirmar_editar",
    ),
    path(
        "asignaciones-alumnos/<int:asignacion_id>/baja/",
        views.asignacion_alumno_baja,
        name="asignacion_alumno_baja",
    ),
]
