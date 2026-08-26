from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.alumnos.models import Alumno, AsignacionAlumnoCurso
from apps.ciclos_lectivos.models import CicloLectivo
from apps.estructura_escolar.models import AsignacionDocente, Curso, Materia, Turno

from ..models import Intervencion, SolicitudInfo


class SolicitudesIntervencionesTests(TestCase):
    def setUp(self):
        User = get_user_model()
        # Usuarios
        self.docente = User.objects.create_user(
            username="docente1",
            password="pass12345",
            rol=User.Rol.DOCENTE,
        )
        self.directivo = User.objects.create_user(
            username="directivo1",
            password="pass12345",
            rol=User.Rol.DIRECTIVO,
        )
        # Estructura
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
        self.asignacion = AsignacionDocente.objects.create(
            docente=self.docente,
            materia=self.materia,
            curso=self.curso,
            fecha_inicio=date(2026, 3, 2),
            activa=True,
        )
        # Alumno
        self.alumno = Alumno.objects.create(
            nombre="Juan", apellido="Pérez", dni="30111222"
        )
        AsignacionAlumnoCurso.objects.create(
            alumno=self.alumno,
            curso=self.curso,
            ciclo_lectivo=self.ciclo,
            fecha_inicio=date(2026, 3, 2),
        )

    def test_docente_puede_solicitar(self):
        """El docente crea una solicitud de información."""
        self.client.force_login(self.docente)
        response = self.client.post(
            reverse("seguimiento:solicitar_info"),
            {"alumno": self.alumno.id, "motivo": "Necesito información"},
        )
        self.assertEqual(response.status_code, 302)
        solicitud = SolicitudInfo.objects.get(alumno=self.alumno)
        self.assertEqual(solicitud.solicitante, self.docente)
        self.assertEqual(solicitud.motivo, "Necesito información")

    def test_solicitud_estado_inicial(self):
        """La solicitud se crea con estado 'pendiente'."""
        self.client.force_login(self.docente)
        self.client.post(
            reverse("seguimiento:solicitar_info"),
            {"alumno": self.alumno.id, "motivo": "Motivo de prueba"},
        )
        solicitud = SolicitudInfo.objects.get(alumno=self.alumno)
        self.assertEqual(solicitud.estado, SolicitudInfo.Estado.PENDIENTE)

    def test_directivo_lista_solicitudes(self):
        """El directivo ve todas las solicitudes."""
        # Crear una solicitud
        SolicitudInfo.objects.create(
            alumno=self.alumno,
            solicitante=self.docente,
            motivo="Motivo de prueba",
        )
        self.client.force_login(self.directivo)
        response = self.client.get(reverse("seguimiento:lista_solicitudes"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pérez, Juan")

    def test_docente_no_ve_solicitudes(self):
        """El docente no accede a la lista de solicitudes (403)."""
        self.client.force_login(self.docente)
        response = self.client.get(reverse("seguimiento:lista_solicitudes"))
        self.assertEqual(response.status_code, 403)

    def test_directivo_responde(self):
        """El directivo responde y se registra quién/cuándo."""
        solicitud = SolicitudInfo.objects.create(
            alumno=self.alumno,
            solicitante=self.docente,
            motivo="Motivo de prueba",
        )
        self.client.force_login(self.directivo)
        response = self.client.post(
            reverse("seguimiento:responder_solicitud", args=[solicitud.id]),
            {
                "estado": SolicitudInfo.Estado.RESPONDIDA,
                "respuesta": "La información está disponible",
            },
        )
        self.assertEqual(response.status_code, 302)
        solicitud.refresh_from_db()
        self.assertEqual(solicitud.estado, SolicitudInfo.Estado.RESPONDIDA)
        self.assertEqual(solicitud.respondido_por, self.directivo)
        self.assertIsNotNone(solicitud.fecha_respuesta)
        self.assertEqual(
            solicitud.respuesta, "La información está disponible"
        )

    def test_directivo_registra_intervencion(self):
        """El directivo registra una intervención."""
        self.client.force_login(self.directivo)
        response = self.client.post(
            reverse("seguimiento:registrar_intervencion", args=[self.alumno.id]),
            {
                "tipo": Intervencion.Tipo.ENTREVISTA,
                "descripcion": "Reunión con la familia",
            },
        )
        self.assertEqual(response.status_code, 302)
        intervencion = Intervencion.objects.get(alumno=self.alumno)
        self.assertEqual(intervencion.responsable, self.directivo)
        self.assertEqual(intervencion.tipo, Intervencion.Tipo.ENTREVISTA)

    def test_docente_no_registra_intervencion(self):
        """El docente no puede registrar intervenciones (403)."""
        self.client.force_login(self.docente)
        response = self.client.post(
            reverse("seguimiento:registrar_intervencion", args=[self.alumno.id]),
            {
                "tipo": Intervencion.Tipo.ENTREVISTA,
                "descripcion": "Reunión con la familia",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Intervencion.objects.count(), 0)

    def test_intervencion_visible_en_ficha(self):
        """Las intervenciones aparecen en la ficha del alumno."""
        Intervencion.objects.create(
            alumno=self.alumno,
            responsable=self.directivo,
            tipo=Intervencion.Tipo.ENTREVISTA,
            descripcion="Reunión con la familia",
        )
        self.client.force_login(self.directivo)
        response = self.client.get(
            reverse("seguimiento:ficha_alumno", args=[self.alumno.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reunión con la familia")
        self.assertContains(response, "Entrevista")

    def test_anonimo_redirige(self):
        """El usuario anónimo es redirigido a login."""
        response = self.client.get(reverse("seguimiento:lista_solicitudes"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("usuarios:login"), response.url)

    def test_docente_no_crea_solicitud_de_alumno_ajeno(self):
        """El docente solo puede solicitar de alumnos de sus cursos."""
        # Alumno en curso ajeno
        otro_curso = Curso.objects.create(
            anio=4,
            division="A",
            turno=self.turno_manana,
            ciclo_lectivo=self.ciclo,
        )
        alumno_ajeno = Alumno.objects.create(
            nombre="Ana", apellido="López", dni="30111223"
        )
        AsignacionAlumnoCurso.objects.create(
            alumno=alumno_ajeno,
            curso=otro_curso,
            ciclo_lectivo=self.ciclo,
            fecha_inicio=date(2026, 3, 2),
        )
        self.client.force_login(self.docente)
        response = self.client.get(reverse("seguimiento:solicitar_info"))
        self.assertEqual(response.status_code, 200)
        # El alumnno ajeno no aparece en el select
        self.assertNotContains(response, "López, Ana")
        # El alumno propio sí
        self.assertContains(response, "Pérez, Juan")