from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from apps.alumnos.models import Alumno, AsignacionAlumnoCurso
from apps.ciclos_lectivos.models import CicloLectivo
from apps.estructura_escolar.models import Curso, Materia, Turno
from apps.observaciones.forms import ObservacionForm
from apps.observaciones.models import CatalogoObservacion, Observacion
from apps.usuarios.decorators import (
    directivo_o_preceptor,
    directivo_requerido,
    docente_requerido,
    preceptor_requerido,
)

from .forms import IntervencionForm, RespuestaSolicitudForm, SolicitudInfoForm
from .models import Intervencion, PreceptorTurno, SolicitudInfo


def turno_del_preceptor(user):
    """Devuelve el turno del preceptor, o None si no tiene asignado."""
    try:
        return user.preceptor_turno.turno
    except PreceptorTurno.DoesNotExist:
        return None


@directivo_requerido
def buscar_alumnos(request):
    """Buscador de alumnos con filtros opcionales para directivos."""
    termino = request.GET.get("q", "").strip()
    curso_id = request.GET.get("curso", "")
    turno_id = request.GET.get("turno", "")
    ciclo_id = request.GET.get("ciclo", "")

    alumnos = Alumno.objects.all().order_by("apellido", "nombre")

    if termino:
        alumnos = alumnos.filter(
            Q(apellido__icontains=termino)
            | Q(nombre__icontains=termino)
            | Q(dni__icontains=termino)
        )

    # Filtro por curso/turno/ciclo a través de asignaciones
    if curso_id or turno_id or ciclo_id:
        asignaciones_ids = AsignacionAlumnoCurso.objects.filter(activa=True)
        if curso_id:
            asignaciones_ids = asignaciones_ids.filter(curso_id=curso_id)
        if ciclo_id:
            asignaciones_ids = asignaciones_ids.filter(ciclo_lectivo_id=ciclo_id)
        if turno_id:
            asignaciones_ids = asignaciones_ids.filter(curso__turno_id=turno_id)
        alumnos = alumnos.filter(
            pk__in=asignaciones_ids.values_list("alumno_id", flat=True)
        ).distinct()

    return render(
        request,
        "seguimiento/buscar_alumnos.html",
        {
            "alumnos": alumnos,
            "termino": termino,
            "cursos": Curso.objects.select_related("turno", "ciclo_lectivo").all(),
            "turnos": Turno.objects.all(),
            "ciclos": CicloLectivo.objects.all(),
            "curso_id": curso_id,
            "turno_id": turno_id,
            "ciclo_id": ciclo_id,
        },
    )


def _preceptor_puede_ver_alumno(user, alumno):
    """Verifica si el preceptor tiene acceso al alumno (debe ser de su turno)."""
    turno = turno_del_preceptor(user)
    if turno is None:
        return False
    return AsignacionAlumnoCurso.objects.filter(
        alumno=alumno,
        curso__turno=turno,
        activa=True,
    ).exists()


@directivo_o_preceptor
def ficha_alumno(request, alumno_id):
    """Ficha integral del alumno: SOLO datos observados, sin diagnósticos."""
    alumno = get_object_or_404(Alumno, pk=alumno_id)

    # Si es preceptor, verificar que el alumno es de su turno
    if request.user.es_preceptor and not _preceptor_puede_ver_alumno(
        request.user, alumno
    ):
        raise PermissionDenied

    # Historial de asignaciones a cursos
    asignaciones = (
        AsignacionAlumnoCurso.objects.filter(alumno=alumno)
        .select_related("curso", "curso__turno", "ciclo_lectivo")
        .order_by("-ciclo_lectivo__anio", "-fecha_inicio")
    )

    # Filtros
    ciclo_id = request.GET.get("ciclo", "")
    materia_id = request.GET.get("materia", "")
    caracter = request.GET.get("caracter", "")

    observaciones = Observacion.objects.filter(
        alumno=alumno, anulada=False
    ).select_related("catalogo", "materia", "curso", "docente")

    if ciclo_id:
        observaciones = observaciones.filter(ciclo_lectivo_id=ciclo_id)
    if materia_id:
        observaciones = observaciones.filter(materia_id=materia_id)
    if caracter:
        observaciones = observaciones.filter(catalogo__caracter=caracter)

    # Conteo por caracter (datos observados, agrupados)
    conteo = (
        Observacion.objects.filter(alumno=alumno, anulada=False)
        .values("catalogo__caracter")
        .annotate(total=Count("id"))
        .order_by("catalogo__caracter")
    )
    conteo_por_caracter = {item["catalogo__caracter"]: item["total"] for item in conteo}

    # Agrupar observaciones por materia
    observaciones_por_materia = {}
    for obs in observaciones.order_by("-fecha_hora"):
        observaciones_por_materia.setdefault(obs.materia, []).append(obs)

    return render(
        request,
        "seguimiento/ficha_alumno.html",
        {
            "alumno": alumno,
            "asignaciones": asignaciones,
            "observaciones_por_materia": observaciones_por_materia,
            "conteo_por_caracter": conteo_por_caracter,
            "ciclos": CicloLectivo.objects.all(),
            "materias": Materia.objects.filter(
                observaciones__alumno=alumno,
                observaciones__anulada=False,
            ).distinct().order_by("nombre"),
            "ciclo_id": ciclo_id,
            "materia_id": materia_id,
            "caracter": caracter,
            "intervenciones": Intervencion.objects.filter(alumno=alumno)
            .select_related("responsable")
            .order_by("-fecha"),
        },
    )


@docente_requerido
@require_http_methods(["GET", "POST"])
def solicitar_info(request):
    """El docente solicita información global de un alumno al directivo."""
    if request.method == "POST":
        form = SolicitudInfoForm(request.POST, user=request.user)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.solicitante = request.user
            solicitud.save()
            messages.success(
                request,
                "Solicitud de información enviada al equipo directivo.",
            )
            return redirect("observaciones:lista_cursos")
    else:
        form = SolicitudInfoForm(user=request.user)

    return render(
        request,
        "seguimiento/solicitar_info.html",
        {"form": form},
    )


@directivo_requerido
def lista_solicitudes(request):
    """El directivo ve todas las solicitudes de información."""
    estado = request.GET.get("estado", "")
    solicitudes = SolicitudInfo.objects.select_related(
        "alumno", "solicitante", "respondido_por"
    )
    if estado:
        solicitudes = solicitudes.filter(estado=estado)

    return render(
        request,
        "seguimiento/lista_solicitudes.html",
        {
            "solicitudes": solicitudes,
            "estado": estado,
        },
    )


@directivo_requerido
@require_http_methods(["GET", "POST"])
def responder_solicitud(request, solicitud_id):
    """El directivo responde una solicitud de información."""
    solicitud = get_object_or_404(
        SolicitudInfo.objects.select_related("alumno", "solicitante"),
        pk=solicitud_id,
    )

    if request.method == "POST":
        form = RespuestaSolicitudForm(request.POST, instance=solicitud)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.respondido_por = request.user
            solicitud.fecha_respuesta = timezone.now()
            solicitud.save()
            messages.success(request, "Solicitud respondida correctamente.")
            return redirect("seguimiento:lista_solicitudes")
    else:
        form = RespuestaSolicitudForm(instance=solicitud)

    return render(
        request,
        "seguimiento/responder_solicitud.html",
        {"form": form, "solicitud": solicitud},
    )


@directivo_requerido
@require_http_methods(["GET", "POST"])
def registrar_intervencion(request, alumno_id):
    """El directivo registra una intervención de seguimiento."""
    alumno = get_object_or_404(Alumno, pk=alumno_id)

    if request.method == "POST":
        form = IntervencionForm(request.POST)
        if form.is_valid():
            intervencion = form.save(commit=False)
            intervencion.alumno = alumno
            intervencion.responsable = request.user
            intervencion.save()
            messages.success(request, "Intervención registrada.")
            return redirect("seguimiento:ficha_alumno", alumno_id=alumno.id)
    else:
        form = IntervencionForm()

    return render(
        request,
        "seguimiento/registrar_intervencion.html",
        {"form": form, "alumno": alumno},
    )


@preceptor_requerido
@login_required
def lista_alumnos_preceptor(request):
    """Muestra los alumnos del turno asignado al preceptor."""
    try:
        preceptor_turno = request.user.preceptor_turno
    except PreceptorTurno.DoesNotExist:
        # El preceptor no tiene turno asignado → no ve alumnos
        return render(
            request,
            "seguimiento/lista_alumnos_preceptor.html",
            {"turno": None, "alumnos": []},
        )

    turno = preceptor_turno.turno

    alumno_ids = AsignacionAlumnoCurso.objects.filter(
        curso__turno=turno, activa=True
    ).values_list("alumno_id", flat=True)

    alumnos = Alumno.objects.filter(pk__in=alumno_ids).order_by(
        "apellido", "nombre"
    )

    return render(
        request,
        "seguimiento/lista_alumnos_preceptor.html",
        {"turno": turno, "alumnos": alumnos},
    )


def _alumno_del_turno_preceptor(user, alumno_id):
    """Devuelve el alumno si pertenece al turno del preceptor, sino 403."""
    alumno = get_object_or_404(Alumno, pk=alumno_id)
    if not _preceptor_puede_ver_alumno(user, alumno):
        raise PermissionDenied
    return alumno


@preceptor_requerido
@require_http_methods(["GET", "POST"])
def registrar_observacion_preceptor(request, alumno_id):
    """El preceptor registra una observación preceptorial (sin materia)."""
    alumno = _alumno_del_turno_preceptor(request.user, alumno_id)
    turno = turno_del_preceptor(request.user)

    # Curso actual del alumno (primera asignación activa)
    asignacion_actual = (
        AsignacionAlumnoCurso.objects.filter(alumno=alumno, activa=True)
        .select_related("curso", "ciclo_lectivo")
        .first()
    )
    if asignacion_actual is None:
        messages.error(request, "El alumno no tiene un curso asignado.")
        return redirect("seguimiento:preceptor_alumnos")

    catalogo_agrupado = CatalogoObservacion.objects.filter(
        activo=True
    ).order_by("familia", "nombre")

    if request.method == "POST":
        form = ObservacionForm(request.POST)
        if form.is_valid():
            observacion = form.save(commit=False)
            observacion.alumno = alumno
            observacion.docente = request.user
            observacion.materia = None  # observación preceptorial
            observacion.curso = asignacion_actual.curso
            observacion.ciclo_lectivo = asignacion_actual.ciclo_lectivo
            observacion.turno = turno.nombre
            observacion.fecha_hora = timezone.now()
            observacion.dentro_horario = False
            observacion.save()
            messages.success(
                request,
                f"Observación registrada para {alumno}.",
            )
            return redirect("seguimiento:preceptor_alumnos")
    else:
        form = ObservacionForm()

    return render(
        request,
        "seguimiento/registrar_observacion_preceptor.html",
        {
            "alumno": alumno,
            "turno": turno,
            "form": form,
            "catalogo_agrupado": catalogo_agrupado,
        },
    )


@preceptor_requerido
@require_http_methods(["GET", "POST"])
def registrar_intervencion_preceptor(request, alumno_id):
    """El preceptor registra una intervención de seguimiento."""
    alumno = _alumno_del_turno_preceptor(request.user, alumno_id)

    if request.method == "POST":
        form = IntervencionForm(request.POST)
        if form.is_valid():
            intervencion = form.save(commit=False)
            intervencion.alumno = alumno
            intervencion.responsable = request.user
            intervencion.save()
            messages.success(request, "Intervención registrada.")
            return redirect("seguimiento:ficha_alumno", alumno_id=alumno.id)
    else:
        form = IntervencionForm()

    return render(
        request,
        "seguimiento/registrar_intervencion.html",
        {"form": form, "alumno": alumno},
    )
