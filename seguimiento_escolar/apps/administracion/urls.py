from django.urls import path

from . import views

app_name = "administracion"

urlpatterns = [
    path("", views.index, name="index"),
]