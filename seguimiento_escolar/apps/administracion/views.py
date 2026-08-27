from django.shortcuts import render

from apps.usuarios.decorators import directivo_o_admin


@directivo_o_admin
def index(request):
    """Panel índice de gestión de datos (directivo y admin)."""
    return render(request, "administracion/index.html")