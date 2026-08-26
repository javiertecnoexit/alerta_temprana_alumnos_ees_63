from datetime import date

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from ..models import CicloLectivo


class CicloLectivoTests(TestCase):
    def setUp(self):
        self.fecha_inicio = date(2026, 3, 2)
        self.fecha_fin = date(2026, 11, 27)

    def test_ciclo_lectivo_str(self):
        """Verifica que __str__ retorna 'Ciclo 2026 (Activo)'."""
        ciclo = CicloLectivo(
            anio=2026,
            fecha_inicio=self.fecha_inicio,
            fecha_fin=self.fecha_fin,
            estado=CicloLectivo.Estado.ACTIVO,
        )
        self.assertEqual(str(ciclo), "Ciclo 2026 (Activo)")

    def test_ciclo_lectivo_fechas(self):
        """Verifica que la fecha de inicio debe ser anterior a la fecha de fin."""
        ciclo = CicloLectivo(
            anio=2026,
            fecha_inicio=self.fecha_fin,
            fecha_fin=self.fecha_inicio,
            estado=CicloLectivo.Estado.PLANIFICADO,
        )
        with self.assertRaises(ValidationError):
            ciclo.full_clean()

    def test_ciclo_lectivo_estado_default(self):
        """Verifica que el estado por defecto es 'planificado'."""
        ciclo = CicloLectivo(
            anio=2026,
            fecha_inicio=self.fecha_inicio,
            fecha_fin=self.fecha_fin,
        )
        self.assertEqual(ciclo.estado, CicloLectivo.Estado.PLANIFICADO)

    def test_ciclo_lectivo_unico_activo(self):
        """Verifica que solo puede haber un ciclo activo para un mismo año."""
        CicloLectivo.objects.create(
            anio=2026,
            fecha_inicio=self.fecha_inicio,
            fecha_fin=self.fecha_fin,
            estado=CicloLectivo.Estado.ACTIVO,
            activo=True,
        )
        with self.assertRaises(IntegrityError):
            CicloLectivo.objects.create(
                anio=2026,
                fecha_inicio=self.fecha_inicio,
                fecha_fin=self.fecha_fin,
                estado=CicloLectivo.Estado.ACTIVO,
                activo=True,
            )