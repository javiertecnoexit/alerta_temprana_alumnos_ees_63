from django.urls import path

from . import views

app_name = "seguimiento"

urlpatterns = [
    path("alumnos/", views.buscar_alumnos, name="buscar_alumnos"),
    path(
        "alumnos/<int:alumno_id>/",
        views.ficha_alumno,
        name="ficha_alumno",
    ),
    path(
        "preceptor/alumnos/",
        views.lista_alumnos_preceptor,
        name="preceptor_alumnos",
    ),
    # Solicitudes de información
    path(
        "solicitar-info/",
        views.solicitar_info,
        name="solicitar_info",
    ),
    path(
        "solicitudes/",
        views.lista_solicitudes,
        name="lista_solicitudes",
    ),
    path(
        "solicitudes/<int:solicitud_id>/responder/",
        views.responder_solicitud,
        name="responder_solicitud",
    ),
    # Intervenciones
    path(
        "alumnos/<int:alumno_id>/intervencion/",
        views.registrar_intervencion,
        name="registrar_intervencion",
    ),
]
