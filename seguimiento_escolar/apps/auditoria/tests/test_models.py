from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import AuditLog


class AuditLogTests(TestCase):
    def setUp(self):
        self.usuario = get_user_model().objects.create_user(
            username="admin1",
            password="pass12345",
        )

    def test_audit_log_str(self):
        """Verifica el formato de __str__."""
        # Se crea con objects.create para que timestamp tenga valor
        log = AuditLog.objects.create(
            usuario=self.usuario,
            accion=AuditLog.Accion.CREAR,
            modelo="Observacion",
            objeto_id=1,
        )
        self.assertTrue(str(log).startswith("admin1 — crear Observacion"))
        self.assertIn("Observacion", str(log))
        self.assertIn("/", str(log))

    def test_audit_log_creacion(self):
        """Verifica que se puede crear un registro."""
        log = AuditLog.objects.create(
            usuario=self.usuario,
            accion=AuditLog.Accion.LOGIN,
            modelo="Usuario",
            detalles={"ip": "127.0.0.1"},
        )
        self.assertEqual(log.accion, AuditLog.Accion.LOGIN)
        self.assertEqual(log.detalles, {"ip": "127.0.0.1"})

    def test_audit_log_inmutable_save(self):
        """Verifica que save con pk existente falla."""
        log = AuditLog.objects.create(
            usuario=self.usuario,
            accion=AuditLog.Accion.CREAR,
            modelo="Observacion",
        )
        log.accion = AuditLog.Accion.MODIFICAR
        with self.assertRaises(ValidationError):
            log.save()

    def test_audit_log_inmutable_delete(self):
        """Verifica que delete falla."""
        log = AuditLog.objects.create(
            usuario=self.usuario,
            accion=AuditLog.Accion.ELIMINAR,
            modelo="Alumno",
        )
        with self.assertRaises(ValidationError):
            log.delete()

    def test_audit_log_usuario_set_null(self):
        """Verifica que al borrar el usuario, el log queda con usuario=None."""
        log = AuditLog.objects.create(
            usuario=self.usuario,
            accion=AuditLog.Accion.LOGOUT,
            modelo="Usuario",
        )
        self.usuario.delete()
        log.refresh_from_db()
        self.assertIsNone(log.usuario)