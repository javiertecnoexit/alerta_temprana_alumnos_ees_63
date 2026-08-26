from django.contrib import admin

from .models import AuditLog

CAMPO_READONLY = (
    "usuario",
    "accion",
    "modelo",
    "objeto_id",
    "detalles",
    "ip_address",
    "timestamp",
)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "usuario", "accion", "modelo", "objeto_id", "ip_address")
    list_filter = ("accion", "modelo")
    search_fields = ("usuario__username", "modelo")

    # Todos los campos readonly (los registros de auditoría son inmutables)
    readonly_fields = CAMPO_READONLY

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        # Permite ver el detalle (change view) pero no editar campos
        return True