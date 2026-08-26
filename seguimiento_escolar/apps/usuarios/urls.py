from django.urls import path

from . import views

app_name = "usuarios"

urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("", views.Home.as_view(), name="home"),
    # Homes por rol (placeholder Fase 6)
    path("docente/", views.home_docente, name="home_docente"),
    path("preceptor/", views.home_preceptor, name="home_preceptor"),
    path("directivo/", views.home_directivo, name="home_directivo"),
]