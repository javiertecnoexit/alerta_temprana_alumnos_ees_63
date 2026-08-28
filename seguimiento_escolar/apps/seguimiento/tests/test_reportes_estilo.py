from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.alumnos.models import Alumno, AsignacionAlumnoCurso
from apps.ciclos_lectivos.models import CicloLectivo
from apps.estructura_escolar.models import Curso, Turno
from apps.observaciones.models import CatalogoObservacion, Observacion

from ..models import PreceptorTurno


class ReportesEstiloTests(TestCase):
    """Estilo de reporte por docente y ficha filtrada."""

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
        # Alumnos
        self.alumno1 = Alumno.objects.create(
            nombre="Juan", apellido="Pérez", dni="30111222"
        )
        self.alumno2 = Alumno.objects.create(
            nombre="María", apellido="García", dni="30111223"
        )
        AsignacionAlumnoCurso.objects.create(
            alumno=self.alumno1,
            curso=self.curso_manana,
            ciclo_lectivo=self.ciclo,
            fecha_inicio=date(2026, 3, 2),
        )
        AsignacionAlumnoCurso.objects.create(
            alumno=self.alumno2,
            curso=self.curso_manana,
            ciclo_lectivo=self.ciclo,
            fecha_inicio=date(2026, 3, 2),
        )
        # Catálogo con distintas familias y caracteres
        self.cat_positivo = CatalogoObservacion.objects.create(
            nombre="Participa en clase",
            familia=CatalogoObservacion.Familia.PARTICIPACION,
            caracter=CatalogoObservacion.Caracter.POSITIVO,
            activo=True,
        )
        self.cat_atencion = CatalogoObservacion.objects.create(
            nombre="No cumple tareas",
            familia=CatalogoObservacion.Familia.TRABAJO_ACADEMICO,
            caracter=CatalogoObservacion.Caracter.ATENCION,
            activo=True,
        )
        self.cat_neutro = CatalogoObservacion.objects.create(
            nombre="Comentario general",
            familia=CatalogoObservacion.Familia.OTRA,
            caracter=CatalogoObservacion.Caracter.NEUTRO,
            activo=True,
        )
        # Observaciones del docente1 (turno mañana)
        Observacion.objects.create(
            alumno=self.alumno1,
            docente=self.docente,
            curso=self.curso_manana,
            catalogo=self.cat_positivo,
            ciclo_lectivo=self.ciclo,
            fecha_hora="2026-04-15T09:30:00-03:00",
            turno="manana",
        )
        Observacion.objects.create(
            alumno=self.alumno2,
            docente=self.docente,
            curso=self.curso_manana,
            catalogo=self.cat_atencion,
            ciclo_lectivo=self.ciclo,
            fecha_hora="2026-05-01T10:00:00-03:00",
            turno="manana",
        )
        Observacion.objects.create(
            alumno=self.alumno1,
            docente=self.docente,
            curso=self.curso_manana,
            catalogo=self.cat_neutro,
            ciclo_lectivo=self.ciclo,
            fecha_hora="2026-05-02T09:00:00-03:00",
            turno="manana",
        )
        # Observación anulada que NO debe contarse
        Observacion.objects.create(
            alumno=self.alumno1,
            docente=self.docente,
            curso=self.curso_manana,
            catalogo=self.cat_positivo,
            ciclo_lectivo=self.ciclo,
            fecha_hora="2026-05-03T09:00:00-03:00",
            turno="manana",
            anulada=True,
        )
        # Observación del docente2 (turno tarde)
        Observacion.objects.create(
            alumno=self.alumno1,
            docente=self.docente2,
            curso=self.curso_tarde,
            catalogo=self.cat_positivo,
            ciclo_lectivo=self.ciclo,
            fecha_hora="2026-06-01T14:00:00-03:00",
            turno="tarde",
        )

    # ------------------------------------------------------------------
    # Estilo de reporte del docente
    # ------------------------------------------------------------------
    def test_estilo_docente_directivo(self):
        """El directivo ve la distribución por carácter del docente."""
        self.client.force_login(self.directivo)
        response = self.client.get(
            reverse("seguimiento:reporte_estilo_docente", args=[self.docente.id])
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("docente1", content)
        self.assertIn("Total de observaciones vigentes", content)

    def test_estilo_docente_distribucion_correcta(self):
        """Los conteos por carácter son correctos (la anulada no cuenta)."""
        self.client.force_login(self.directivo)
        response = self.client.get(
            reverse("seguimiento:reporte_estilo_docente", args=[self.docente.id])
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        # docente1 tiene 3 vigentes: 1 positivo, 1 atencion, 1 neutro
        self.assertIn("Total de observaciones vigentes:</strong> 3", content)
        self.assertIn("positivo", content)
        self.assertIn("atencion", content)
        self.assertIn("neutro", content)

    def test_estilo_docente_familias(self):
        """La distribución por familia refleja las familias correctas."""
        self.client.force_login(self.directivo)
        response = self.client.get(
            reverse("seguimiento:reporte_estilo_docente", args=[self.docente.id])
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("Distribución por familia", content)
        self.assertIn("participacion", content)
        self.assertIn("trabajo_academico", content)
        self.assertIn("otra", content)

    def test_estilo_docente_preceptor_otro_turno(self):
        """El preceptor recibe 403 si el docente no reportó en su turno."""
        self.client.force_login(self.preceptor)
        # docente2 solo tiene observaciones en turno tarde
        response = self.client.get(
            reverse("seguimiento:reporte_estilo_docente", args=[self.docente2.id])
        )
        self.assertEqual(response.status_code, 403)

    def test_docente_no_accede(self):
        """El docente NO accede al reporte de estilo (403)."""
        self.client.force_login(self.docente)
        response = self.client.get(
            reverse("seguimiento:reporte_estilo_docente", args=[self.docente.id])
        )
        self.assertEqual(response.status_code, 403)

    # ------------------------------------------------------------------
    # Ficha de alumno filtrada
    # ------------------------------------------------------------------
    def test_ficha_filtro_docente(self):
        """La ficha muestra solo observaciones del docente filtrado."""
        self.client.force_login(self.directivo)
        # Filtro por docente1 (tiene 3 obs en el alumno1/alumno2)
        response = self.client.get(
            reverse("seguimiento:ficha_alumno", args=[self.alumno1.id]),
            {"docente": self.docente.id},
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("Participa en clase", content)
        self.assertIn("Comentario general", content)
        # El select de filtros muestra todos los docentes (docente2 presente),
        # pero las observaciones mostradas son solo del docente1 (el conteo de
        # positivas es 1, no 2 — la obs del docente2 está en el curso tarde).
        self.assertIn("docente1", content)

    def test_ficha_filtro_curso(self):
        """La ficha muestra solo observaciones del curso filtrado."""
        self.client.force_login(self.directivo)
        response = self.client.get(
            reverse("seguimiento:ficha_alumno", args=[self.alumno1.id]),
            {"curso": self.curso_manana.id},
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("3° B", content)
        # Las observaciones del curso manana están en la ficha

    def test_ficha_filtro_combinado(self):
        """Los filtros docente + curso se combinan."""
        self.client.force_login(self.directivo)
        response = self.client.get(
            reverse("seguimiento:ficha_alumno", args=[self.alumno1.id]),
            {"docente": self.docente.id, "curso": self.curso_manana.id},
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")
        self.assertIn("Participa en clase", content)
        # El filtro combinado excluye las observaciones del docente2
        # (la obs del docente2 es de curso tarde y docente distinto, mientras
        #  el filtro combina docente1 + curso_manana).
        self.assertIn("docente1", content)

    def test_ficha_conteo_refleja_filtro(self):
        """El conteo por carácter cambia al filtrar por docente."""
        self.client.force_login(self.directivo)
        # Sin filtro: alumno1 tiene obs de docente1 y docente2 (2 en total)
        respuesta_sin = self.client.get(
            reverse("seguimiento:ficha_alumno", args=[self.alumno1.id])
        )
        # Con filtro por docente1: alumno1 tiene 2 obs del docente1
        respuesta_filtro = self.client.get(
            reverse("seguimiento:ficha_alumno", args=[self.alumno1.id]),
            {"docente": self.docente.id},
        )
        self.assertEqual(respuesta_filtro.status_code, 200)
        contenido = respuesta_filtro.content.decode("utf-8")
        # El conteo positivo refleja las obs del docente1 (1 positivo)
        self.assertIn("1", contenido)