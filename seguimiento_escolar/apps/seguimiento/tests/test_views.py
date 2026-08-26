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

from ..models import PreceptorTurno


class SeguimientoViewsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        # Usuarios
        self.directivo = User.objects.create_user(
            username="directivo1",
            password="pass12345",
            rol=User.Rol.DIRECTIVO,
        )
        self.docente = User.objects.create_user(
            username="docente1",
            password="pass12345",
            rol=User.Rol.DOCENTE,
        )
        self.preceptor = User.objects.create_user(
            username="preceptor1",
            password="pass12345",
            rol=User.Rol.PRECEPTOR,
        )
        # Turnos
        self.turno_manana = Turno.objects.create(nombre=Turno.Nombre.MANANA)
        self.turno_tarde = Turno.objects.create(nombre=Turno.Nombre.TARDE)
        # Preceptor asignado al turno mañana
        PreceptorTurno.objects.create(
            preceptor=self.preceptor, turno=self.turno_manana
        )
        # Ciclo y cursos
        self.ciclo = CicloLectivo.objects.create(
            anio=2026,
            fecha_inicio=date(2026, 3, 2),
            fecha_fin=date(2026, 11, 27),
        )
        self.curso_manana = Curso.objects.create(
            anio=3,
            division="B",
            turno=self.turno_manana,
            ciclo_lectivo=self.ciclo,
        )
        self.curso_tarde = Curso.objects.create(
            anio=4,
            division="A",
            turno=self.turno_tarde,
            ciclo_lectivo=self.ciclo,
        )
        self.materia = Materia.objects.create(nombre="Matemática")
        # Asignación docente
        self.asignacion = AsignacionDocente.objects.create(
            docente=self.docente,
            materia=self.materia,
            curso=self.curso_manana,
            fecha_inicio=date(2026, 3, 2),
            activa=True,
        )
        # Alumnos
        self.alumno1 = Alumno.objects.create(
            nombre="Juan", apellido="Pérez", dni="30111222"
        )
        self.alumno2 = Alumno.objects.create(
            nombre="María", apellido="García", dni="30111223"
        )
        # Asignaciones alumno-curso (ambos en turno mañana)
        self.asig_al1 = AsignacionAlumnoCurso.objects.create(
            alumno=self.alumno1,
            curso=self.curso_manana,
            ciclo_lectivo=self.ciclo,
            fecha_inicio=date(2026, 3, 2),
        )
        self.asig_al2 = AsignacionAlumnoCurso.objects.create(
            alumno=self.alumno2,
            curso=self.curso_manana,
            ciclo_lectivo=self.ciclo,
            fecha_inicio=date(2026, 3, 2),
        )
        # Categoría y observaciones de ambos docentes
        self.catalogo = CatalogoObservacion.objects.create(
            nombre="Participa en clase",
            familia=CatalogoObservacion.Familia.PARTICIPACION,
            caracter=CatalogoObservacion.Caracter.POSITIVO,
            activo=True,
        )
        otro_docente = User.objects.create_user(
            username="docente2",
            password="pass12345",
            rol=User.Rol.DOCENTE,
        )
        self.obs_doc1 = Observacion.objects.create(
            alumno=self.alumno1,
            docente=self.docente,
            materia=self.materia,
            curso=self.curso_manana,
            catalogo=self.catalogo,
            ciclo_lectivo=self.ciclo,
            fecha_hora="2026-04-15T09:30:00-03:00",
            turno="manana",
        )
        self.obs_doc2 = Observacion.objects.create(
            alumno=self.alumno1,
            docente=otro_docente,
            materia=self.materia,
            curso=self.curso_manana,
            catalogo=self.catalogo,
            ciclo_lectivo=self.ciclo,
            fecha_hora="2026-04-16T10:00:00-03:00",
            turno="manana",
        )

    # ---------- Directivo ----------

    def test_buscar_alumnos_directivo(self):
        """El directivo accede a la búsqueda de alumnos."""
        self.client.force_login(self.directivo)
        response = self.client.get(reverse("seguimiento:buscar_alumnos"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pérez, Juan")

    def test_buscar_alumnos_docente_denegado(self):
        """El docente NO accede a la búsqueda de alumnos (403)."""
        self.client.force_login(self.docente)
        response = self.client.get(reverse("seguimiento:buscar_alumnos"))
        self.assertEqual(response.status_code, 403)

    def test_ficha_alumno_directivo(self):
        """El directivo ve observaciones de TODOS los docentes."""
        self.client.force_login(self.directivo)
        response = self.client.get(
            reverse("seguimiento:ficha_alumno", args=[self.alumno1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Participa en clase")

    def test_ficha_alumno_muestra_todas_materias(self):
        """La ficha agrupa observaciones y el conteo muestra datos."""
        self.client.force_login(self.directivo)
        response = self.client.get(
            reverse("seguimiento:ficha_alumno", args=[self.alumno1.id])
        )
        self.assertEqual(response.status_code, 200)
        # Hay 2 observaciones → conteo positivo = 2
        self.assertContains(response, "2")
        # Ambas observaciones están agrupadas bajo la materia
        self.assertContains(response, "Matemática")

    def test_ficha_alumno_docente_denegado(self):
        """El docente NO accede a la ficha integral (403)."""
        self.client.force_login(self.docente)
        response = self.client.get(
            reverse("seguimiento:ficha_alumno", args=[self.alumno1.id])
        )
        self.assertEqual(response.status_code, 403)

    # ---------- Preceptor ----------

    def test_preceptor_su_turno(self):
        """El preceptor ve solo alumnos de su turno (mañana)."""
        self.client.force_login(self.preceptor)
        response = self.client.get(reverse("seguimiento:preceptor_alumnos"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pérez, Juan")
        self.assertContains(response, "García, María")

    def test_preceptor_otro_turno_denegado(self):
        """El preceptor no ve alumnos de otros turnos."""
        # Alumno en turno tarde
        alumno_tarde = Alumno.objects.create(
            nombre="Ana", apellido="López", dni="30111224"
        )
        AsignacionAlumnoCurso.objects.create(
            alumno=alumno_tarde,
            curso=self.curso_tarde,
            ciclo_lectivo=self.ciclo,
            fecha_inicio=date(2026, 3, 2),
        )
        self.client.force_login(self.preceptor)
        response = self.client.get(reverse("seguimiento:preceptor_alumnos"))
        self.assertEqual(response.status_code, 200)
        # No debe aparecer el alumno del turno tarde
        self.assertNotContains(response, "López, Ana")

    # ---------- Genéricos ----------

    def test_ficha_no_muestra_diagnostico(self):
        """La ficha solo muestra datos observados (sin diagnósticos)."""
        self.client.force_login(self.directivo)
        response = self.client.get(
            reverse("seguimiento:ficha_alumno", args=[self.alumno1.id])
        )
        content = response.content.decode("utf-8")
        # No hay etiquetas diagnósticas
        self.assertNotIn("Diagnóstico", content)
        self.assertNotIn("diagnóstico", content)

    def test_anonimo_redirige(self):
        """El usuario anónimo es redirigido a login."""
        response = self.client.get(reverse("seguimiento:buscar_alumnos"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("usuarios:login"), response.url)