"""
Configuración de URLs del proyecto Sistema de Seguimiento Escolar — ES63.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.usuarios.urls', namespace='usuarios')),
    path('observaciones/', include('apps.observaciones.urls', namespace='observaciones')),
    path('seguimiento/', include('apps.seguimiento.urls', namespace='seguimiento')),
    path('administracion/', include('apps.administracion.urls', namespace='administracion')),
]
