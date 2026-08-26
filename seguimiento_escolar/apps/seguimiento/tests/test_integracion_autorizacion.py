from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.alumnos.models import Alumno, AsignacionAlumnoCurso
from apps.ciclos_lectivos.models import CicloLectivo
from apps.estructura_escolar.models import (
    AsignacionDocente,
    Curso,
    Materia,
    Turno,
)
from apps.observaciones.models import CatalogoObservacion, Observacion

from ..models import PreceptorTurno, SolicitudInfo


class TestIntegracionAutorizacion(TestCase):
    """Tests de integración de acceso horizontal (IDOR) y vertical (rol)."""

    def setUp(self):
        User = get_user_model()
        # Docentes
        self.docente_a = User.objects.create_user(
            username="docente_a",
            password="pass12345",
            rol=User.Rol.DOCENTE,
        )
        self.docente_b = User.objects.create_user(
            username="docente_b",
            password="pass12345",
            rol=User.Rol.DOCENTE,
        )
        # Roles
        self.directivo = User.objects.create_user(
            username="directivo1",
            password="pass12345",
            rol=User.Rol.DIRECTIVO,
        )
        self.preceptor = User.objects.create_user(
            username="preceptor1",
            password="pass12345",
            rol=User.Rol.PRECEPTOR,
        )
        self.admin = User.objects.create_user(
            username="admin1",
            password="pass12345",
            rol=User.Rol.ADMIN,
        )
        # Turnos y ciclo
        self.turno_manana = Turno.objects.create(nombre=Turno.Nombre.MANANA)
        self.turno_tarde = Turno.objects.create(nombre=Turno.Nombre.TARDE)
        PreceptorTurno.objects.create(
            preceptor=self.preceptor, turno=self.turno_manana
        )
        self.ciclo = CicloLectivo.objects.create(
            anio=2026,
            fecha_inicio=date(2026, 3, 2),
            fecha_fin=date(2026, 11, 27),
        )
        # Cursos (mismo ciclo, turnos distintos)
        self.curso_a = Curso.objects.create(
            anio=3,
            division="A",
            turno=self.turno_manana,
            ciclo_lectivo=self.ciclo,
        )
        self.curso_b = Curso.objects.create(
            anio=4,
            division="B",
            turno=self.turno_tarde,
            ciclo_lectivo=self.ciclo,
        )
        # Materias
        self.materia_1 = Materia.objects.create(nombre="Matemática")
        self.materia_2 = Materia.objects.create(nombre="Lengua")
        # Asignaciones (docente_a→curso_a, docente_b→curso_b)
        self.asignacion_a = AsignacionDocente.objects.create(
            docente=self.docente_a,
            materia=self.materia_1,
            curso=self.curso_a,
            fecha_inicio=date(2026, 3, 2),
            activa=True,
        )
        self.asignacion_b = AsignacionDocente.objects.create(
            docente=self.docente_b,
            materia=self.materia_2,
            curso=self.curso_b,
            fecha_inicio=date(2026, 3, 2),
            activa=True,
        )
        # Alumnos
        self.alumno_a = Alumno.objects.create(
            nombre="Juan", apellido="Pérez", dni="30111222"
        )
        self.alumno_b = Alumno.objects.create(
            nombre="Ana", apellido="López", dni="30111223"
        )
        # Asignaciones alumno-curso
        AsignacionAlumnoCurso.objects.create(
            alumno=self.alumno_a,
            curso=self.curso_a,
            ciclo_lectivo=self.ciclo,
            fecha_inicio=date(2026, 3, 2),
        )
        AsignacionAlumnoCurso.objects.create(
            alumno=self.alumno_b,
            curso=self.curso_b,
            ciclo_lectivo=self.ciclo,
            fecha_inicio=date(2026, 3, 2),
        )
        # Catálogo
        self.catalogo = CatalogoObservacion.objects.create(
            nombre="Participa en clase",
            familia=CatalogoObservacion.Familia.PARTICIPACION,
            caracter=CatalogoObservacion.Caracter.POSITIVO,
            activo=True,
        )
        # Observaciones (cada docente sobre su alumno)
        self.obs_docente_a = Observacion.objects.create(
            alumno=self.alumno_a,
            docente=self.docente_a,
            materia=self.materia_1,
            curso=self.curso_a,
            catalogo=self.catalogo,
            ciclo_lectivo=self.ciclo,
            fecha_hora="2026-04-15T09:30:00-03:00",
            turno="manana",
        )
        self.obs_docente_b = Observacion.objects.create(
            alumno=self.alumno_b,
            docente=self.docente_b,
            materia=self.materia_2,
            curso=self.curso_b,
            catalogo=self.catalogo,
            ciclo_lectivo=self.ciclo,
            fecha_hora="2026-04-15T10:30:00-03:00",
            turno="tarde",
        )

    # ---------- 1. Acceso horizontal (IDOR) ----------

    def test_docente_no_accede_observaciones_otro_docente(self):
        """El docente A solo ve sus observaciones en su historial."""
        self.client.force_login(self.docente_a)
        response = self.client.get(reverse("observaciones:historial"))
        self.assertEqual(response.status_code, 200)
        # Ve la suya
        self.assertContains(response, "Pérez, Juan")
        # No ve la de docente_b (López, Ana)
        self.assertNotContains(response, "López, Ana")

    def test_docente_no_accede_ficha_alumno_otro_curso(self):
        """El docente A no accede a la ficha del alumno de curso B."""
        self.client.force_login(self.docente_a)
        response = self.client.get(
            reverse("seguimiento:ficha_alumno", args=[self.alumno_b.id])
        )
        # directivo_requerido → 403 para docente
        self.assertEqual(response.status_code, 403)

    def test_docente_no_accede_asistencia_otro_curso(self):
        """El docente A no accede a la lista de alumnos del curso B (asignación ajena)."""
        self.client.force_login(self.docente_a)
        response = self.client.get(
            reverse("observaciones:lista_alumnos", args=[self.asignacion_b.id])
        )
        # La asignación b pertenece a docente_b → 404
        self.assertEqual(response.status_code, 404)

    def test_preceptor_solo_su_turno(self):
        """El preceptor de turno mañana no ve alumnos de turno tarde."""
        self.client.force_login(self.preceptor)
        response = self.client.get(reverse("seguimiento:preceptor_alumnos"))
        self.assertEqual(response.status_code, 200)
        # Ve alumno de turno mañana (Pérez)
        self.assertContains(response, "Pérez, Juan")
        # No ve alumno de turno tarde (López, Ana)
        self.assertNotContains(response, "López, Ana")

    # ---------- 2. Acceso vertical (rol) ----------

    def test_directivo_ve_todo(self):
        """El directivo ve observaciones de todos los docentes."""
        self.client.force_login(self.directivo)
        response = self.client.get(
            reverse("seguimiento:ficha_alumno", args=[self.alumno_a.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Participa en clase")

        # También ve el historial completo vía búsqueda
        response2 = self.client.get(reverse("seguimiento:buscar_alumnos"))
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, "Pérez, Juan")
        self.assertContains(response2, "López, Ana")

    def test_admin_no_ve_datos_pedagogicos(self):
        """Un admin (rol admin) sin is_superuser no accede a datos pedagógicos."""
        self.admin.is_superuser = False
        self.admin.save()
        self.client.force_login(self.admin)
        response = self.client.get(reverse("seguimiento:buscar_alumnos"))
        # directivo_requerido → admin no incluido → 403
        self.assertEqual(response.status_code, 403)

    def test_anonimo_no_accede_ningun_endpoint(self):
        """El anónimo es redirigido a login en todos los endpoints protegidos."""
        endpoints = [
            reverse("observaciones:lista_cursos"),
            reverse("observaciones:historial"),
            reverse("seguimiento:buscar_alumnos"),
            reverse("seguimiento:preceptor_alumnos"),
            reverse("seguimiento:lista_solicitudes"),
        ]
        for url in endpoints:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                302,
                f"Anónimo debiera redirigir en {url}",
            )
            self.assertIn(reverse("usuarios:login"), response.url)

    def test_suplantacion_asignacion(self):
        """El docente A no puede registrar usando la asignación del docente B."""
        self.client.force_login(self.docente_a)
        url = reverse(
            "observaciones:registrar",
            args=[self.asignacion_b.id, self.alumno_b.id],
        )
        response = self.client.post(
            url,
            {"catalogo": self.catalogo.id},
        )
        self.assertEqual(response.status_code, 404)
        # No se crea una observación nueva para docente_a sobre alumno_b
        self.assertFalse(
            Observacion.objects.filter(
                docente=self.docente_a, alumno=self.alumno_b
            ).exists()
        )

    def test_observacion_inmutable(self):
        """No existe vista de edición de observaciones (inmutables)."""
        self.client.force_login(self.docente_a)
        url_edicion = (
            f"/observaciones/observacion/{self.obs_docente_a.id}/editar/"
        )
        response = self.client.get(url_edicion)
        # No hay ruta → 404 (no existe endpoint de edición)
        self.assertEqual(response.status_code, 404)

    def test_solicitud_solo_alumnos_propios(self):
        """El docente A no puede crear solicitud para alumno del curso B."""
        self.client.force_login(self.docente_a)
        response = self.client.post(
            reverse("seguimiento:solicitar_info"),
            {"alumno": self.alumno_b.id, "motivo": "Quiero información"},
        )
        # El formulario solo ofrece alumnos de sus cursos → el POST no crea
        # la solicitud porque alumno_b no está en la queryset del form.
        self.assertEqual(SolicitudInfo.objects.count(), 0)