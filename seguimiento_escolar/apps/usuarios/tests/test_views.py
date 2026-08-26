from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.urls import reverse

from ..decorators import admin_requerido, docente_requerido


@docente_requerido
def vista_docente(request):
    return HttpResponse("ok docente")


@admin_requerido
def vista_admin(request):
    return HttpResponse("ok admin")


class LoginLogoutTests(TestCase):
    def setUp(self):
        User = get_user_model()
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
        self.directivo = User.objects.create_user(
            username="directivo1",
            password="pass12345",
            rol=User.Rol.DIRECTIVO,
        )

    def test_login_get(self):
        """GET /login/ retorna 200."""
        response = self.client.get(reverse("usuarios:login"))
        self.assertEqual(response.status_code, 200)

    def test_login_post_valido(self):
        """POST con credenciales válidas redirige."""
        response = self.client.post(
            reverse("usuarios:login"),
            {"username": "admin1", "password": "pass12345"},
        )
        self.assertEqual(response.status_code, 302)

    def test_login_post_invalido(self):
        """POST con credenciales inválidas muestra error."""
        response = self.client.post(
            reverse("usuarios:login"),
            {"username": "admin1", "password": "incorrecta"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "incorrectos")

    def test_logout(self):
        """POST /logout/ cierra sesión y redirige."""
        self.client.login(username="admin1", password="pass12345")
        response = self.client.post(reverse("usuarios:logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("usuarios:login"))

    def test_home_requiere_login(self):
        """GET / sin login redirige a /login/."""
        response = self.client.get(reverse("usuarios:home"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("usuarios:login"), response.url)


class DecoradoresTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.factory = RequestFactory()
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
        self.admin = User.objects.create_user(
            username="admin1",
            password="pass12345",
            rol=User.Rol.ADMIN,
        )

    def test_decorador_docente(self):
        """El docente puede acceder a la vista docente."""
        request = self.factory.get("/")
        request.user = self.docente
        response = vista_docente(request)
        self.assertEqual(response.status_code, 200)

    def test_decorador_docente_deniega_directivo(self):
        """El directivo NO puede acceder a la vista docente."""
        request = self.factory.get("/")
        request.user = self.directivo
        with self.assertRaises(PermissionDenied):
            vista_docente(request)

    def test_decorador_admin(self):
        """Solo el admin puede acceder a la vista admin."""
        request = self.factory.get("/")
        request.user = self.admin
        response = vista_admin(request)
        self.assertEqual(response.status_code, 200)

        request2 = self.factory.get("/")
        request2.user = self.docente
        with self.assertRaises(PermissionDenied):
            vista_admin(request2)

    def test_decorador_deniega_anonimo(self):
        """El usuario anónimo es redirigido (login_required)."""
        # RequestFactory sin user autenticado → LoginRequired redirige
        # Simulamos con un usuario AnonymousUser
        from django.contrib.auth.models import AnonymousUser

        request = self.factory.get("/")
        request.user = AnonymousUser()
        response = vista_docente(request)
        # login_required redirige a LOGIN_URL
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("usuarios:login"), response.url)