from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.auditoria.models import AuditLog
from apps.ciclos_lectivos.models import CicloLectivo
from apps.estructura_escolar.models import Curso, Materia, Turno

User = get_user_model()


class CrudEstructuraTests(TestCase):
    """CRUD de Materia, Turno, Curso y CicloLectivo con confirmación y auditoría."""

    def setUp(self):
        self.directivo = User.objects.create_user(
            username="directivo1",
            password="pass12345",
            rol=User.Rol.DIRECTIVO,
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
        self.turno = Turno.objects.create(nombre=Turno.Nombre.MANANA)
        self.ciclo = CicloLectivo.objects.create(
            anio=2026,
            fecha_inicio="2026-03-02",
            fecha_fin="2026-12-18",
            estado=CicloLectivo.Estado.ACTIVO,
        )
        self.materia = Materia.objects.create(nombre="Matemática")

    # ------------------------------------------------------------------
    # Creaciones
    # ------------------------------------------------------------------
    def test_materia_crear_auditada(self):
        """Crea una materia con flujo de 2 pasos y registra AuditLog."""
        self.client.force_login(self.directivo)

        response = self.client.post(reverse("administracion:materia_crear"), {
            "nombre": "Lengua",
            "activa": "on",
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("administracion:materia_confirmar"))

        self.client.post(reverse("administracion:materia_confirmar"))

        materia = Materia.objects.get(nombre="Lengua")
        self.assertTrue(materia.activa)
        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.CREAR, modelo="Materia"
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario, self.directivo)
        self.assertEqual(log.detalles.get("nombre"), "Lengua")

    def test_turno_crear_auditado(self):
        """Crea un turno con flujo de 2 pasos y registra AuditLog."""
        self.client.force_login(self.directivo)

        response = self.client.post(reverse("administracion:turno_crear"), {
            "nombre": "tarde",
            "activo": "on",
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("administracion:turno_confirmar"))

        self.client.post(reverse("administracion:turno_confirmar"))

        turno = Turno.objects.get(nombre=Turno.Nombre.TARDE)
        self.assertTrue(turno.activo)
        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.CREAR, modelo="Turno"
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario, self.directivo)

    def test_curso_crear_auditado(self):
        """Crea un curso con turno y ciclo lectivo + AuditLog."""
        self.client.force_login(self.directivo)

        response = self.client.post(reverse("administracion:curso_crear"), {
            "anio": "1",
            "division": "A",
            "turno": self.turno.id,
            "ciclo_lectivo": self.ciclo.id,
            "activo": "on",
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("administracion:curso_confirmar"))

        self.client.post(reverse("administracion:curso_confirmar"))

        curso = Curso.objects.get(anio=1, division="A")
        self.assertEqual(curso.turno, self.turno)
        self.assertEqual(curso.ciclo_lectivo, self.ciclo)
        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.CREAR, modelo="Curso"
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario, self.directivo)

    def test_ciclo_crear_auditado(self):
        """Crea un ciclo lectivo con fechas válidas + AuditLog."""
        self.client.force_login(self.directivo)

        response = self.client.post(reverse("administracion:ciclo_crear"), {
            "anio": "2027",
            "fecha_inicio": "2027-03-01",
            "fecha_fin": "2027-12-17",
            "estado": "planificado",
            "activo": "on",
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("administracion:ciclo_confirmar"))

        self.client.post(reverse("administracion:ciclo_confirmar"))

        ciclo = CicloLectivo.objects.get(anio=2027)
        self.assertEqual(ciclo.estado, CicloLectivo.Estado.PLANIFICADO)
        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.CREAR, modelo="CicloLectivo"
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario, self.directivo)
        self.assertEqual(log.detalles.get("anio"), 2027)

    # ------------------------------------------------------------------
    # Ediciones
    # ------------------------------------------------------------------
    def test_materia_editar(self):
        """Edita una materia y registra la acción en AuditLog."""
        self.client.force_login(self.directivo)

        response = self.client.post(
            reverse("administracion:materia_editar", args=[self.materia.id]),
            {
                "nombre": "Matemática 2",
                "activa": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("administracion:materia_confirmar_editar"))

        self.client.post(reverse("administracion:materia_confirmar_editar"))

        self.materia.refresh_from_db()
        self.assertEqual(self.materia.nombre, "Matemática 2")
        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.MODIFICAR,
            modelo="Materia",
            objeto_id=self.materia.id,
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario, self.directivo)

    def test_curso_editar(self):
        """Edita un curso y registra la acción en AuditLog."""
        curso = Curso.objects.create(
            anio=2,
            division="B",
            turno=self.turno,
            ciclo_lectivo=self.ciclo,
        )
        self.client.force_login(self.directivo)

        response = self.client.post(
            reverse("administracion:curso_editar", args=[curso.id]),
            {
                "anio": "2",
                "division": "C",
                "turno": self.turno.id,
                "ciclo_lectivo": self.ciclo.id,
                "activo": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("administracion:curso_confirmar_editar"))

        self.client.post(reverse("administracion:curso_confirmar_editar"))

        curso.refresh_from_db()
        self.assertEqual(curso.division, "C")
        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.MODIFICAR,
            modelo="Curso",
            objeto_id=curso.id,
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario, self.directivo)

    # ------------------------------------------------------------------
    # Bajas
    # ------------------------------------------------------------------
    def test_materia_baja(self):
        """Da de baja (activa=False) a una materia + AuditLog."""
        self.client.force_login(self.directivo)
        self.assertTrue(self.materia.activa)

        self.client.post(
            reverse("administracion:materia_baja", args=[self.materia.id])
        )

        self.materia.refresh_from_db()
        self.assertFalse(self.materia.activa)
        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.MODIFICAR,
            modelo="Materia",
            objeto_id=self.materia.id,
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.detalles.get("activa"), False)

    # ------------------------------------------------------------------
    # Seguridad
    # ------------------------------------------------------------------
    def test_docente_no_accede(self):
        """El rol docente recibe 403 en la lista de materias."""
        self.client.force_login(self.docente)
        response = self.client.get(reverse("administracion:materias_lista"))
        self.assertEqual(response.status_code, 403)

    def test_preceptor_no_accede(self):
        """El rol preceptor recibe 403 en la lista de materias."""
        self.client.force_login(self.preceptor)
        response = self.client.get(reverse("administracion:materias_lista"))
        self.assertEqual(response.status_code, 403)

    def test_anonimo_redirige(self):
        """El usuario anónimo es redirigido a login."""
        response = self.client.get(reverse("administracion:materias_lista"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("usuarios:login"), response.url)