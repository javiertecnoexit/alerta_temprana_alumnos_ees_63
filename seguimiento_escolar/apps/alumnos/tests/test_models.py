from datetime import date

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from apps.ciclos_lectivos.models import CicloLectivo
from apps.estructura_escolar.models import Curso, Turno

from ..models import Alumno, AsignacionAlumnoCurso


class AlumnoTests(TestCase):
    def test_alumno_str(self):
        """Verifica que __str__ retorna 'Apellido, Nombre'."""
        alumno = Alumno(nombre="Juan", apellido="Pérez")
        self.assertEqual(str(alumno), "Pérez, Juan")

    def test_alumno_nombre_completo(self):
        """Verifica que nombre_completo retorna 'Nombre Apellido'."""
        alumno = Alumno(nombre="María", apellido="García")
        self.assertEqual(alumno.nombre_completo, "María García")

    def test_alumno_estado_default(self):
        """Verifica que el estado por defecto es 'activo'."""
        alumno = Alumno(nombre="Juan", apellido="Pérez")
        self.assertEqual(alumno.estado, Alumno.Estado.ACTIVO)


class AsignacionAlumnoCursoTests(TestCase):
    def setUp(self):
        self.alumno = Alumno.objects.create(nombre="Juan", apellido="Pérez")
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

    def test_asignacion_alumno_str(self):
        """Verifica que __str__ incluye alumno, curso y ciclo."""
        asignacion = AsignacionAlumnoCurso(
            alumno=self.alumno,
            curso=self.curso,
            ciclo_lectivo=self.ciclo,
            fecha_inicio=date(2026, 3, 2),
        )
        self.assertEqual(
            str(asignacion),
            "Pérez, Juan → 3° B — Mañana (Ciclo 2026 (Planificado))",
        )

    def test_asignacion_alumno_unica(self):
        """Verifica que no se puede duplicar alumno+curso+ciclo."""
        AsignacionAlumnoCurso.objects.create(
            alumno=self.alumno,
            curso=self.curso,
            ciclo_lectivo=self.ciclo,
            fecha_inicio=date(2026, 3, 2),
        )
        with self.assertRaises(IntegrityError):
            AsignacionAlumnoCurso.objects.create(
                alumno=self.alumno,
                curso=self.curso,
                ciclo_lectivo=self.ciclo,
                fecha_inicio=date(2026, 3, 2),
            )

    def test_asignacion_alumno_fechas(self):
        """Verifica que fecha_fin debe ser posterior a fecha_inicio."""
        asignacion = AsignacionAlumnoCurso(
            alumno=self.alumno,
            curso=self.curso,
            ciclo_lectivo=self.ciclo,
            fecha_inicio=date(2026, 3, 2),
            fecha_fin=date(2026, 2, 1),
        )
        with self.assertRaises(ValidationError):
            asignacion.full_clean()