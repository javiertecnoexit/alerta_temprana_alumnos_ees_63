from datetime import date, time, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from apps.ciclos_lectivos.models import CicloLectivo

from ..models import AsignacionDocente, Curso, Horario, Materia, Turno


class TurnoTests(TestCase):
    def test_turno_str(self):
        """Verifica que __str__ retorna 'Mañana'/'Tarde'."""
        turno_manana = Turno(nombre=Turno.Nombre.MANANA)
        turno_tarde = Turno(nombre=Turno.Nombre.TARDE)
        self.assertEqual(str(turno_manana), "Mañana")
        self.assertEqual(str(turno_tarde), "Tarde")

    def test_turno_unico(self):
        """Verifica que no se pueden crear dos turnos con el mismo nombre."""
        Turno.objects.create(nombre=Turno.Nombre.MANANA)
        with self.assertRaises(IntegrityError):
            Turno.objects.create(nombre=Turno.Nombre.MANANA)


class CursoTests(TestCase):
    def setUp(self):
        self.turno_manana = Turno.objects.create(nombre=Turno.Nombre.MANANA)
        self.ciclo = CicloLectivo.objects.create(
            anio=2026,
            fecha_inicio=date(2026, 3, 2),
            fecha_fin=date(2026, 11, 27),
        )

    def test_curso_str(self):
        """Verifica que __str__ retorna '3° B — Mañana'."""
        curso = Curso(
            anio=3,
            division="B",
            turno=self.turno_manana,
            ciclo_lectivo=self.ciclo,
        )
        self.assertEqual(str(curso), "3° B — Mañana")

    def test_curso_unico_por_turno_ciclo(self):
        """Verifica que no se puede duplicar un curso en el mismo turno/ciclo."""
        Curso.objects.create(
            anio=3,
            division="B",
            turno=self.turno_manana,
            ciclo_lectivo=self.ciclo,
        )
        with self.assertRaises(IntegrityError):
            Curso.objects.create(
                anio=3,
                division="B",
                turno=self.turno_manana,
                ciclo_lectivo=self.ciclo,
            )

    def test_curso_validacion_anio(self):
        """Verifica que se rechaza un año fuera del rango 1-6."""
        curso = Curso(
            anio=7,
            division="B",
            turno=self.turno_manana,
            ciclo_lectivo=self.ciclo,
        )
        with self.assertRaises(ValidationError):
            curso.full_clean()

    def test_curso_validacion_division(self):
        """Verifica que se rechaza una división inválida."""
        curso = Curso(
            anio=3,
            division="BB",
            turno=self.turno_manana,
            ciclo_lectivo=self.ciclo,
        )
        with self.assertRaises(ValidationError):
            curso.full_clean()


class MateriaTests(TestCase):
    def test_materia_str(self):
        """Verifica que __str__ retorna el nombre."""
        materia = Materia(nombre="Matemática")
        self.assertEqual(str(materia), "Matemática")

    def test_materia_unica(self):
        """Verifica que no se pueden duplicar nombres de materia."""
        Materia.objects.create(nombre="Lengua")
        with self.assertRaises(IntegrityError):
            Materia.objects.create(nombre="Lengua")


class AsignacionDocenteTests(TestCase):
    def setUp(self):
        self.docente = get_user_model().objects.create_user(
            username="docente1",
            password="pass12345",
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

    def test_asignacion_str(self):
        """Verifica que __str__ incluye docente, materia, curso y tipo."""
        asignacion = AsignacionDocente(
            docente=self.docente,
            materia=self.materia,
            curso=self.curso,
            fecha_inicio=date(2026, 3, 2),
        )
        self.assertEqual(
            str(asignacion),
            "docente1 — Matemática — 3° B — Mañana (Titular)",
        )

    def test_asignacion_fechas(self):
        """Verifica que fecha_fin debe ser posterior a fecha_inicio."""
        asignacion = AsignacionDocente(
            docente=self.docente,
            materia=self.materia,
            curso=self.curso,
            fecha_inicio=date(2026, 3, 2),
            fecha_fin=date(2026, 2, 1),
        )
        with self.assertRaises(ValidationError):
            asignacion.full_clean()

    def test_asignacion_vigente_sin_fecha_fin(self):
        """Verifica que vigente=True si no hay fecha de fin."""
        asignacion = AsignacionDocente.objects.create(
            docente=self.docente,
            materia=self.materia,
            curso=self.curso,
            fecha_inicio=date(2024, 3, 2),
        )
        self.assertTrue(asignacion.vigente)

    def test_asignacion_vigente_pasada(self):
        """Verifica que vigente=False si la fecha de fin ya pasó."""
        asignacion = AsignacionDocente.objects.create(
            docente=self.docente,
            materia=self.materia,
            curso=self.curso,
            fecha_inicio=date(2024, 3, 2),
            fecha_fin=timezone.localdate() - timedelta(days=1),
        )
        self.assertFalse(asignacion.vigente)

    def test_asignacion_tipo_default(self):
        """Verifica que el tipo por defecto es 'titular'."""
        asignacion = AsignacionDocente(
            docente=self.docente,
            materia=self.materia,
            curso=self.curso,
            fecha_inicio=date(2026, 3, 2),
        )
        self.assertEqual(asignacion.tipo, AsignacionDocente.Tipo.TITULAR)


class HorarioTests(TestCase):
    def setUp(self):
        self.docente = get_user_model().objects.create_user(
            username="docente1",
            password="pass12345",
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
        )

    def test_horario_str(self):
        """Verifica el formato de __str__."""
        horario = Horario(
            asignacion_docente=self.asignacion,
            dia_semana=Horario.DiaSemana.LUNES,
            hora_inicio=time(8, 0),
            hora_fin=time(9, 0),
        )
        self.assertEqual(str(horario), "Matemática — Lunes 08:00:00-09:00:00")

    def test_horario_horas(self):
        """Verifica que hora_inicio debe ser anterior a hora_fin."""
        horario = Horario(
            asignacion_docente=self.asignacion,
            dia_semana=Horario.DiaSemana.LUNES,
            hora_inicio=time(10, 0),
            hora_fin=time(9, 0),
        )
        with self.assertRaises(ValidationError):
            horario.full_clean()

    def test_horario_unico(self):
        """Verifica que no se puede duplicar día+hora para una asignación."""
        Horario.objects.create(
            asignacion_docente=self.asignacion,
            dia_semana=Horario.DiaSemana.LUNES,
            hora_inicio=time(8, 0),
            hora_fin=time(9, 0),
        )
        with self.assertRaises(IntegrityError):
            Horario.objects.create(
                asignacion_docente=self.asignacion,
                dia_semana=Horario.DiaSemana.LUNES,
                hora_inicio=time(8, 0),
                hora_fin=time(9, 0),
            )
