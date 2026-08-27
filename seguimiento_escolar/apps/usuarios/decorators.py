from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def rol_requerido(*roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.rol in roles or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator


docente_requerido = rol_requerido("docente")
preceptor_requerido = rol_requerido("preceptor")
directivo_requerido = rol_requerido("directivo")
admin_requerido = rol_requerido("admin")
directivo_o_preceptor = rol_requerido("directivo", "preceptor")
directivo_o_admin = rol_requerido("directivo", "admin")
