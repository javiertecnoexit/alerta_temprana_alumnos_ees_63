from django.urls import path

from . import views

app_name = "observaciones"

urlpatterns = [
    path("cursos/", views.lista_cursos, name="lista_cursos"),
    path(
        "cursos/<int:asignacion_id>/alumnos/",
        views.lista_alumnos,
        name="lista_alumnos",
    ),
    path(
        "cursos/<int:asignacion_id>/alumnos/<int:alumno_id>/registrar/",
        views.registrar_observacion,
        name="registrar",
    ),
    path("historial/", views.historial, name="historial"),
]