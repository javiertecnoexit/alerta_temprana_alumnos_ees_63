from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.alumnos.models import Alumno, AsignacionAlumnoCurso
from apps.ciclos_lectivos.models import CicloLectivo
from apps.estructura_escolar.models import Curso, Turno
from apps.observaciones.models import CatalogoObservacion, Observacion

from ..models import Intervencion, PreceptorTurno


class PreceptorAmpliadoTests(TestCase):
    """Tests del rol ampliado del preceptor (ficha, observaciones, intervenciones)."""

    def setUp(self):
        User = get_user_model()
        # Usuarios
        self.preceptor = User.objects.create_user(
            username="preceptor1",
            password="pass12345",
            rol=User.Rol.PRECEPTOR,
        )
        self.docente = User.objects.create_user(
            username="docente1",
            password="pass12345",
            rol=User.Rol.DOCENTE,
        )
        self.directivo = User.objects.create_user(
            username="directivo1",
            password="pass12345",
            rol=User.Rol.DIRECTIVO,
        )
        # Turnos
        self.turno_manana = Turno.objects.create(nombre=Turno.Nombre.MANANA)
        self.turno_tarde = Turno.objects.create(nombre=Turno.Nombre.TARDE)
        # Preceptor del turno mañana
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
            division="A",
            turno=self.turno_manana,
            ciclo_lectivo=self.ciclo,
        )
        self.curso_tarde = Curso.objects.create(
            anio=3,
            division="B",
            turno=self.turno_tarde,
            ciclo_lectivo=self.ciclo,
        )
        # Alumnos
        self.alumno_manana = Alumno.objects.create(
            nombre="Juan", apellido="Pérez", dni="30111222"
        )
        self.alumno_tarde = Alumno.objects.create(
            nombre="Ana", apellido="López", dni="30111223"
        )
        # Asignaciones alumno-curso
        AsignacionAlumnoCurso.objects.create(
            alumno=self.alumno_manana,
            curso=self.curso_manana,
            ciclo_lectivo=self.ciclo,
            fecha_inicio=date(2026, 3, 2),
        )
        AsignacionAlumnoCurso.objects.create(
            alumno=self.alumno_tarde,
            curso=self.curso_tarde,
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

    def test_preceptor_ve_ficha_su_turno(self):
        """El preceptor ve la ficha de un alumno de su turno."""
        self.client.force_login(self.preceptor)
        response = self.client.get(
            reverse("seguimiento:ficha_alumno", args=[self.alumno_manana.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pérez, Juan")

    def test_preceptor_no_ve_ficha_otro_turno(self):
        """El preceptor NO ve la ficha de un alumno de otro turno (403)."""
        self.client.force_login(self.preceptor)
        response = self.client.get(
            reverse("seguimiento:ficha_alumno", args=[self.alumno_tarde.id])
        )
        self.assertEqual(response.status_code, 403)

    def test_preceptor_registra_observacion(self):
        """El preceptor registra una observación sin materia."""
        self.client.force_login(self.preceptor)
        response = self.client.post(
            reverse(
                "seguimiento:preceptor_registrar_observacion",
                args=[self.alumno_manana.id],
            ),
            {"catalogo": self.catalogo.id},
        )
        self.assertEqual(response.status_code, 302)
        obs = Observacion.objects.get(alumno=self.alumno_manana)
        self.assertEqual(obs.docente, self.preceptor)
        self.assertIsNone(obs.materia)
        self.assertEqual(obs.turno, "manana")

    def test_preceptor_no_registra_observacion_otro_turno(self):
        """El preceptor NO registra observación de alumno de otro turno (403)."""
        self.client.force_login(self.preceptor)
        response = self.client.post(
            reverse(
                "seguimiento:preceptor_registrar_observacion",
                args=[self.alumno_tarde.id],
            ),
            {"catalogo": self.catalogo.id},
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Observacion.objects.count(), 0)

    def test_preceptor_registra_intervencion(self):
        """El preceptor registra una intervención de seguimiento."""
        self.client.force_login(self.preceptor)
        response = self.client.post(
            reverse(
                "seguimiento:preceptor_registrar_intervencion",
                args=[self.alumno_manana.id],
            ),
            {
                "tipo": Intervencion.Tipo.ACOMPANAMIENTO,
                "descripcion": "Seguimiento diario del alumno",
            },
        )
        self.assertEqual(response.status_code, 302)
        intervencion = Intervencion.objects.get(alumno=self.alumno_manana)
        self.assertEqual(intervencion.responsable, self.preceptor)
        self.assertEqual(intervencion.tipo, Intervencion.Tipo.ACOMPANAMIENTO)

    def test_preceptor_no_registra_intervencion_otro_turno(self):
        """El preceptor NO registra intervención de alumno de otro turno (403)."""
        self.client.force_login(self.preceptor)
        response = self.client.post(
            reverse(
                "seguimiento:preceptor_registrar_intervencion",
                args=[self.alumno_tarde.id],
            ),
            {
                "tipo": Intervencion.Tipo.ACOMPANAMIENTO,
                "descripcion": "Seguimiento diario",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Intervencion.objects.count(), 0)

    def test_docente_sigue_sin_acceso_ficha(self):
        """El docente sigue sin acceso a la ficha integral (403)."""
        self.client.force_login(self.docente)
        response = self.client.get(
            reverse("seguimiento:ficha_alumno", args=[self.alumno_manana.id])
        )
        self.assertEqual(response.status_code, 403)

    def test_directivo_sigue_viendo_todo(self):
        """El directivo ve cualquier ficha (de cualquier turno)."""
        self.client.force_login(self.directivo)
        for alumno in (self.alumno_manana, self.alumno_tarde):
            response = self.client.get(
                reverse("seguimiento:ficha_alumno", args=[alumno.id])
            )
            self.assertEqual(response.status_code, 200)

    def test_preceptor_ficha_enlace_volver_a_sus_alumnos(self):
        """La ficha del preceptor vuelve a su lista y no enlaza vistas del directivo."""
        self.client.force_login(self.preceptor)
        response = self.client.get(
            reverse("seguimiento:ficha_alumno", args=[self.alumno_manana.id])
        )
        self.assertEqual(response.status_code, 200)
        # Enlace de volver apunta a la vista del preceptor
        self.assertContains(
            response,
            'href="{}"'.format(reverse("seguimiento:preceptor_alumnos")),
        )
        self.assertContains(response, "← Volver")
        # No debe mostrar el enlace de volver del directivo
        self.assertNotContains(
            response,
            'href="{}"'.format(reverse("seguimiento:buscar_alumnos")),
        )
        # El botón de intervención apunta a la vista del preceptor (sin 403)
        self.assertContains(
            response,
            'href="{}"'.format(
                reverse(
                    "seguimiento:preceptor_registrar_intervencion",
                    args=[self.alumno_manana.id],
                )
            ),
        )
        self.assertNotContains(
            response,
            'href="{}"'.format(
                reverse(
                    "seguimiento:registrar_intervencion",
                    args=[self.alumno_manana.id],
                )
            ),
        )

    def test_directivo_ficha_enlace_volver_a_busqueda(self):
        """La ficha del directivo sigue volviendo a la búsqueda de alumnos."""
        self.client.force_login(self.directivo)
        response = self.client.get(
            reverse("seguimiento:ficha_alumno", args=[self.alumno_manana.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "← Volver a la búsqueda")
        self.assertContains(
            response,
            'href="{}"'.format(reverse("seguimiento:buscar_alumnos")),
        )
        self.assertNotContains(
            response,
            'href="{}"'.format(reverse("seguimiento:preceptor_alumnos")),
        )
        # El botón de intervención sigue siendo el institucional (solo directivo)
        self.assertContains(
            response,
            'href="{}"'.format(
                reverse(
                    "seguimiento:registrar_intervencion",
                    args=[self.alumno_manana.id],
                )
            ),
        )
        self.assertNotContains(
            response,
            'href="{}"'.format(
                reverse(
                    "seguimiento:preceptor_registrar_intervencion",
                    args=[self.alumno_manana.id],
                )
            ),
        )
