from apps.auditoria.models import AuditLog


def registrar_auditoria(usuario, accion, modelo, objeto_id=None,
                        detalles=None, request=None):
    """
    Crea un registro inmutable de auditoría.
    accion: 'crear' | 'modificar' | 'eliminar'
    modelo: nombre del modelo (ej. 'Alumno')
    objeto_id: id del objeto afectado (opcional)
    detalles: dict con datos adicionales (opcional)
    request: para capturar IP (opcional)
    """
    ip = None
    if request:
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            ip = xff.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")

    return AuditLog.objects.create(
        usuario=usuario,
        accion=accion,
        modelo=modelo,
        objeto_id=objeto_id,
        detalles=detalles or {},
        ip_address=ip,
    )