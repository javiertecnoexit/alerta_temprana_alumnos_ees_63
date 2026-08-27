from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, models
from django.test import TestCase
from django.utils import timezone

from apps.alumnos.models import Alumno
from apps.ciclos_lectivos.models import CicloLectivo
from apps.estructura_escolar.models import Curso, Materia, Turno

from ..models import CatalogoObservacion, Observacion


class CatalogoObservacionTests(TestCase):
    def test_catalogo_str(self):
        """Verifica que __str__ retorna 'nombre (v1)'."""
        catalogo = CatalogoObservacion(
            nombre="Participa en clase",
            familia=CatalogoObservacion.Familia.PARTICIPACION,
        )
        self.assertEqual(str(catalogo), "Participa en clase (v1)")

    def test_catalogo_version_unico(self):
        """Verifica que nombre+versión es único."""
        CatalogoObservacion.objects.create(
            nombre="Realiza tareas",
            familia=CatalogoObservacion.Familia.TRABAJO_ACADEMICO,
            version=1,
        )
        with self.assertRaises(IntegrityError):
            CatalogoObservacion.objects.create(
                nombre="Realiza tareas",
                familia=CatalogoObservacion.Familia.TRABAJO_ACADEMICO,
                version=1,
            )

    def test_catalogo_default_activo(self):
        """Verifica que activo=True por defecto."""
        catalogo = CatalogoObservacion(
            nombre="Participa en clase",
            familia=CatalogoObservacion.Familia.PARTICIPACION,
        )
        self.assertTrue(catalogo.activo)

    def test_catalogo_default_caracter(self):
        """Verifica que caracter='neutro' por defecto."""
        catalogo = CatalogoObservacion(
            nombre="Participa en clase",
            familia=CatalogoObservacion.Familia.PARTICIPACION,
        )
        self.assertEqual(catalogo.caracter, CatalogoObservacion.Caracter.NEUTRO)


class ObservacionTests(TestCase):
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
        self.catalogo = CatalogoObservacion.objects.create(
            nombre="Participa en clase",
            familia=CatalogoObservacion.Familia.PARTICIPACION,
            caracter=CatalogoObservacion.Caracter.POSITIVO,
        )

    def crear_observacion(self, **kwargs):
        """Helper para crear una observación con valores por defecto."""
        defaults = {
            "alumno": self.alumno,
            "docente": self.docente,
            "materia": self.materia,
            "curso": self.curso,
            "catalogo": self.catalogo,
            "ciclo_lectivo": self.ciclo,
            "fecha_hora": timezone.make_aware(
                timezone.datetime(2026, 4, 15, 9, 30)
            ),
            "turno": "manana",
        }
        defaults.update(kwargs)
        return Observacion.objects.create(**defaults)

    def test_observacion_sin_materia(self):
        """Verifica que se puede crear una observación sin materia (preceptoría)."""
        obs = self.crear_observacion(materia=None)
        obs.refresh_from_db()
        self.assertIsNone(obs.materia)

    def test_observacion_str(self):
        """Verifica que __str__ incluye alumno, categoría y fecha."""
        obs = self.crear_observacion()
        self.assertEqual(str(obs), "Pérez, Juan — Participa en clase (15/04/2026)")

    def test_observacion_inmutable(self):
        """Verifica que la observación no tiene un método de edición (solo anulación)."""
        obs = self.crear_observacion()
        # No existe un método de edición en el modelo
        self.assertFalse(hasattr(obs, "editar"))
        self.assertFalse(hasattr(obs, "modificar"))
        self.assertFalse(hasattr(obs, "update"))

    def test_observacion_anulacion_requiere_motivo(self):
        """Verifica que anular sin motivo falla."""
        obs = self.crear_observacion(
            anulada=True,
            motivo_anulacion="",
        )
        with self.assertRaises(ValidationError):
            obs.full_clean()

    def test_observacion_vigente(self):
        """Verifica que vigente=True si no está anulada."""
        obs = self.crear_observacion()
        self.assertTrue(obs.vigente)

        obs_anulada = self.crear_observacion(
            anulada=True,
            motivo_anulacion="Error de registro",
        )
        self.assertFalse(obs_anulada.vigente)

    def test_observacion_fks_protect(self):
        """Verifica que los FK usan on_delete=PROTECT."""
        obs = self.crear_observacion()

        for campo in (
            "alumno",
            "docente",
            "materia",
            "curso",
            "catalogo",
            "ciclo_lectivo",
        ):
            fk = Observacion._meta.get_field(campo)
            self.assertEqual(fk.remote_field.on_delete, models.PROTECT)
