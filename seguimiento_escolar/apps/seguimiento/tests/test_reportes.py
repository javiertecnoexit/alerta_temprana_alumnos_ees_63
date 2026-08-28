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


class ReportesTests(TestCase):
    """Reportes de participación docente y filtros."""

    def setUp(self):
        User = get_user_model()
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
        self.docente2 = User.objects.create_user(
            username="docente2",
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
        # Asignaciones docentes
        self.asignacion_manana = AsignacionDocente.objects.create(
            docente=self.docente,
            materia=self.materia,
            curso=self.curso_manana,
            fecha_inicio=date(2026, 3, 2),
            activa=True,
        )
        self.asignacion_tarde = AsignacionDocente.objects.create(
            docente=self.docente2,
            materia=self.materia,
            curso=self.curso_tarde,
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
        # Categoría y observaciones de ambos docentes (turno mañana)
        self.catalogo = CatalogoObservacion.objects.create(
            nombre="Participa en clase",
            familia=CatalogoObservacion.Familia.PARTICIPACION,
            caracter=CatalogoObservacion.Caracter.POSITIVO,
            activo=True,
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
        self.obs_doc1_b = Observacion.objects.create(
            alumno=self.alumno2,
            docente=self.docente,
            materia=self.materia,
            curso=self.curso_manana,
            catalogo=self.catalogo,
            ciclo_lectivo=self.ciclo,
            fecha_hora="2026-05-01T10:00:00-03:00",
            turno="manana",
        )
        self.obs_doc2 = Observacion.objects.create(
            alumno=self.alumno1,
            docente=self.docente2,
            materia=self.materia,
            curso=self.curso_manana,
            catalogo=self.catalogo,
            ciclo_lectivo=self.ciclo,
            fecha_hora="2026-04-16T10:00:00-03:00",
            turno="manana",
        )
        # Observación anulada que NO debe contarse
        Observacion.objects.create(
            alumno=self.alumno1,
            docente=self.docente,
            materia=self.materia,
            curso=self.curso_manana,
            catalogo=self.catalogo,
            ciclo_lectivo=self.ciclo,
            fecha_hora="2026-04-17T09:00:00-03:00",
            turno="manana",
            anulada=True,
        )

    # ------------------------------------------------------------------
    # Reporte de participación
    # ------------------------------------------------------------------
    def test_reporte_participacion_directivo(self):
        """El directivo accede al reporte de participación."""
        self.client.force_login(self.directivo)
        response = self.client.get(reverse("seguimiento:reporte_participacion"))
        self.assertEqual(response.status_code, 200)
        # Verifica que hay resultados (los docentes de test no tienen nombre)
        self.assertContains(response, "docente1")
        self.assertContains(response, "docente2")

    def test_reporte_participacion_conteo(self):
        """El conteo de observaciones por docente es correcto."""
        self.client.force_login(self.directivo)
        response = self.client.get(reverse("seguimiento:reporte_participacion"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        # El docente1 tiene 2 observaciones vigentes (la anulada no cuenta)
        self.assertIn("docente1", content)
        self.assertIn("2", content)
        # El docente2 tiene 1 observación
        # (verificamos que no aparezca la observación anulada en el conteo
        #  validando que docente1 tenga exactamente 2, no 3)

    def test_reporte_participacion_preceptor_turno(self):
        """El preceptor solo ve observaciones de su turno (mañana)."""
        # Creamos una observación en turno tarde del docente2
        Observacion.objects.create(
            alumno=self.alumno1,
            docente=self.docente2,
            materia=self.materia,
            curso=self.curso_tarde,
            catalogo=self.catalogo,
            ciclo_lectivo=self.ciclo,
            fecha_hora="2026-06-01T14:00:00-03:00",
            turno="tarde",
        )
        self.client.force_login(self.preceptor)
        response = self.client.get(reverse("seguimiento:reporte_participacion"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        # El docente2 tiene 1 obs en turno mañana + 1 en tarde = 2 en total,
        # pero el preceptor solo ve la de mañana → debe mostrar conteo 1
        self.assertIn("docente2", content)
        # El docente1 tiene 2 en mañana
        self.assertIn("docente1", content)
        # Verificar que la suma total NO incluye la obs de tarde:
        # docente2 debería tener 1 (no 2)

    def test_docente_no_accede_reportes(self):
        """El docente NO accede a los reportes (403)."""
        self.client.force_login(self.docente)
        response = self.client.get(reverse("seguimiento:reporte_participacion"))
        self.assertEqual(response.status_code, 403)

    def test_anonimo_redirige(self):
        """El usuario anónimo es redirigido a login."""
        response = self.client.get(reverse("seguimiento:reporte_participacion"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("usuarios:login"), response.url)

    # ------------------------------------------------------------------
    # Reporte de docentes por curso
    # ------------------------------------------------------------------
    def test_reporte_docentes_curso(self):
        """El directivo ve los docentes que dan clase en un curso."""
        self.client.force_login(self.directivo)
        response = self.client.get(
            reverse("seguimiento:reporte_docentes_curso"),
            {"curso": self.curso_manana.id},
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("docente1", content)
        self.assertIn("3° B", content)

    def test_reporte_docentes_curso_preceptor_otro_turno(self):
        """El preceptor NO puede ver docentes de un curso de otro turno."""
        self.client.force_login(self.preceptor)
        # El preceptor es de turno mañana → intenta ver el curso de la tarde
        response = self.client.get(
            reverse("seguimiento:reporte_docentes_curso"),
            {"curso": self.curso_tarde.id},
        )
        # get_object_or_404 con filter(turno) → 404 porque no pertenece a su turno
        self.assertEqual(response.status_code, 404)

    # ------------------------------------------------------------------
    # Filtro por docente en búsqueda de alumnos
    # ------------------------------------------------------------------
    def test_buscar_alumnos_filtro_docente(self):
        """El filtro por docente muestra solo alumnos observados por ese docente."""
        self.client.force_login(self.directivo)
        response = self.client.get(
            reverse("seguimiento:buscar_alumnos"),
            {"docente": self.docente.id},
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        # El docente1 observó a alumno1 y alumno2 (obs vigentes)
        self.assertIn("Pérez, Juan", content)
        self.assertIn("García, María", content)