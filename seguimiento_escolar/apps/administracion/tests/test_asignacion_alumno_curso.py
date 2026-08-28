from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.alumnos.models import Alumno, AsignacionAlumnoCurso
from apps.auditoria.models import AuditLog
from apps.ciclos_lectivos.models import CicloLectivo
from apps.estructura_escolar.models import Curso, Turno

from ..forms import AsignacionAlumnoCursoForm

User = get_user_model()


class AsignacionAlumnoCursoTests(TestCase):
    """CRUD de AsignacionAlumnoCurso y asignación al crear alumno."""

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
        self.curso = Curso.objects.create(
            anio=1,
            division="A",
            turno=self.turno,
            ciclo_lectivo=self.ciclo,
        )
        self.alumno = Alumno.objects.create(
            nombre="Juan",
            apellido="Pérez",
            dni="30111222",
        )
        self.alumno2 = Alumno.objects.create(
            nombre="Ana",
            apellido="López",
            dni="30111223",
        )
        self.asignacion = AsignacionAlumnoCurso.objects.create(
            alumno=self.alumno,
            curso=self.curso,
            ciclo_lectivo=self.ciclo,
            fecha_inicio="2026-03-02",
            condicion=AsignacionAlumnoCurso.Condicion.REGULAR,
            activa=True,
        )

    def test_asignacion_alumno_crear(self):
        """El directivo crea una asignación con el flujo de 2 pasos."""
        self.client.force_login(self.directivo)

        response = self.client.post(
            reverse("administracion:asignacion_alumno_crear"),
            {
                "alumno": self.alumno2.id,
                "curso": self.curso.id,
                "ciclo_lectivo": self.ciclo.id,
                "fecha_inicio": "2026-03-02",
                "fecha_fin": "",
                "condicion": "regular",
                "activa": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("administracion:asignacion_alumno_confirmar")
        )

        self.client.post(reverse("administracion:asignacion_alumno_confirmar"))

        asignacion = AsignacionAlumnoCurso.objects.get(alumno=self.alumno2)
        self.assertEqual(asignacion.curso, self.curso)
        self.assertEqual(asignacion.ciclo_lectivo, self.ciclo)
        self.assertTrue(asignacion.activa)

    def test_asignacion_alumno_crear_auditada(self):
        """La creación de la asignación queda registrada en AuditLog."""
        self.client.force_login(self.directivo)
        self.client.post(
            reverse("administracion:asignacion_alumno_crear"),
            {
                "alumno": self.alumno2.id,
                "curso": self.curso.id,
                "ciclo_lectivo": self.ciclo.id,
                "fecha_inicio": "2026-03-02",
                "fecha_fin": "",
                "condicion": "repitente",
                "activa": "on",
            },
        )
        self.client.post(reverse("administracion:asignacion_alumno_confirmar"))

        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.CREAR, modelo="AsignacionAlumnoCurso"
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario, self.directivo)

    def test_asignacion_alumno_editar(self):
        """Edita una asignación y registra la acción en AuditLog."""
        self.client.force_login(self.directivo)

        response = self.client.post(
            reverse(
                "administracion:asignacion_alumno_editar",
                args=[self.asignacion.id],
            ),
            {
                "alumno": self.alumno.id,
                "curso": self.curso.id,
                "ciclo_lectivo": self.ciclo.id,
                "fecha_inicio": "2026-03-02",
                "fecha_fin": "2026-07-15",
                "condicion": "movilidad",
                "activa": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("administracion:asignacion_alumno_confirmar_editar"),
        )

        self.client.post(reverse("administracion:asignacion_alumno_confirmar_editar"))

        self.asignacion.refresh_from_db()
        self.assertEqual(
            self.asignacion.condicion, AsignacionAlumnoCurso.Condicion.MOVILIDAD
        )
        self.assertEqual(self.asignacion.fecha_fin.isoformat(), "2026-07-15")
        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.MODIFICAR,
            modelo="AsignacionAlumnoCurso",
            objeto_id=self.asignacion.id,
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario, self.directivo)

    def test_asignacion_alumno_baja(self):
        """Da de baja (activa=False) a una asignación con auditoría."""
        self.client.force_login(self.directivo)

        self.client.post(
            reverse(
                "administracion:asignacion_alumno_baja",
                args=[self.asignacion.id],
            )
        )

        self.asignacion.refresh_from_db()
        self.assertFalse(self.asignacion.activa)
        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.MODIFICAR,
            modelo="AsignacionAlumnoCurso",
            objeto_id=self.asignacion.id,
        ).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.usuario, self.directivo)

    def test_alumno_crear_con_curso(self):
        """Al crear un alumno con curso y ciclo se crea la asignación."""
        self.client.force_login(self.directivo)

        response = self.client.post(
            reverse("administracion:alumno_crear"),
            {
                "nombre": "María",
                "apellido": "Gómez",
                "dni": "40111222",
                "fecha_nacimiento": "2010-05-01",
                "estado": "activo",
                "curso": self.curso.id,
                "ciclo_lectivo": self.ciclo.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("administracion:alumno_confirmar"))

        self.client.post(reverse("administracion:alumno_confirmar"))

        alumno = Alumno.objects.get(dni="40111222")
        asignacion = AsignacionAlumnoCurso.objects.get(alumno=alumno)
        self.assertEqual(asignacion.curso, self.curso)
        self.assertEqual(asignacion.ciclo_lectivo, self.ciclo)
        self.assertEqual(
            asignacion.condicion, AsignacionAlumnoCurso.Condicion.REGULAR
        )
        self.assertTrue(asignacion.activa)
        self.assertEqual(asignacion.fecha_inicio, timezone.localdate())
        # La asignación también queda auditada
        log = AuditLog.objects.filter(
            accion=AuditLog.Accion.CREAR, modelo="AsignacionAlumnoCurso"
        ).first()
        self.assertIsNotNone(log)

    def test_alumno_crear_sin_curso(self):
        """Al crear un alumno sin curso NO se crea asignación."""
        self.client.force_login(self.directivo)
        self.client.post(
            reverse("administracion:alumno_crear"),
            {
                "nombre": "Pedro",
                "apellido": "Díaz",
                "dni": "40111223",
                "fecha_nacimiento": "2010-06-01",
                "estado": "activo",
                "curso": "",
                "ciclo_lectivo": "",
            },
        )
        self.client.post(reverse("administracion:alumno_confirmar"))

        alumno = Alumno.objects.get(dni="40111223")
        self.assertFalse(
            AsignacionAlumnoCurso.objects.filter(alumno=alumno).exists()
        )

    def test_alumno_crear_curso_sin_ciclo_invalido(self):
        """Curso sin ciclo lectivo (o viceversa) invalida el formulario."""
        self.client.force_login(self.directivo)
        response = self.client.post(
            reverse("administracion:alumno_crear"),
            {
                "nombre": "Lucas",
                "apellido": "Ramírez",
                "dni": "40111224",
                "fecha_nacimiento": "2010-07-01",
                "estado": "activo",
                "curso": self.curso.id,
                "ciclo_lectivo": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Alumno.objects.filter(dni="40111224").exists())

    def test_asignacion_alumno_no_duplica_alumno_curso_ciclo(self):
        """No se puede asignar el mismo alumno al mismo curso y ciclo dos veces."""
        form = AsignacionAlumnoCursoForm(
            data={
                "alumno": self.alumno.id,
                "curso": self.curso.id,
                "ciclo_lectivo": self.ciclo.id,
                "fecha_inicio": "2026-03-02",
                "fecha_fin": "",
                "condicion": "regular",
                "activa": True,
            }
        )
        self.assertFalse(form.is_valid())

    def test_lista_muestra_asignaciones(self):
        """El listado muestra las asignaciones existentes."""
        self.client.force_login(self.directivo)
        response = self.client.get(
            reverse("administracion:asignaciones_alumnos_lista")
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pérez, Juan")

    def test_docente_no_accede(self):
        """El rol docente recibe 403 en la lista de asignaciones alumno-curso."""
        self.client.force_login(self.docente)
        response = self.client.get(
            reverse("administracion:asignaciones_alumnos_lista")
        )
        self.assertEqual(response.status_code, 403)

    def test_preceptor_no_accede(self):
        """El rol preceptor recibe 403 en la lista de asignaciones alumno-curso."""
        self.client.force_login(self.preceptor)
        response = self.client.get(
            reverse("administracion:asignaciones_alumnos_lista")
        )
        self.assertEqual(response.status_code, 403)

    def test_anonimo_redirige(self):
        """El usuario anónimo es redirigido a login."""
        response = self.client.get(
            reverse("administracion:asignaciones_alumnos_lista")
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("usuarios:login"), response.url)
