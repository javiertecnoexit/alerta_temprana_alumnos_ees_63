from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class Login(LoginView):
    template_name = "usuarios/login.html"
    redirect_authenticated_user = True


class Logout(LogoutView):
    next_page = reverse_lazy("usuarios:login")


class Home(LoginRequiredMixin, TemplateView):
    template_name = "base.html"

    def dispatch(self, request, *args, **kwargs):
        # Si el usuario no está autenticado, LoginRequiredMixin redirige a login
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        # Redirigir según el rol
        user = request.user
        if user.es_docente:
            return redirect("usuarios:home_docente")
        elif user.es_preceptor:
            return redirect("usuarios:home_preceptor")
        elif user.es_directivo:
            return redirect("usuarios:home_directivo")
        elif user.es_admin:
            return redirect("usuarios:home_admin")
        return super().dispatch(request, *args, **kwargs)


class EnConstruccion(LoginRequiredMixin, TemplateView):
    """Vista simple 'en construcción' para los homes por rol (Fase 6)."""

    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mensaje"] = (
            "Esta sección está en construcción. "
            "Estará disponible en una próxima fase."
        )
        return context


def home_docente_redirect(request):
    """Home del docente: redirige al dashboard de observaciones."""
    return redirect("observaciones:lista_cursos")


def home_directivo_redirect(request):
    """Home del directivo: redirige al buscador de alumnos."""
    return redirect("seguimiento:buscar_alumnos")


def home_preceptor_redirect(request):
    """Home del preceptor: redirige a los alumnos de su turno."""
    return redirect("seguimiento:preceptor_alumnos")


def home_admin_redirect(request):
    """Home del admin: redirige al panel de administración."""
    return redirect("administracion:index")


home_docente = home_docente_redirect
home_preceptor = home_preceptor_redirect
home_directivo = home_directivo_redirect
home_admin = home_admin_redirect
