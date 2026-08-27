from datetime import date, time
from unittest.mock import patch

from django.utils import timezone as dj_timezone

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.alumnos.models import Alumno, AsignacionAlumnoCurso
from apps.ciclos_lectivos.models import CicloLectivo
from apps.estructura_escolar.models import (
    AsignacionDocente,
    Curso,
    Horario,
    Materia,
    Turno,
)
from apps.observaciones.models import CatalogoObservacion, Observacion


class ObservacionesViewsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        # Docentes
        self.docente = User.objects.create_user(
            username="docente1",
            password="pass12345",
            rol=User.Rol.DOCENTE,
        )
        self.otro_docente = User.objects.create_user(
            username="docente2",
            password="pass12345",
            rol=User.Rol.DOCENTE,
        )
        # Estructura
        self.turno_manana = Turno.objects.create(nombre=Turno.Nombre.MANANA)
        self.ciclo = CicloLectivo.objects.create(
            anio=2026,
            fecha_inicio=date(2026, 3, 2),
            fecha_fin=date(2026, 11, 27),
        )
        self.curso = Curso.objects.create(
            anio=3,
            division="B",
            turno=self.turno_manana,
            ciclo_lectivo=self.ciclo,
        )
        self.materia = Materia.objects.create(nombre="Matemática")
        self.asignacion = AsignacionDocente.objects.create(
            docente=self.docente,
            materia=self.materia,
            curso=self.curso,
            fecha_inicio=date(2026, 3, 2),
            activa=True,
        )
        # Asignación del otro docente (curso diferente)
        self.curso2 = Curso.objects.create(
            anio=4,
            division="A",
            turno=self.turno_manana,
            ciclo_lectivo=self.ciclo,
        )
        self.asignacion_otro = AsignacionDocente.objects.create(
            docente=self.otro_docente,
            materia=self.materia,
            curso=self.curso2,
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
        # Asignación alumno-curso (ambos alumnos en curso1)
        self.asig_alumno1 = AsignacionAlumnoCurso.objects.create(
            alumno=self.alumno1,
            curso=self.curso,
            ciclo_lectivo=self.ciclo,
            fecha_inicio=date(2026, 3, 2),
        )
        self.asig_alumno2 = AsignacionAlumnoCurso.objects.create(
            alumno=self.alumno2,
            curso=self.curso,
            ciclo_lectivo=self.ciclo,
            fecha_inicio=date(2026, 3, 2),
        )
        # Categoría de catálogo
        self.catalogo = CatalogoObservacion.objects.create(
            nombre="Participa en clase",
            familia=CatalogoObservacion.Familia.PARTICIPACION,
            caracter=CatalogoObservacion.Caracter.POSITIVO,
            activo=True,
        )
        # Login helper
        self.client.force_login(self.docente)

    def test_lista_cursos_docente(self):
        """El docente ve sus cursos (asignaciones)."""
        response = self.client.get(reverse("observaciones:lista_cursos"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "3° B — Mañana")
        # No ve el curso del otro docente
        self.assertNotContains(response, "4° A — Mañana")

    def test_lista_cursos_sin_asignaciones(self):
        """Un docente sin asignaciones ve lista vacía."""
        # Docente sin asignaciones
        docente_sin = get_user_model().objects.create_user(
            username="docente_sin",
            password="pass12345",
            rol=get_user_model().Rol.DOCENTE,
        )
        self.client.force_login(docente_sin)
        response = self.client.get(reverse("observaciones:lista_cursos"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No tenés asignaciones vigentes")

    def test_lista_alumnos_propia(self):
        """El docente ve los alumnos de su curso."""
        response = self.client.get(
            reverse("observaciones:lista_alumnos", args=[self.asignacion.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pérez, Juan")
        self.assertContains(response, "García, María")

    def test_lista_alumnos_ajena(self):
        """El docente NO ve alumnos de un curso que no le pertenece."""
        response = self.client.get(
            reverse("observaciones:lista_alumnos", args=[self.asignacion_otro.id])
        )
        self.assertEqual(response.status_code, 404)

    def test_lista_alumnos_no_muestra_dni(self):
        """El docente NO ve el DNI de los alumnos en la lista."""
        response = self.client.get(
            reverse("observaciones:lista_alumnos", args=[self.asignacion.id])
        )
        self.assertEqual(response.status_code, 200)
        # El DNI de alumno1 es "30111222"
        self.assertNotContains(response, "30111222")
        # El DNI de alumno2 es "30111223"
        self.assertNotContains(response, "30111223")

    def test_registrar_observacion_valida(self):
        """El docente registra una observación correctamente."""
        url = reverse(
            "observaciones:registrar",
            args=[self.asignacion.id, self.alumno1.id],
        )
        response = self.client.post(
            url,
            {"catalogo": self.catalogo.id, "comentario": "Buen desempeño"},
        )
        self.assertEqual(response.status_code, 302)
        obs = Observacion.objects.get(alumno=self.alumno1)
        self.assertEqual(obs.docente, self.docente)
        self.assertEqual(obs.comentario, "Buen desempeño")

    def test_registrar_observacion_ajena(self):
        """El docente NO puede registrar en un curso ajeno."""
        url = reverse(
            "observaciones:registrar",
            args=[self.asignacion_otro.id, self.alumno1.id],
        )
        response = self.client.post(
            url,
            {"catalogo": self.catalogo.id},
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Observacion.objects.count(), 0)

    def test_registrar_observacion_contexto(self):
        """La observación captura materia/curso/turno/ciclo automáticamente."""
        url = reverse(
            "observaciones:registrar",
            args=[self.asignacion.id, self.alumno1.id],
        )
        self.client.post(
            url,
            {"catalogo": self.catalogo.id},
        )
        obs = Observacion.objects.get(alumno=self.alumno1)
        self.assertEqual(obs.materia, self.materia)
        self.assertEqual(obs.curso, self.curso)
        self.assertEqual(obs.ciclo_lectivo, self.ciclo)
        self.assertEqual(obs.turno, "manana")

    def test_historial_propio(self):
        """El historial muestra solo las observaciones propias."""
        Observacion.objects.create(
            alumno=self.alumno1,
            docente=self.docente,
            materia=self.materia,
            curso=self.curso,
            catalogo=self.catalogo,
            ciclo_lectivo=self.ciclo,
            fecha_hora="2026-04-15T09:30:00-03:00",
            turno="manana",
        )
        response = self.client.get(reverse("observaciones:historial"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pérez, Juan")

    def test_historial_no_muestra_otros(self):
        """El historial NO muestra observaciones de otros docentes."""
        # Observación del otro docente
        Observacion.objects.create(
            alumno=self.alumno1,
            docente=self.otro_docente,
            materia=self.materia,
            curso=self.curso,
            catalogo=self.catalogo,
            ciclo_lectivo=self.ciclo,
            fecha_hora="2026-04-15T10:00:00-03:00",
            turno="manana",
        )
        response = self.client.get(reverse("observaciones:historial"))
        self.assertEqual(response.status_code, 200)
        # El historial del docente1 no muestra observaciones del docente2
        self.assertContains(response, "Todavía no registraste observaciones")

    def test_anonimo_redirige(self):
        """Un usuario anónimo es redirigido a login."""
        self.client.logout()
        response = self.client.get(reverse("observaciones:lista_cursos"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("usuarios:login"), response.url)

    def test_registro_observacion_dentro_horario(self):
        """La vista guarda dentro_horario=True cuando hay clase en ese momento."""
        # Horario lunes 08:00-10:00 (2026-03-02 es lunes)
        Horario.objects.create(
            asignacion_docente=self.asignacion,
            dia_semana=Horario.DiaSemana.LUNES,
            hora_inicio=time(8, 0),
            hora_fin=time(10, 0),
        )
        fecha_fija = dj_timezone.make_aware(
            dj_timezone.datetime(2026, 3, 2, 9, 0)  # lunes 09:00
        )
        url = reverse(
            "observaciones:registrar",
            args=[self.asignacion.id, self.alumno1.id],
        )
        with patch("apps.observaciones.views.timezone.now", return_value=fecha_fija):
            self.client.post(url, {"catalogo": self.catalogo.id})
        obs = Observacion.objects.get(alumno=self.alumno1)
        self.assertTrue(obs.dentro_horario)

    def test_registro_observacion_fuera_horario(self):
        """La vista guarda dentro_horario=False cuando no hay clase en ese momento."""
        # Sin horarios asignados → lunes a las 09:00 no es horario de clase
        fecha_fija = dj_timezone.make_aware(
            dj_timezone.datetime(2026, 3, 2, 9, 0)  # lunes 09:00
        )
        url = reverse(
            "observaciones:registrar",
            args=[self.asignacion.id, self.alumno1.id],
        )
        with patch("apps.observaciones.views.timezone.now", return_value=fecha_fija):
            self.client.post(url, {"catalogo": self.catalogo.id})
        obs = Observacion.objects.get(alumno=self.alumno1)
        self.assertFalse(obs.dentro_horario)
