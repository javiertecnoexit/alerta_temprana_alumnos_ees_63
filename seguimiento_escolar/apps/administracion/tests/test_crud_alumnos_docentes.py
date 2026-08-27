from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.alumnos.models import Alumno
from apps.auditoria.models import AuditLog

User = get_user_model()


class CrudAlumnosDocentesTests(TestCase):
    """CRUD de alumnos y docentes con confirmación y auditoría."""

    def setUp(self):
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
        self.alumno = Alumno.objects.create(
            nombre="Ana",
            apellido="Pérez",
            dni="30111222",
        )

    # ------------------------------------------------------------------
    # Alumnos
    # ------------------------------------------------------------------
    def test_alumno_crear(self):
        """Directivo crea un alumno con el flujo de 2 pasos (confirmación)."""
        self.client.force_login(self.directivo)

        # Paso 1: enviar el formulario → redirige a confirmación
        response = self.client.post(reverse("administracion:alumno_crear"), {
            "nombre": "Carlos",
            "apellido": "Gómez",
            "dni": "40222333",
            "fecha_nacimiento": "2010-03-15",
            "estado": "activo",
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("administracion:alumno_confirmar"))

        # Paso 2: confirmar → crea el alumno y redirige a la lista
        response = self.client.post(reverse("administracion:alumno_confirmar"))
        self.assertRedirects(response, reverse("administracion:alumnos_lista"))

        alumno = Alumno.objects.get(dni="40222333")
        self.assertEqual(alumno.nombre, "Carlos")
        self.assertEqual(alumno.apellido, "Gómez")

    def test_alumno_crear_auditado(self):
        """La creación de un alumno queda registrada en AuditLog."""
        self.client.force_login(self.directivo)
        self.client.post(reverse("administracion:alumno_crear"), {
            "nombre": "Carlos",
            "apellido": "Gómez",
            "dni": "40222333",
            "fecha_nacimiento": "2010-03-15",
            "estado": "activo",
        })
        self.client.post(reverse("administracion:alumno_confirmar"))

        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.CREAR,
            modelo="Alumno",
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario, self.directivo)
        self.assertEqual(log.detalles.get("apellido"), "Gómez")

    def test_alumno_editar(self):
        """Edita un alumno y registra la acción en el AuditLog."""
        self.client.force_login(self.directivo)

        # Paso 1: formulario de edición
        response = self.client.post(
            reverse("administracion:alumno_editar", args=[self.alumno.id]),
            {
                "nombre": "Ana María",
                "apellido": "Pérez",
                "dni": "30111222",
                "fecha_nacimiento": "",
                "estado": "activo",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("administracion:alumno_confirmar_editar"))

        # Paso 2: confirmar
        self.client.post(reverse("administracion:alumno_confirmar_editar"))

        self.alumno.refresh_from_db()
        self.assertEqual(self.alumno.nombre, "Ana María")
        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.MODIFICAR,
            modelo="Alumno",
            objeto_id=self.alumno.id,
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario, self.directivo)

    def test_alumno_baja(self):
        """Da de baja (estado inactivo) a un alumno con confirmación."""
        self.client.force_login(self.directivo)
        self.assertEqual(self.alumno.estado, Alumno.Estado.ACTIVO)

        self.client.post(
            reverse("administracion:alumno_baja", args=[self.alumno.id])
        )

        self.alumno.refresh_from_db()
        self.assertEqual(self.alumno.estado, Alumno.Estado.INACTIVO)
        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.MODIFICAR,
            modelo="Alumno",
            objeto_id=self.alumno.id,
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.detalles.get("estado"), "inactivo")

    # ------------------------------------------------------------------
    # Docentes
    # ------------------------------------------------------------------
    def test_docente_crear(self):
        """Crea un usuario con rol docente mediante el flujo de 2 pasos."""
        self.client.force_login(self.directivo)

        # Paso 1: formulario → redirige a confirmación
        response = self.client.post(reverse("administracion:docente_crear"), {
            "username": "docente_nuevo",
            "first_name": "Laura",
            "last_name": "Fernández",
            "email": "laura@es63.edu.ar",
            "password": "Segura123",
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("administracion:docente_confirmar"))

        # Paso 2: confirmar → crea el usuario docente
        self.client.post(reverse("administracion:docente_confirmar"))

        docente = User.objects.get(username="docente_nuevo")
        self.assertEqual(docente.rol, User.Rol.DOCENTE)
        self.assertTrue(docente.check_password("Segura123"))

    def test_docente_crear_auditado(self):
        """La creación de un docente queda registrada en AuditLog."""
        self.client.force_login(self.directivo)
        self.client.post(reverse("administracion:docente_crear"), {
            "username": "docente_nuevo",
            "first_name": "Laura",
            "last_name": "Fernández",
            "email": "laura@es63.edu.ar",
            "password": "Segura123",
        })
        self.client.post(reverse("administracion:docente_confirmar"))

        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.CREAR,
            modelo="Usuario",
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario, self.directivo)
        self.assertEqual(log.detalles.get("username"), "docente_nuevo")

    def test_docente_baja(self):
        """Desactiva (is_active=False) a un docente con confirmación."""
        self.client.force_login(self.directivo)
        self.assertTrue(self.docente.is_active)

        self.client.post(
            reverse("administracion:docente_baja", args=[self.docente.id])
        )

        self.docente.refresh_from_db()
        self.assertFalse(self.docente.is_active)
        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.MODIFICAR,
            modelo="Usuario",
            objeto_id=self.docente.id,
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.detalles.get("is_active"), False)

    # ------------------------------------------------------------------
    # Seguridad
    # ------------------------------------------------------------------
    def test_docente_no_accede(self):
        """El rol docente recibe 403 en la lista de alumnos."""
        self.client.force_login(self.docente)
        response = self.client.get(reverse("administracion:alumnos_lista"))
        self.assertEqual(response.status_code, 403)

    def test_preceptor_no_accede(self):
        """El rol preceptor recibe 403 en la lista de alumnos."""
        self.client.force_login(self.preceptor)
        response = self.client.get(reverse("administracion:alumnos_lista"))
        self.assertEqual(response.status_code, 403)

    def test_anonimo_redirige(self):
        """El usuario anónimo es redirigido a login."""
        response = self.client.get(reverse("administracion:alumnos_lista"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("usuarios:login"), response.url)