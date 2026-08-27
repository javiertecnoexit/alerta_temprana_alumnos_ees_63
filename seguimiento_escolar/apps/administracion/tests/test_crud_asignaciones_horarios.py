from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.auditoria.models import AuditLog
from apps.ciclos_lectivos.models import CicloLectivo
from apps.estructura_escolar.models import (
    AsignacionDocente,
    Curso,
    Horario,
    Materia,
    Turno,
)

User = get_user_model()


class CrudAsignacionesHorariosTests(TestCase):
    """CRUD de AsignacionDocente y Horario con confirmación y auditoría."""

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
        self.docente2 = User.objects.create_user(
            username="docente2",
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
        self.curso = Curso.objects.create(
            anio=1,
            division="A",
            turno=self.turno,
            ciclo_lectivo=self.ciclo,
        )
        self.asignacion = AsignacionDocente.objects.create(
            docente=self.docente,
            materia=self.materia,
            curso=self.curso,
            tipo=AsignacionDocente.Tipo.TITULAR,
            fecha_inicio="2026-03-02",
        )

    def test_asignacion_crear_auditada(self):
        """Crea una asignación con flujo de 2 pasos y registra AuditLog."""
        self.client.force_login(self.directivo)

        response = self.client.post(
            reverse("administracion:asignacion_crear"),
            {
                "docente": self.docente2.id,
                "materia": self.materia.id,
                "curso": self.curso.id,
                "tipo": "suplente",
                "fecha_inicio": "2026-04-01",
                "fecha_fin": "",
                "activa": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("administracion:asignacion_confirmar")
        )

        self.client.post(reverse("administracion:asignacion_confirmar"))

        asignacion = AsignacionDocente.objects.get(docente=self.docente2)
        self.assertEqual(asignacion.tipo, AsignacionDocente.Tipo.SUPLENTE)
        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.CREAR, modelo="AsignacionDocente"
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario, self.directivo)

    def test_asignacion_editar(self):
        """Edita una asignación y registra la acción en AuditLog."""
        self.client.force_login(self.directivo)

        response = self.client.post(
            reverse("administracion:asignacion_editar", args=[self.asignacion.id]),
            {
                "docente": self.docente.id,
                "materia": self.materia.id,
                "curso": self.curso.id,
                "tipo": "reemplazo",
                "fecha_inicio": "2026-03-02",
                "fecha_fin": "2026-07-01",
                "activa": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("administracion:asignacion_confirmar_editar")
        )

        self.client.post(reverse("administracion:asignacion_confirmar_editar"))

        self.asignacion.refresh_from_db()
        self.assertEqual(self.asignacion.tipo, AsignacionDocente.Tipo.REEMPLAZO)
        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.MODIFICAR,
            modelo="AsignacionDocente",
            objeto_id=self.asignacion.id,
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario, self.directivo)

    def test_asignacion_baja(self):
        """Da de baja (activa=False) a una asignación + AuditLog."""
        self.client.force_login(self.directivo)
        self.assertTrue(self.asignacion.activa)

        self.client.post(
            reverse("administracion:asignacion_baja", args=[self.asignacion.id])
        )

        self.asignacion.refresh_from_db()
        self.assertFalse(self.asignacion.activa)
        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.MODIFICAR,
            modelo="AsignacionDocente",
            objeto_id=self.asignacion.id,
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.detalles.get("activa"), False)

    def test_horario_crear_auditado(self):
        """Crea un horario con flujo de 2 pasos y registra AuditLog."""
        self.client.force_login(self.directivo)

        response = self.client.post(
            reverse("administracion:horario_crear"),
            {
                "asignacion_docente": self.asignacion.id,
                "dia_semana": "lunes",
                "hora_inicio": "08:00",
                "hora_fin": "09:00",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("administracion:horario_confirmar"))

        self.client.post(reverse("administracion:horario_confirmar"))

        horario = Horario.objects.get(asignacion_docente=self.asignacion)
        self.assertEqual(horario.dia_semana, Horario.DiaSemana.LUNES)
        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.CREAR, modelo="Horario"
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario, self.directivo)

    def test_horario_editar(self):
        """Edita un horario y registra la acción en AuditLog."""
        horario = Horario.objects.create(
            asignacion_docente=self.asignacion,
            dia_semana=Horario.DiaSemana.LUNES,
            hora_inicio="08:00",
            hora_fin="09:00",
        )
        self.client.force_login(self.directivo)

        response = self.client.post(
            reverse("administracion:horario_editar", args=[horario.id]),
            {
                "asignacion_docente": self.asignacion.id,
                "dia_semana": "martes",
                "hora_inicio": "10:00",
                "hora_fin": "11:00",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("administracion:horario_confirmar_editar")
        )

        self.client.post(reverse("administracion:horario_confirmar_editar"))

        horario.refresh_from_db()
        self.assertEqual(horario.dia_semana, Horario.DiaSemana.MARTES)
        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.MODIFICAR,
            modelo="Horario",
            objeto_id=horario.id,
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario, self.directivo)

    def test_horario_eliminar(self):
        """Elimina físicamente un horario con auditoría accion='eliminar'."""
        horario = Horario.objects.create(
            asignacion_docente=self.asignacion,
            dia_semana=Horario.DiaSemana.VIERNES,
            hora_inicio="09:00",
            hora_fin="10:00",
        )
        self.client.force_login(self.directivo)

        self.client.post(
            reverse("administracion:horario_eliminar", args=[horario.id])
        )

        self.assertFalse(Horario.objects.filter(pk=horario.id).exists())
        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.ELIMINAR,
            modelo="Horario",
            objeto_id=horario.id,
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario, self.directivo)

    def test_docente_no_accede(self):
        """El rol docente recibe 403 en la lista de asignaciones."""
        self.client.force_login(self.docente)
        response = self.client.get(reverse("administracion:asignaciones_lista"))
        self.assertEqual(response.status_code, 403)

    def test_preceptor_no_accede(self):
        """El rol preceptor recibe 403 en la lista de asignaciones."""
        self.client.force_login(self.preceptor)
        response = self.client.get(reverse("administracion:asignaciones_lista"))
        self.assertEqual(response.status_code, 403)

    def test_anonimo_redirige(self):
        """El usuario anónimo es redirigido a login."""
        response = self.client.get(reverse("administracion:asignaciones_lista"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("usuarios:login"), response.url)