from datetime import date, time

from django.contrib.auth import get_user_model
from django.db import IntegrityError, models
from django.test import TestCase

from apps.alumnos.models import Alumno
from apps.ciclos_lectivos.models import CicloLectivo
from apps.estructura_escolar.models import Curso, Materia, Turno

from ..models import RegistroAsistencia


class RegistroAsistenciaTests(TestCase):
    def setUp(self):
        self.alumno = Alumno.objects.create(nombre="Juan", apellido="Pérez")
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

    def crear_registro(self, **kwargs):
        """Helper para crear un registro de asistencia con valores por defecto."""
        defaults = {
            "alumno": self.alumno,
            "curso": self.curso,
            "docente": self.docente,
            "ciclo_lectivo": self.ciclo,
            "fecha": date(2026, 4, 15),
        }
        defaults.update(kwargs)
        return RegistroAsistencia.objects.create(**defaults)

    def test_asistencia_str(self):
        """Verifica el formato de __str__."""
        registro = self.crear_registro(estado=RegistroAsistencia.Estado.PRESENTE)
        self.assertEqual(str(registro), "Pérez, Juan — Presente (2026-04-15)")

    def test_asistencia_unica(self):
        """Verifica que no se puede duplicar alumno+fecha+materia+curso."""
        self.crear_registro(materia=self.materia)
        with self.assertRaises(IntegrityError):
            self.crear_registro(materia=self.materia)

    def test_asistencia_estado_default(self):
        """Verifica que el estado por defecto es 'presente'."""
        registro = self.crear_registro()
        self.assertEqual(registro.estado, RegistroAsistencia.Estado.PRESENTE)

    def test_asistencia_estados_validos(self):
        """Verifica que existen las 4 opciones de estado."""
        choices = dict(RegistroAsistencia.Estado.choices)
        self.assertEqual(
            choices,
            {
                "presente": "Presente",
                "ausente": "Ausente",
                "tardanza": "Tardanza",
                "justificado": "Justificado",
            },
        )

    def test_asistencia_hora_llegada_opcional(self):
        """Verifica que hora_llegada puede ser null."""
        registro = self.crear_registro()
        self.assertIsNone(registro.hora_llegada)

        registro_tardanza = self.crear_registro(
            estado=RegistroAsistencia.Estado.TARDANZA,
            hora_llegada=time(8, 30),
        )
        self.assertEqual(registro_tardanza.hora_llegada, time(8, 30))

    def test_asistencia_fks_protect(self):
        """Verifica que los FK usan on_delete=PROTECT."""
        registro = self.crear_registro()
        for campo in ("alumno", "curso", "materia", "docente", "ciclo_lectivo"):
            fk = RegistroAsistencia._meta.get_field(campo)
            self.assertEqual(fk.remote_field.on_delete, models.PROTECT)