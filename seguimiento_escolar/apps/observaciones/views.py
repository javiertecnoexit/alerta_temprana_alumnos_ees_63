from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from apps.alumnos.models import Alumno, AsignacionAlumnoCurso
from apps.estructura_escolar.models import AsignacionDocente
from apps.usuarios.decorators import docente_requerido

from .forms import ObservacionForm
from .models import CatalogoObservacion, Observacion
from .services import es_dentro_de_horario


def _asignacion_del_docente(asignacion_id, user):
    """Devuelve la asignación si pertenece al docente, sino PermissionDenied."""
    asignacion = get_object_or_404(
        AsignacionDocente,
        pk=asignacion_id,
        docente=user,
        activa=True,
    )
    return asignacion


@docente_requerido
def lista_cursos(request):
    """Muestra las asignaciones docentes vigentes del usuario logueado."""
    hoy = timezone.localdate()
    asignaciones = (
        AsignacionDocente.objects.filter(docente=request.user, activa=True)
        .exclude(fecha_fin__lt=hoy)
        .select_related("curso", "materia", "curso__ciclo_lectivo", "curso__turno")
    )
    return render(
        request,
        "observaciones/lista_cursos.html",
        {"asignaciones": asignaciones},
    )


@docente_requerido
def lista_alumnos(request, asignacion_id):
    """Muestra los alumnos del curso de la asignación del docente."""
    asignacion = _asignacion_del_docente(asignacion_id, request.user)

    alumnos_ids = AsignacionAlumnoCurso.objects.filter(
        curso=asignacion.curso,
        ciclo_lectivo=asignacion.curso.ciclo_lectivo,
        activa=True,
    ).values_list("alumno_id", flat=True)

    alumnos = Alumno.objects.filter(pk__in=alumnos_ids).order_by(
        "apellido", "nombre"
    )

    return render(
        request,
        "observaciones/lista_alumnos.html",
        {"asignacion": asignacion, "alumnos": alumnos},
    )


@docente_requerido
@require_http_methods(["GET", "POST"])
def registrar_observacion(request, asignacion_id, alumno_id):
    """Registra una observación rápida (inmutable)."""
    asignacion = _asignacion_del_docente(asignacion_id, request.user)

    # Verificar que el alumno pertenece al curso de la asignación en este ciclo
    alumno = get_object_or_404(
        AsignacionAlumnoCurso,
        alumno_id=alumno_id,
        curso=asignacion.curso,
        ciclo_lectivo=asignacion.curso.ciclo_lectivo,
        activa=True,
    ).alumno

    catalogo_agrupado = CatalogoObservacion.objects.filter(
        activo=True
    ).order_by("familia", "nombre")

    if request.method == "POST":
        form = ObservacionForm(request.POST)
        if form.is_valid():
            observacion = form.save(commit=False)
            observacion.alumno = alumno
            observacion.docente = request.user
            observacion.materia = asignacion.materia
            observacion.curso = asignacion.curso
            observacion.ciclo_lectivo = asignacion.curso.ciclo_lectivo
            observacion.turno = asignacion.curso.turno.nombre
            observacion.fecha_hora = timezone.now()
            observacion.dentro_horario = es_dentro_de_horario(
                asignacion, observacion.fecha_hora
            )
            observacion.save()
            messages.success(
                request,
                f"Observación registrada para {alumno}.",
            )
            return redirect(
                "observaciones:registrar",
                asignacion_id=asignacion_id,
                alumno_id=alumno_id,
            )
    else:
        form = ObservacionForm()

    return render(
        request,
        "observaciones/registrar.html",
        {
            "asignacion": asignacion,
            "alumno": alumno,
            "form": form,
            "catalogo_agrupado": catalogo_agrupado,
        },
    )


@docente_requerido
def historial(request):
    """Muestra SOLO las observaciones del docente logueado."""
    observaciones = (
        Observacion.objects.filter(docente=request.user)
        .select_related(
            "alumno", "catalogo", "materia", "curso", "curso__ciclo_lectivo"
        )
        .order_by("-fecha_hora")
    )
    return render(
        request,
        "observaciones/historial.html",
        {"observaciones": observaciones},
    )