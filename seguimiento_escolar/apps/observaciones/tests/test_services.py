from datetime import date, time

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.ciclos_lectivos.models import CicloLectivo
from apps.estructura_escolar.models import (
    AsignacionDocente,
    Curso,
    Horario,
    Materia,
    Turno,
)

from ..services import es_dentro_de_horario


class EsDentroDeHorarioTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.docente = User.objects.create_user(
            username="docente1",
            password="pass12345",
            rol=User.Rol.DOCENTE,
        )
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
        # Horario lunes 08:00-10:00
        Horario.objects.create(
            asignacion_docente=self.asignacion,
            dia_semana=Horario.DiaSemana.LUNES,
            hora_inicio=time(8, 0),
            hora_fin=time(10, 0),
        )

    def hacer_fecha(self, weekday, hora, minuto):
        """Crea una fecha aware para el día de la semana dado (0=lunes)."""
        # 2026-03-02 es lunes → weekday 0
        fecha = date(2026, 3, 2 + weekday)
        return timezone.make_aware(
            timezone.datetime(fecha.year, fecha.month, fecha.day, hora, minuto)
        )

    def test_dentro_horario_correcto(self):
        """Lunes 09:00 dentro de la franja 08:00-10:00 → True."""
        fecha = self.hacer_fecha(0, 9, 0)
        self.assertTrue(es_dentro_de_horario(self.asignacion, fecha))

    def test_fuera_horario_correcto(self):
        """Lunes 11:00 fuera de la franja → False."""
        fecha = self.hacer_fecha(0, 11, 0)
        self.assertFalse(es_dentro_de_horario(self.asignacion, fecha))

    def test_dia_sin_horario(self):
        """Martes sin horario asignado → False."""
        fecha = self.hacer_fecha(1, 9, 0)
        self.assertFalse(es_dentro_de_horario(self.asignacion, fecha))

    def test_fin_de_semana(self):
        """Sábado y domingo → False."""
        sabado = self.hacer_fecha(5, 9, 0)  # 2026-03-07 sábado
        domingo = self.hacer_fecha(6, 9, 0)  # 2026-03-08 domingo
        self.assertFalse(es_dentro_de_horario(self.asignacion, sabado))
        self.assertFalse(es_dentro_de_horario(self.asignacion, domingo))

    def test_limite_horario_inicio(self):
        """Exactamente en hora_inicio (08:00) → True."""
        fecha = self.hacer_fecha(0, 8, 0)
        self.assertTrue(es_dentro_de_horario(self.asignacion, fecha))

    def test_limite_horario_fin(self):
        """Exactamente en hora_fin (10:00) → True."""
        fecha = self.hacer_fecha(0, 10, 0)
        self.assertTrue(es_dentro_de_horario(self.asignacion, fecha))