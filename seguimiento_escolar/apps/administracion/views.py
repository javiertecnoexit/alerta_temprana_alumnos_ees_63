from datetime import date, datetime, time

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from apps.alumnos.models import Alumno, AsignacionAlumnoCurso
from apps.auditoria.models import AuditLog
from apps.ciclos_lectivos.models import CicloLectivo
from apps.estructura_escolar.models import (
    AsignacionDocente,
    Curso,
    Horario,
    Materia,
    Turno,
)
from apps.usuarios.decorators import directivo_o_admin
from apps.usuarios.models import Usuario

from .forms import (
    AlumnoForm,
    AsignacionAlumnoCursoForm,
    AsignacionDocenteForm,
    CicloLectivoForm,
    CursoForm,
    DocenteForm,
    HorarioForm,
    MateriaForm,
    TurnoForm,
)
from .services import registrar_auditoria


@directivo_o_admin
def index(request):
    """Panel índice de gestión de datos (directivo y admin)."""
    return render(request, "administracion/index.html")


def _serializar_datos(datos):
    """
    Convierte los valores de cleaned_data para poder guardarlos en sesión
    (la sesión usa JSON: los objetos date/datetime se pasan a ISO string
    y las instancias de modelos a su pk).
    """
    resultado = {}
    for clave, valor in datos.items():
        if isinstance(valor, (date, datetime, time)):
            resultado[clave] = valor.isoformat()
        elif hasattr(valor, "pk"):
            resultado[clave] = valor.pk
        else:
            resultado[clave] = valor
    return resultado


# ---------------------------------------------------------------------------
# Alumnos
# ---------------------------------------------------------------------------
@directivo_o_admin
def alumnos_lista(request):
    """Listado de alumnos."""
    alumnos = Alumno.objects.all()
    return render(request, "administracion/alumnos_lista.html", {"alumnos": alumnos})


@directivo_o_admin
def alumno_crear(request):
    """Paso 1: formulario de alta de alumno (guarda en sesión)."""
    if request.method == "POST":
        form = AlumnoForm(request.POST)
        if form.is_valid():
            request.session["alumno_crear"] = _serializar_datos(form.cleaned_data)
            return redirect("administracion:alumno_confirmar")
    else:
        form = AlumnoForm()
    return render(request, "administracion/alumno_form.html", {
        "form": form,
        "titulo": "Nuevo alumno",
        "accion_url": reverse("administracion:alumno_crear"),
    })


@directivo_o_admin
def alumno_confirmar(request):
    """Paso 2: muestra resumen y confirma la creación del alumno."""
    datos = request.session.get("alumno_crear")
    if not datos:
        return redirect("administracion:alumno_crear")

    if request.method == "POST":
        form = AlumnoForm(datos)
        if form.is_valid():
            alumno = form.save()
            registrar_auditoria(
                request.user, AuditLog.Accion.CREAR, "Alumno", alumno.id,
                {"nombre": alumno.nombre, "apellido": alumno.apellido,
                 "dni": alumno.dni},
                request,
            )
            # Asignación opcional de curso al crear el alumno
            curso = form.cleaned_data.get("curso")
            ciclo_lectivo = form.cleaned_data.get("ciclo_lectivo")
            if curso and ciclo_lectivo:
                asignacion = AsignacionAlumnoCurso.objects.create(
                    alumno=alumno,
                    curso=curso,
                    ciclo_lectivo=ciclo_lectivo,
                    fecha_inicio=timezone.now().date(),
                    condicion=AsignacionAlumnoCurso.Condicion.REGULAR,
                    activa=True,
                )
                registrar_auditoria(
                    request.user, AuditLog.Accion.CREAR,
                    "AsignacionAlumnoCurso", asignacion.id,
                    {"asignacion": str(asignacion)},
                    request,
                )
            del request.session["alumno_crear"]
            messages.success(request, f"Alumno {alumno} creado correctamente.")
            return redirect("administracion:alumnos_lista")
        # Si el form no es válido (p. ej. dato inconsistente), vuelve a crear
        del request.session["alumno_crear"]
        return redirect("administracion:alumno_crear")

    return render(request, "administracion/alumno_confirmar.html", {
        "datos": datos,
        "titulo": "Confirmar alta de alumno",
        "cancelar_url": reverse("administracion:alumno_crear"),
        "volver_url": reverse("administracion:alumnos_lista"),
    })


@directivo_o_admin
def alumno_editar(request, alumno_id):
    """Paso 1: formulario de edición de alumno (guarda en sesión)."""
    alumno = get_object_or_404(Alumno, pk=alumno_id)
    if request.method == "POST":
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            request.session["alumno_editar"] = {
                "id": alumno.id,
                "datos": _serializar_datos(form.cleaned_data),
            }
            return redirect("administracion:alumno_confirmar_editar")
    else:
        form = AlumnoForm(instance=alumno)
    return render(request, "administracion/alumno_form.html", {
        "form": form,
        "titulo": f"Editar alumno: {alumno}",
        "accion_url": reverse("administracion:alumno_editar", args=[alumno.id]),
        "volver_url": reverse("administracion:alumnos_lista"),
    })


@directivo_o_admin
def alumno_confirmar_editar(request):
    """Paso 2: confirma la edición del alumno."""
    sesion = request.session.get("alumno_editar")
    if not sesion:
        return redirect("administracion:alumnos_lista")

    alumno = get_object_or_404(Alumno, pk=sesion["id"])
    if request.method == "POST":
        form = AlumnoForm(sesion["datos"], instance=alumno)
        if form.is_valid():
            form.save()
            registrar_auditoria(
                request.user, AuditLog.Accion.MODIFICAR, "Alumno", alumno.id,
                {"campos": list(sesion["datos"].keys())},
                request,
            )
            del request.session["alumno_editar"]
            messages.success(request, f"Alumno {alumno} modificado correctamente.")
            return redirect("administracion:alumnos_lista")
        del request.session["alumno_editar"]
        return redirect("administracion:alumno_editar", alumno_id=alumno.id)

    datos = {"id": alumno.id, **sesion["datos"]}
    return render(request, "administracion/alumno_confirmar.html", {
        "datos": datos,
        "titulo": "Confirmar modificación de alumno",
        "cancelar_url": reverse("administracion:alumno_editar", args=[alumno.id]),
        "volver_url": reverse("administracion:alumnos_lista"),
    })


@directivo_o_admin
def alumno_baja(request, alumno_id):
    """Da de baja (estado inactivo) a un alumno con confirmación."""
    alumno = get_object_or_404(Alumno, pk=alumno_id)
    if request.method == "POST":
        alumno.estado = Alumno.Estado.INACTIVO
        alumno.save()
        registrar_auditoria(
            request.user, AuditLog.Accion.MODIFICAR, "Alumno", alumno.id,
            {"estado": "inactivo"},
            request,
        )
        messages.success(request, f"Alumno {alumno} dado de baja.")
        return redirect("administracion:alumnos_lista")
    return render(request, "administracion/alumno_confirmar.html", {
        "datos": {
            "id": alumno.id, "apellido": alumno.apellido,
            "nombre": alumno.nombre, "dni": alumno.dni,
        },
        "titulo": "Confirmar baja de alumno",
        "es_baja": True,
        "cancelar_url": reverse("administracion:alumnos_lista"),
        "volver_url": reverse("administracion:alumnos_lista"),
    })


# ---------------------------------------------------------------------------
# Docentes
# ---------------------------------------------------------------------------
@directivo_o_admin
def docentes_lista(request):
    """Listado de usuarios con rol docente."""
    docentes = Usuario.objects.filter(rol=Usuario.Rol.DOCENTE)
    return render(request, "administracion/docentes_lista.html", {"docentes": docentes})


@directivo_o_admin
def docente_crear(request):
    """Paso 1: formulario de alta de docente (guarda en sesión)."""
    if request.method == "POST":
        form = DocenteForm(request.POST)
        if form.is_valid():
            request.session["docente_crear"] = _serializar_datos(form.cleaned_data)
            return redirect("administracion:docente_confirmar")
    else:
        form = DocenteForm()
    return render(request, "administracion/docente_form.html", {
        "form": form,
        "titulo": "Nuevo docente",
        "accion_url": reverse("administracion:docente_crear"),
    })


@directivo_o_admin
def docente_confirmar(request):
    """Paso 2: muestra resumen y confirma la creación del docente."""
    datos = request.session.get("docente_crear")
    if not datos:
        return redirect("administracion:docente_crear")

    if request.method == "POST":
        form = DocenteForm(datos)
        if form.is_valid():
            docente = form.save()
            registrar_auditoria(
                request.user, AuditLog.Accion.CREAR, "Usuario", docente.id,
                {"username": docente.username, "rol": docente.rol},
                request,
            )
            del request.session["docente_crear"]
            messages.success(request, f"Docente {docente} creado correctamente.")
            return redirect("administracion:docentes_lista")
        del request.session["docente_crear"]
        return redirect("administracion:docente_crear")

    return render(request, "administracion/docente_confirmar.html", {
        "datos": datos,
        "titulo": "Confirmar alta de docente",
        "cancelar_url": reverse("administracion:docente_crear"),
        "volver_url": reverse("administracion:docentes_lista"),
    })


@directivo_o_admin
def docente_editar(request, docente_id):
    """Paso 1: formulario de edición de docente (guarda en sesión)."""
    docente = get_object_or_404(Usuario, pk=docente_id, rol=Usuario.Rol.DOCENTE)
    if request.method == "POST":
        form = DocenteForm(request.POST, instance=docente)
        if form.is_valid():
            request.session["docente_editar"] = {
                "id": docente.id,
                "datos": _serializar_datos(form.cleaned_data),
            }
            return redirect("administracion:docente_confirmar_editar")
    else:
        form = DocenteForm(instance=docente)
    return render(request, "administracion/docente_form.html", {
        "form": form,
        "titulo": f"Editar docente: {docente}",
        "accion_url": reverse("administracion:docente_editar", args=[docente.id]),
        "volver_url": reverse("administracion:docentes_lista"),
    })


@directivo_o_admin
def docente_confirmar_editar(request):
    """Paso 2: confirma la edición del docente."""
    sesion = request.session.get("docente_editar")
    if not sesion:
        return redirect("administracion:docentes_lista")

    docente = get_object_or_404(Usuario, pk=sesion["id"], rol=Usuario.Rol.DOCENTE)
    if request.method == "POST":
        form = DocenteForm(sesion["datos"], instance=docente)
        if form.is_valid():
            form.save()
            registrar_auditoria(
                request.user, AuditLog.Accion.MODIFICAR, "Usuario", docente.id,
                {"campos": list(sesion["datos"].keys())},
                request,
            )
            del request.session["docente_editar"]
            messages.success(request, f"Docente {docente} modificado correctamente.")
            return redirect("administracion:docentes_lista")
        del request.session["docente_editar"]
        return redirect("administracion:docente_editar", docente_id=docente.id)

    datos = {"id": docente.id, **sesion["datos"]}
    return render(request, "administracion/docente_confirmar.html", {
        "datos": datos,
        "titulo": "Confirmar modificación de docente",
        "cancelar_url": reverse("administracion:docente_editar", args=[docente.id]),
        "volver_url": reverse("administracion:docentes_lista"),
    })


@directivo_o_admin
def docente_baja(request, docente_id):
    """Desactiva (is_active=False) a un docente con confirmación."""
    docente = get_object_or_404(Usuario, pk=docente_id, rol=Usuario.Rol.DOCENTE)
    if request.method == "POST":
        docente.is_active = False
        docente.save()
        registrar_auditoria(
            request.user, AuditLog.Accion.MODIFICAR, "Usuario", docente.id,
            {"is_active": False},
            request,
        )
        messages.success(request, f"Docente {docente} desactivado.")
        return redirect("administracion:docentes_lista")
    return render(request, "administracion/docente_confirmar.html", {
        "datos": {
            "id": docente.id,
            "username": docente.username,
            "first_name": docente.first_name,
            "last_name": docente.last_name,
            "email": docente.email,
        },
        "titulo": "Confirmar desactivación de docente",
        "es_baja": True,
        "cancelar_url": reverse("administracion:docentes_lista"),
        "volver_url": reverse("administracion:docentes_lista"),
    })


# ---------------------------------------------------------------------------
# Materias
# ---------------------------------------------------------------------------
@directivo_o_admin
def materias_lista(request):
    """Listado de materias."""
    materias = Materia.objects.all()
    return render(request, "administracion/materias_lista.html", {"materias": materias})


@directivo_o_admin
def materia_crear(request):
    """Paso 1: formulario de alta de materia (guarda en sesión)."""
    if request.method == "POST":
        form = MateriaForm(request.POST)
        if form.is_valid():
            request.session["materia_crear"] = _serializar_datos(form.cleaned_data)
            return redirect("administracion:materia_confirmar")
    else:
        form = MateriaForm()
    return render(request, "administracion/materia_form.html", {
        "form": form,
        "titulo": "Nueva materia",
        "accion_url": reverse("administracion:materia_crear"),
    })


@directivo_o_admin
def materia_confirmar(request):
    """Paso 2: muestra resumen y confirma la creación de la materia."""
    datos = request.session.get("materia_crear")
    if not datos:
        return redirect("administracion:materia_crear")

    if request.method == "POST":
        form = MateriaForm(datos)
        if form.is_valid():
            materia = form.save()
            registrar_auditoria(
                request.user, AuditLog.Accion.CREAR, "Materia", materia.id,
                {"nombre": materia.nombre},
                request,
            )
            del request.session["materia_crear"]
            messages.success(request, f"Materia {materia} creada correctamente.")
            return redirect("administracion:materias_lista")
        del request.session["materia_crear"]
        return redirect("administracion:materia_crear")

    return render(request, "administracion/materia_confirmar.html", {
        "datos": datos,
        "titulo": "Confirmar alta de materia",
        "cancelar_url": reverse("administracion:materia_crear"),
        "volver_url": reverse("administracion:materias_lista"),
    })


@directivo_o_admin
def materia_editar(request, materia_id):
    """Paso 1: formulario de edición de materia (guarda en sesión)."""
    materia = get_object_or_404(Materia, pk=materia_id)
    if request.method == "POST":
        form = MateriaForm(request.POST, instance=materia)
        if form.is_valid():
            request.session["materia_editar"] = {
                "id": materia.id,
                "datos": _serializar_datos(form.cleaned_data),
            }
            return redirect("administracion:materia_confirmar_editar")
    else:
        form = MateriaForm(instance=materia)
    return render(request, "administracion/materia_form.html", {
        "form": form,
        "titulo": f"Editar materia: {materia}",
        "accion_url": reverse("administracion:materia_editar", args=[materia.id]),
        "volver_url": reverse("administracion:materias_lista"),
    })


@directivo_o_admin
def materia_confirmar_editar(request):
    """Paso 2: confirma la edición de la materia."""
    sesion = request.session.get("materia_editar")
    if not sesion:
        return redirect("administracion:materias_lista")

    materia = get_object_or_404(Materia, pk=sesion["id"])
    if request.method == "POST":
        form = MateriaForm(sesion["datos"], instance=materia)
        if form.is_valid():
            form.save()
            registrar_auditoria(
                request.user, AuditLog.Accion.MODIFICAR, "Materia", materia.id,
                {"campos": list(sesion["datos"].keys())},
                request,
            )
            del request.session["materia_editar"]
            messages.success(request, f"Materia {materia} modificada correctamente.")
            return redirect("administracion:materias_lista")
        del request.session["materia_editar"]
        return redirect("administracion:materia_editar", materia_id=materia.id)

    datos = {"id": materia.id, **sesion["datos"]}
    return render(request, "administracion/materia_confirmar.html", {
        "datos": datos,
        "titulo": "Confirmar modificación de materia",
        "cancelar_url": reverse("administracion:materia_editar", args=[materia.id]),
        "volver_url": reverse("administracion:materias_lista"),
    })


@directivo_o_admin
def materia_baja(request, materia_id):
    """Da de baja (activa=False) a una materia con confirmación."""
    materia = get_object_or_404(Materia, pk=materia_id)
    if request.method == "POST":
        materia.activa = False
        materia.save()
        registrar_auditoria(
            request.user, AuditLog.Accion.MODIFICAR, "Materia", materia.id,
            {"activa": False},
            request,
        )
        messages.success(request, f"Materia {materia} dada de baja.")
        return redirect("administracion:materias_lista")
    return render(request, "administracion/materia_confirmar.html", {
        "datos": {"id": materia.id, "nombre": materia.nombre},
        "titulo": "Confirmar baja de materia",
        "es_baja": True,
        "cancelar_url": reverse("administracion:materias_lista"),
        "volver_url": reverse("administracion:materias_lista"),
    })


# ---------------------------------------------------------------------------
# Turnos
# ---------------------------------------------------------------------------
@directivo_o_admin
def turnos_lista(request):
    """Listado de turnos."""
    turnos = Turno.objects.all()
    return render(request, "administracion/turnos_lista.html", {"turnos": turnos})


@directivo_o_admin
def turno_crear(request):
    """Paso 1: formulario de alta de turno (guarda en sesión)."""
    if request.method == "POST":
        form = TurnoForm(request.POST)
        if form.is_valid():
            request.session["turno_crear"] = _serializar_datos(form.cleaned_data)
            return redirect("administracion:turno_confirmar")
    else:
        form = TurnoForm()
    return render(request, "administracion/turno_form.html", {
        "form": form,
        "titulo": "Nuevo turno",
        "accion_url": reverse("administracion:turno_crear"),
    })


@directivo_o_admin
def turno_confirmar(request):
    """Paso 2: muestra resumen y confirma la creación del turno."""
    datos = request.session.get("turno_crear")
    if not datos:
        return redirect("administracion:turno_crear")

    if request.method == "POST":
        form = TurnoForm(datos)
        if form.is_valid():
            turno = form.save()
            registrar_auditoria(
                request.user, AuditLog.Accion.CREAR, "Turno", turno.id,
                {"nombre": turno.nombre},
                request,
            )
            del request.session["turno_crear"]
            messages.success(request, f"Turno {turno} creado correctamente.")
            return redirect("administracion:turnos_lista")
        del request.session["turno_crear"]
        return redirect("administracion:turno_crear")

    return render(request, "administracion/turno_confirmar.html", {
        "datos": datos,
        "titulo": "Confirmar alta de turno",
        "cancelar_url": reverse("administracion:turno_crear"),
        "volver_url": reverse("administracion:turnos_lista"),
    })


@directivo_o_admin
def turno_editar(request, turno_id):
    """Paso 1: formulario de edición de turno (guarda en sesión)."""
    turno = get_object_or_404(Turno, pk=turno_id)
    if request.method == "POST":
        form = TurnoForm(request.POST, instance=turno)
        if form.is_valid():
            request.session["turno_editar"] = {
                "id": turno.id,
                "datos": _serializar_datos(form.cleaned_data),
            }
            return redirect("administracion:turno_confirmar_editar")
    else:
        form = TurnoForm(instance=turno)
    return render(request, "administracion/turno_form.html", {
        "form": form,
        "titulo": f"Editar turno: {turno}",
        "accion_url": reverse("administracion:turno_editar", args=[turno.id]),
        "volver_url": reverse("administracion:turnos_lista"),
    })


@directivo_o_admin
def turno_confirmar_editar(request):
    """Paso 2: confirma la edición del turno."""
    sesion = request.session.get("turno_editar")
    if not sesion:
        return redirect("administracion:turnos_lista")

    turno = get_object_or_404(Turno, pk=sesion["id"])
    if request.method == "POST":
        form = TurnoForm(sesion["datos"], instance=turno)
        if form.is_valid():
            form.save()
            registrar_auditoria(
                request.user, AuditLog.Accion.MODIFICAR, "Turno", turno.id,
                {"campos": list(sesion["datos"].keys())},
                request,
            )
            del request.session["turno_editar"]
            messages.success(request, f"Turno {turno} modificado correctamente.")
            return redirect("administracion:turnos_lista")
        del request.session["turno_editar"]
        return redirect("administracion:turno_editar", turno_id=turno.id)

    datos = {"id": turno.id, **sesion["datos"]}
    return render(request, "administracion/turno_confirmar.html", {
        "datos": datos,
        "titulo": "Confirmar modificación de turno",
        "cancelar_url": reverse("administracion:turno_editar", args=[turno.id]),
        "volver_url": reverse("administracion:turnos_lista"),
    })


@directivo_o_admin
def turno_baja(request, turno_id):
    """Da de baja (activo=False) a un turno con confirmación."""
    turno = get_object_or_404(Turno, pk=turno_id)
    if request.method == "POST":
        turno.activo = False
        turno.save()
        registrar_auditoria(
            request.user, AuditLog.Accion.MODIFICAR, "Turno", turno.id,
            {"activo": False},
            request,
        )
        messages.success(request, f"Turno {turno} dado de baja.")
        return redirect("administracion:turnos_lista")
    return render(request, "administracion/turno_confirmar.html", {
        "datos": {"id": turno.id, "nombre": turno.nombre},
        "titulo": "Confirmar baja de turno",
        "es_baja": True,
        "cancelar_url": reverse("administracion:turnos_lista"),
        "volver_url": reverse("administracion:turnos_lista"),
    })


# ---------------------------------------------------------------------------
# Cursos
# ---------------------------------------------------------------------------
@directivo_o_admin
def cursos_lista(request):
    """Listado de cursos."""
    cursos = Curso.objects.select_related("turno", "ciclo_lectivo").all()
    return render(request, "administracion/cursos_lista.html", {"cursos": cursos})


@directivo_o_admin
def curso_crear(request):
    """Paso 1: formulario de alta de curso (guarda en sesión)."""
    if request.method == "POST":
        form = CursoForm(request.POST)
        if form.is_valid():
            request.session["curso_crear"] = _serializar_datos(form.cleaned_data)
            return redirect("administracion:curso_confirmar")
    else:
        form = CursoForm()
    return render(request, "administracion/curso_form.html", {
        "form": form,
        "titulo": "Nuevo curso",
        "accion_url": reverse("administracion:curso_crear"),
    })


@directivo_o_admin
def curso_confirmar(request):
    """Paso 2: muestra resumen y confirma la creación del curso."""
    datos = request.session.get("curso_crear")
    if not datos:
        return redirect("administracion:curso_crear")

    if request.method == "POST":
        form = CursoForm(datos)
        if form.is_valid():
            curso = form.save()
            registrar_auditoria(
                request.user, AuditLog.Accion.CREAR, "Curso", curso.id,
                {"curso": str(curso)},
                request,
            )
            del request.session["curso_crear"]
            messages.success(request, f"Curso {curso} creado correctamente.")
            return redirect("administracion:cursos_lista")
        del request.session["curso_crear"]
        return redirect("administracion:curso_crear")

    return render(request, "administracion/curso_confirmar.html", {
        "datos": datos,
        "titulo": "Confirmar alta de curso",
        "cancelar_url": reverse("administracion:curso_crear"),
        "volver_url": reverse("administracion:cursos_lista"),
    })


@directivo_o_admin
def curso_editar(request, curso_id):
    """Paso 1: formulario de edición de curso (guarda en sesión)."""
    curso = get_object_or_404(Curso, pk=curso_id)
    if request.method == "POST":
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            request.session["curso_editar"] = {
                "id": curso.id,
                "datos": _serializar_datos(form.cleaned_data),
            }
            return redirect("administracion:curso_confirmar_editar")
    else:
        form = CursoForm(instance=curso)
    return render(request, "administracion/curso_form.html", {
        "form": form,
        "titulo": f"Editar curso: {curso}",
        "accion_url": reverse("administracion:curso_editar", args=[curso.id]),
        "volver_url": reverse("administracion:cursos_lista"),
    })


@directivo_o_admin
def curso_confirmar_editar(request):
    """Paso 2: confirma la edición del curso."""
    sesion = request.session.get("curso_editar")
    if not sesion:
        return redirect("administracion:cursos_lista")

    curso = get_object_or_404(Curso, pk=sesion["id"])
    if request.method == "POST":
        form = CursoForm(sesion["datos"], instance=curso)
        if form.is_valid():
            form.save()
            registrar_auditoria(
                request.user, AuditLog.Accion.MODIFICAR, "Curso", curso.id,
                {"campos": list(sesion["datos"].keys())},
                request,
            )
            del request.session["curso_editar"]
            messages.success(request, f"Curso {curso} modificado correctamente.")
            return redirect("administracion:cursos_lista")
        del request.session["curso_editar"]
        return redirect("administracion:curso_editar", curso_id=curso.id)

    datos = {"id": curso.id, **sesion["datos"]}
    return render(request, "administracion/curso_confirmar.html", {
        "datos": datos,
        "titulo": "Confirmar modificación de curso",
        "cancelar_url": reverse("administracion:curso_editar", args=[curso.id]),
        "volver_url": reverse("administracion:cursos_lista"),
    })


@directivo_o_admin
def curso_baja(request, curso_id):
    """Da de baja (activo=False) a un curso con confirmación."""
    curso = get_object_or_404(Curso, pk=curso_id)
    if request.method == "POST":
        curso.activo = False
        curso.save()
        registrar_auditoria(
            request.user, AuditLog.Accion.MODIFICAR, "Curso", curso.id,
            {"activo": False},
            request,
        )
        messages.success(request, f"Curso {curso} dado de baja.")
        return redirect("administracion:cursos_lista")
    return render(request, "administracion/curso_confirmar.html", {
        "datos": {"id": curso.id, "curso": str(curso)},
        "titulo": "Confirmar baja de curso",
        "es_baja": True,
        "cancelar_url": reverse("administracion:cursos_lista"),
        "volver_url": reverse("administracion:cursos_lista"),
    })


# ---------------------------------------------------------------------------
# Ciclos lectivos
# ---------------------------------------------------------------------------
@directivo_o_admin
def ciclos_lista(request):
    """Listado de ciclos lectivos."""
    ciclos = CicloLectivo.objects.all()
    return render(request, "administracion/ciclos_lista.html", {"ciclos": ciclos})


@directivo_o_admin
def ciclo_crear(request):
    """Paso 1: formulario de alta de ciclo (guarda en sesión)."""
    if request.method == "POST":
        form = CicloLectivoForm(request.POST)
        if form.is_valid():
            request.session["ciclo_crear"] = _serializar_datos(form.cleaned_data)
            return redirect("administracion:ciclo_confirmar")
    else:
        form = CicloLectivoForm()
    return render(request, "administracion/ciclo_form.html", {
        "form": form,
        "titulo": "Nuevo ciclo lectivo",
        "accion_url": reverse("administracion:ciclo_crear"),
    })


@directivo_o_admin
def ciclo_confirmar(request):
    """Paso 2: muestra resumen y confirma la creación del ciclo."""
    datos = request.session.get("ciclo_crear")
    if not datos:
        return redirect("administracion:ciclo_crear")

    if request.method == "POST":
        form = CicloLectivoForm(datos)
        if form.is_valid():
            ciclo = form.save()
            registrar_auditoria(
                request.user, AuditLog.Accion.CREAR, "CicloLectivo", ciclo.id,
                {"anio": ciclo.anio},
                request,
            )
            del request.session["ciclo_crear"]
            messages.success(request, f"Ciclo lectivo {ciclo} creado correctamente.")
            return redirect("administracion:ciclos_lista")
        del request.session["ciclo_crear"]
        return redirect("administracion:ciclo_crear")

    return render(request, "administracion/ciclo_confirmar.html", {
        "datos": datos,
        "titulo": "Confirmar alta de ciclo lectivo",
        "cancelar_url": reverse("administracion:ciclo_crear"),
        "volver_url": reverse("administracion:ciclos_lista"),
    })


@directivo_o_admin
def ciclo_editar(request, ciclo_id):
    """Paso 1: formulario de edición de ciclo (guarda en sesión)."""
    ciclo = get_object_or_404(CicloLectivo, pk=ciclo_id)
    if request.method == "POST":
        form = CicloLectivoForm(request.POST, instance=ciclo)
        if form.is_valid():
            request.session["ciclo_editar"] = {
                "id": ciclo.id,
                "datos": _serializar_datos(form.cleaned_data),
            }
            return redirect("administracion:ciclo_confirmar_editar")
    else:
        form = CicloLectivoForm(instance=ciclo)
    return render(request, "administracion/ciclo_form.html", {
        "form": form,
        "titulo": f"Editar ciclo lectivo: {ciclo}",
        "accion_url": reverse("administracion:ciclo_editar", args=[ciclo.id]),
        "volver_url": reverse("administracion:ciclos_lista"),
    })


@directivo_o_admin
def ciclo_confirmar_editar(request):
    """Paso 2: confirma la edición del ciclo lectivo."""
    sesion = request.session.get("ciclo_editar")
    if not sesion:
        return redirect("administracion:ciclos_lista")

    ciclo = get_object_or_404(CicloLectivo, pk=sesion["id"])
    if request.method == "POST":
        form = CicloLectivoForm(sesion["datos"], instance=ciclo)
        if form.is_valid():
            form.save()
            registrar_auditoria(
                request.user, AuditLog.Accion.MODIFICAR, "CicloLectivo", ciclo.id,
                {"campos": list(sesion["datos"].keys())},
                request,
            )
            del request.session["ciclo_editar"]
            messages.success(request, f"Ciclo lectivo {ciclo} modificado correctamente.")
            return redirect("administracion:ciclos_lista")
        del request.session["ciclo_editar"]
        return redirect("administracion:ciclo_editar", ciclo_id=ciclo.id)

    datos = {"id": ciclo.id, **sesion["datos"]}
    return render(request, "administracion/ciclo_confirmar.html", {
        "datos": datos,
        "titulo": "Confirmar modificación de ciclo lectivo",
        "cancelar_url": reverse("administracion:ciclo_editar", args=[ciclo.id]),
        "volver_url": reverse("administracion:ciclos_lista"),
    })


# ---------------------------------------------------------------------------
# Asignaciones docentes
# ---------------------------------------------------------------------------
@directivo_o_admin
def asignaciones_lista(request):
    """Listado de asignaciones docentes."""
    asignaciones = AsignacionDocente.objects.select_related(
        "docente", "materia", "curso"
    ).all()
    return render(request, "administracion/asignaciones_lista.html", {
        "asignaciones": asignaciones,
    })


@directivo_o_admin
def asignacion_crear(request):
    """Paso 1: formulario de alta de asignación (guarda en sesión)."""
    if request.method == "POST":
        form = AsignacionDocenteForm(request.POST)
        if form.is_valid():
            request.session["asignacion_crear"] = _serializar_datos(form.cleaned_data)
            return redirect("administracion:asignacion_confirmar")
    else:
        form = AsignacionDocenteForm()
    return render(request, "administracion/asignacion_form.html", {
        "form": form,
        "titulo": "Nueva asignación docente",
        "accion_url": reverse("administracion:asignacion_crear"),
    })


@directivo_o_admin
def asignacion_confirmar(request):
    """Paso 2: muestra resumen y confirma la creación de la asignación."""
    datos = request.session.get("asignacion_crear")
    if not datos:
        return redirect("administracion:asignacion_crear")

    if request.method == "POST":
        form = AsignacionDocenteForm(datos)
        if form.is_valid():
            asignacion = form.save()
            registrar_auditoria(
                request.user, AuditLog.Accion.CREAR, "AsignacionDocente",
                asignacion.id, {"asignacion": str(asignacion)},
                request,
            )
            del request.session["asignacion_crear"]
            messages.success(
                request, f"Asignación {asignacion} creada correctamente."
            )
            return redirect("administracion:asignaciones_lista")
        del request.session["asignacion_crear"]
        return redirect("administracion:asignacion_crear")

    return render(request, "administracion/asignacion_confirmar.html", {
        "datos": datos,
        "titulo": "Confirmar alta de asignación docente",
        "cancelar_url": reverse("administracion:asignacion_crear"),
        "volver_url": reverse("administracion:asignaciones_lista"),
    })


@directivo_o_admin
def asignacion_editar(request, asignacion_id):
    """Paso 1: formulario de edición de asignación (guarda en sesión)."""
    asignacion = get_object_or_404(AsignacionDocente, pk=asignacion_id)
    if request.method == "POST":
        form = AsignacionDocenteForm(request.POST, instance=asignacion)
        if form.is_valid():
            request.session["asignacion_editar"] = {
                "id": asignacion.id,
                "datos": _serializar_datos(form.cleaned_data),
            }
            return redirect("administracion:asignacion_confirmar_editar")
    else:
        form = AsignacionDocenteForm(instance=asignacion)
    return render(request, "administracion/asignacion_form.html", {
        "form": form,
        "titulo": f"Editar asignación: {asignacion}",
        "accion_url": reverse(
            "administracion:asignacion_editar", args=[asignacion.id]
        ),
        "volver_url": reverse("administracion:asignaciones_lista"),
    })


@directivo_o_admin
def asignacion_confirmar_editar(request):
    """Paso 2: confirma la edición de la asignación."""
    sesion = request.session.get("asignacion_editar")
    if not sesion:
        return redirect("administracion:asignaciones_lista")

    asignacion = get_object_or_404(AsignacionDocente, pk=sesion["id"])
    if request.method == "POST":
        form = AsignacionDocenteForm(sesion["datos"], instance=asignacion)
        if form.is_valid():
            form.save()
            registrar_auditoria(
                request.user, AuditLog.Accion.MODIFICAR,
                "AsignacionDocente", asignacion.id,
                {"campos": list(sesion["datos"].keys())},
                request,
            )
            del request.session["asignacion_editar"]
            messages.success(
                request, f"Asignación {asignacion} modificada correctamente."
            )
            return redirect("administracion:asignaciones_lista")
        del request.session["asignacion_editar"]
        return redirect(
            "administracion:asignacion_editar", asignacion_id=asignacion.id
        )

    datos = {"id": asignacion.id, **sesion["datos"]}
    return render(request, "administracion/asignacion_confirmar.html", {
        "datos": datos,
        "titulo": "Confirmar modificación de asignación docente",
        "cancelar_url": reverse(
            "administracion:asignacion_editar", args=[asignacion.id]
        ),
        "volver_url": reverse("administracion:asignaciones_lista"),
    })


@directivo_o_admin
def asignacion_baja(request, asignacion_id):
    """Da de baja (activa=False) a una asignación con confirmación."""
    asignacion = get_object_or_404(AsignacionDocente, pk=asignacion_id)
    if request.method == "POST":
        asignacion.activa = False
        asignacion.save()
        registrar_auditoria(
            request.user, AuditLog.Accion.MODIFICAR,
            "AsignacionDocente", asignacion.id,
            {"activa": False},
            request,
        )
        messages.success(request, f"Asignación {asignacion} dada de baja.")
        return redirect("administracion:asignaciones_lista")
    return render(request, "administracion/asignacion_confirmar.html", {
        "datos": {"id": asignacion.id, "asignacion": str(asignacion)},
        "titulo": "Confirmar baja de asignación docente",
        "es_baja": True,
        "cancelar_url": reverse("administracion:asignaciones_lista"),
        "volver_url": reverse("administracion:asignaciones_lista"),
    })


# ---------------------------------------------------------------------------
# Asignaciones alumno-curso
# ---------------------------------------------------------------------------
@directivo_o_admin
def asignaciones_alumnos_lista(request):
    """Listado de asignaciones alumno-curso."""
    asignaciones = AsignacionAlumnoCurso.objects.select_related(
        "alumno", "curso", "curso__turno", "ciclo_lectivo"
    ).all()
    return render(
        request,
        "administracion/asignaciones_alumnos_lista.html",
        {"asignaciones": asignaciones},
    )


@directivo_o_admin
def asignacion_alumno_crear(request):
    """Paso 1: formulario de alta de asignación alumno-curso (guarda en sesión)."""
    if request.method == "POST":
        form = AsignacionAlumnoCursoForm(request.POST)
        if form.is_valid():
            request.session["asignacion_alumno_crear"] = _serializar_datos(
                form.cleaned_data
            )
            return redirect("administracion:asignacion_alumno_confirmar")
    else:
        form = AsignacionAlumnoCursoForm()
    return render(request, "administracion/asignacion_alumno_form.html", {
        "form": form,
        "titulo": "Nueva asignación alumno-curso",
        "accion_url": reverse("administracion:asignacion_alumno_crear"),
    })


@directivo_o_admin
def asignacion_alumno_confirmar(request):
    """Paso 2: muestra resumen y confirma la creación de la asignación."""
    datos = request.session.get("asignacion_alumno_crear")
    if not datos:
        return redirect("administracion:asignacion_alumno_crear")

    if request.method == "POST":
        form = AsignacionAlumnoCursoForm(datos)
        if form.is_valid():
            asignacion = form.save()
            registrar_auditoria(
                request.user, AuditLog.Accion.CREAR, "AsignacionAlumnoCurso",
                asignacion.id, {"asignacion": str(asignacion)},
                request,
            )
            del request.session["asignacion_alumno_crear"]
            messages.success(
                request, f"Asignación {asignacion} creada correctamente."
            )
            return redirect("administracion:asignaciones_alumnos_lista")
        del request.session["asignacion_alumno_crear"]
        return redirect("administracion:asignacion_alumno_crear")

    return render(request, "administracion/asignacion_alumno_confirmar.html", {
        "datos": datos,
        "titulo": "Confirmar alta de asignación alumno-curso",
        "cancelar_url": reverse("administracion:asignacion_alumno_crear"),
        "volver_url": reverse("administracion:asignaciones_alumnos_lista"),
    })


@directivo_o_admin
def asignacion_alumno_editar(request, asignacion_id):
    """Paso 1: formulario de edición de asignación (guarda en sesión)."""
    asignacion = get_object_or_404(AsignacionAlumnoCurso, pk=asignacion_id)
    if request.method == "POST":
        form = AsignacionAlumnoCursoForm(request.POST, instance=asignacion)
        if form.is_valid():
            request.session["asignacion_alumno_editar"] = {
                "id": asignacion.id,
                "datos": _serializar_datos(form.cleaned_data),
            }
            return redirect("administracion:asignacion_alumno_confirmar_editar")
    else:
        form = AsignacionAlumnoCursoForm(instance=asignacion)
    return render(request, "administracion/asignacion_alumno_form.html", {
        "form": form,
        "titulo": f"Editar asignación: {asignacion}",
        "accion_url": reverse(
            "administracion:asignacion_alumno_editar", args=[asignacion.id]
        ),
        "volver_url": reverse("administracion:asignaciones_alumnos_lista"),
    })


@directivo_o_admin
def asignacion_alumno_confirmar_editar(request):
    """Paso 2: confirma la edición de la asignación."""
    sesion = request.session.get("asignacion_alumno_editar")
    if not sesion:
        return redirect("administracion:asignaciones_alumnos_lista")

    asignacion = get_object_or_404(AsignacionAlumnoCurso, pk=sesion["id"])
    if request.method == "POST":
        form = AsignacionAlumnoCursoForm(sesion["datos"], instance=asignacion)
        if form.is_valid():
            form.save()
            registrar_auditoria(
                request.user, AuditLog.Accion.MODIFICAR,
                "AsignacionAlumnoCurso", asignacion.id,
                {"campos": list(sesion["datos"].keys())},
                request,
            )
            del request.session["asignacion_alumno_editar"]
            messages.success(
                request,
                f"Asignación {asignacion} modificada correctamente.",
            )
            return redirect("administracion:asignaciones_alumnos_lista")
        del request.session["asignacion_alumno_editar"]
        return redirect(
            "administracion:asignacion_alumno_editar",
            asignacion_id=asignacion.id,
        )

    datos = {"id": asignacion.id, **sesion["datos"]}
    return render(request, "administracion/asignacion_alumno_confirmar.html", {
        "datos": datos,
        "titulo": "Confirmar modificación de asignación alumno-curso",
        "cancelar_url": reverse(
            "administracion:asignacion_alumno_editar", args=[asignacion.id]
        ),
        "volver_url": reverse("administracion:asignaciones_alumnos_lista"),
    })


@directivo_o_admin
def asignacion_alumno_baja(request, asignacion_id):
    """Da de baja (activa=False) a una asignación con confirmación."""
    asignacion = get_object_or_404(AsignacionAlumnoCurso, pk=asignacion_id)
    if request.method == "POST":
        asignacion.activa = False
        asignacion.save()
        registrar_auditoria(
            request.user, AuditLog.Accion.MODIFICAR,
            "AsignacionAlumnoCurso", asignacion.id,
            {"activa": False},
            request,
        )
        messages.success(request, f"Asignación {asignacion} dada de baja.")
        return redirect("administracion:asignaciones_alumnos_lista")
    return render(request, "administracion/asignacion_alumno_confirmar.html", {
        "datos": {"id": asignacion.id, "asignacion": str(asignacion)},
        "titulo": "Confirmar baja de asignación alumno-curso",
        "es_baja": True,
        "cancelar_url": reverse("administracion:asignaciones_alumnos_lista"),
        "volver_url": reverse("administracion:asignaciones_alumnos_lista"),
    })


# ---------------------------------------------------------------------------
# Horarios
# ---------------------------------------------------------------------------
@directivo_o_admin
def horarios_lista(request):
    """Listado de horarios de asignaciones docentes."""
    horarios = Horario.objects.select_related("asignacion_docente").all()
    return render(request, "administracion/horarios_lista.html", {
        "horarios": horarios,
    })


@directivo_o_admin
def horario_crear(request):
    """Paso 1: formulario de alta de horario (guarda en sesión)."""
    if request.method == "POST":
        form = HorarioForm(request.POST)
        if form.is_valid():
            request.session["horario_crear"] = _serializar_datos(form.cleaned_data)
            return redirect("administracion:horario_confirmar")
    else:
        form = HorarioForm()
    return render(request, "administracion/horario_form.html", {
        "form": form,
        "titulo": "Nuevo horario",
        "accion_url": reverse("administracion:horario_crear"),
    })


@directivo_o_admin
def horario_confirmar(request):
    """Paso 2: muestra resumen y confirma la creación del horario."""
    datos = request.session.get("horario_crear")
    if not datos:
        return redirect("administracion:horario_crear")

    if request.method == "POST":
        form = HorarioForm(datos)
        if form.is_valid():
            horario = form.save()
            registrar_auditoria(
                request.user, AuditLog.Accion.CREAR, "Horario", horario.id,
                {"horario": str(horario)},
                request,
            )
            del request.session["horario_crear"]
            messages.success(request, f"Horario {horario} creado correctamente.")
            return redirect("administracion:horarios_lista")
        del request.session["horario_crear"]
        return redirect("administracion:horario_crear")

    return render(request, "administracion/horario_confirmar.html", {
        "datos": datos,
        "titulo": "Confirmar alta de horario",
        "cancelar_url": reverse("administracion:horario_crear"),
        "volver_url": reverse("administracion:horarios_lista"),
    })


@directivo_o_admin
def horario_editar(request, horario_id):
    """Paso 1: formulario de edición de horario (guarda en sesión)."""
    horario = get_object_or_404(Horario, pk=horario_id)
    if request.method == "POST":
        form = HorarioForm(request.POST, instance=horario)
        if form.is_valid():
            request.session["horario_editar"] = {
                "id": horario.id,
                "datos": _serializar_datos(form.cleaned_data),
            }
            return redirect("administracion:horario_confirmar_editar")
    else:
        form = HorarioForm(instance=horario)
    return render(request, "administracion/horario_form.html", {
        "form": form,
        "titulo": f"Editar horario: {horario}",
        "accion_url": reverse("administracion:horario_editar", args=[horario.id]),
        "volver_url": reverse("administracion:horarios_lista"),
    })


@directivo_o_admin
def horario_confirmar_editar(request):
    """Paso 2: confirma la edición del horario."""
    sesion = request.session.get("horario_editar")
    if not sesion:
        return redirect("administracion:horarios_lista")

    horario = get_object_or_404(Horario, pk=sesion["id"])
    if request.method == "POST":
        form = HorarioForm(sesion["datos"], instance=horario)
        if form.is_valid():
            form.save()
            registrar_auditoria(
                request.user, AuditLog.Accion.MODIFICAR, "Horario", horario.id,
                {"campos": list(sesion["datos"].keys())},
                request,
            )
            del request.session["horario_editar"]
            messages.success(request, f"Horario {horario} modificado correctamente.")
            return redirect("administracion:horarios_lista")
        del request.session["horario_editar"]
        return redirect("administracion:horario_editar", horario_id=horario.id)

    datos = {"id": horario.id, **sesion["datos"]}
    return render(request, "administracion/horario_confirmar.html", {
        "datos": datos,
        "titulo": "Confirmar modificación de horario",
        "cancelar_url": reverse("administracion:horario_editar", args=[horario.id]),
        "volver_url": reverse("administracion:horarios_lista"),
    })


@directivo_o_admin
def horario_eliminar(request, horario_id):
    """Elimina físicamente un horario con confirmación y auditoría."""
    horario = get_object_or_404(Horario, pk=horario_id)
    if request.method == "POST":
        horario_str = str(horario)
        horario.delete()
        registrar_auditoria(
            request.user, AuditLog.Accion.ELIMINAR, "Horario", horario_id,
            {"horario": horario_str},
            request,
        )
        messages.success(request, f"Horario {horario_str} eliminado.")
        return redirect("administracion:horarios_lista")
    return render(request, "administracion/horario_confirmar.html", {
        "datos": {"id": horario.id, "horario": str(horario)},
        "titulo": "Confirmar eliminación de horario",
        "es_eliminacion": True,
        "cancelar_url": reverse("administracion:horarios_lista"),
        "volver_url": reverse("administracion:horarios_lista"),
    })
