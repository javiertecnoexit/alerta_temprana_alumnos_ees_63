from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.auditoria.models import AuditLog

from ..services import registrar_auditoria


class AuditoriaServiceTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.directivo = User.objects.create_user(
            username="directivo1",
            password="pass12345",
            rol=User.Rol.DIRECTIVO,
        )
        self.admin = User.objects.create_user(
            username="admin1",
            password="pass12345",
            rol=User.Rol.ADMIN,
        )
        self.docente = User.objects.create_user(
            username="docente1",
            password="pass12345",
            rol=User.Rol.DOCENTE,
        )
        self.preceptor = User.objects.create_user(
            username="preceptor1",
            password="pass12345",
            rol=User.Rol.PRECEPTOR,
        )

    def test_registrar_auditoria_crea_log(self):
        """El helper crea un AuditLog con los campos correctos."""
        log = registrar_auditoria(
            usuario=self.directivo,
            accion=AuditLog.Accion.CREAR,
            modelo="Alumno",
            objeto_id=1,
            detalles={"dni": "30111222"},
        )
        self.assertEqual(log.usuario, self.directivo)
        self.assertEqual(log.accion, AuditLog.Accion.CREAR)
        self.assertEqual(log.modelo, "Alumno")
        self.assertEqual(log.objeto_id, 1)
        self.assertEqual(log.detalles, {"dni": "30111222"})

    def test_audit_log_inmutable(self):
        """El helper usa AuditLog.objects.create (los logs son inmutables)."""
        log = registrar_auditoria(
            usuario=self.admin,
            accion=AuditLog.Accion.MODIFICAR,
            modelo="Curso",
            objeto_id=2,
        )
        log.accion = AuditLog.Accion.ELIMINAR
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            log.save()

    def test_index_requiere_permiso(self):
        """Directivo y admin acceden (200); docente y preceptor NO (403)."""
        url = reverse("administracion:index")
        # Directivo → 200
        self.client.force_login(self.directivo)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Admin (rol admin, sin superuser) → 200
        self.admin.is_superuser = False
        self.admin.save()
        self.client.force_login(self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Docente → 403
        self.client.force_login(self.docente)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        # Preceptor → 403
        self.client.force_login(self.preceptor)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_index_anonimo_redirige(self):
        """El usuario anónimo es redirigido a login."""
        response = self.client.get(reverse("administracion:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("usuarios:login"), response.url)