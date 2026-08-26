from django.core.exceptions import ValidationError
from django.db import models


class AuditLog(models.Model):
    class Accion(models.TextChoices):
        CREAR = "crear", "Crear"
        MODIFICAR = "modificar", "Modificar"
        ELIMINAR = "eliminar", "Eliminar"
        ANULAR = "anular", "Anular"
        LOGIN = "login", "Inicio de sesión"
        LOGOUT = "logout", "Cierre de sesión"
        SOLICITAR = "solicitar", "Solicitar"
        RESPONDER = "responder", "Responder"

    usuario = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="auditoria",
        verbose_name="Usuario",
    )
    accion = models.CharField(
        max_length=20,
        choices=Accion.choices,
        verbose_name="Acción",
    )
    modelo = models.CharField(
        max_length=100,
        verbose_name="Modelo",
        help_text="Nombre del modelo afectado",
    )
    objeto_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="ID del objeto",
    )
    detalles = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Detalles",
        help_text="Datos adicionales en formato JSON",
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Dirección IP",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha y hora",
    )

    class Meta:
        verbose_name = "Registro de Auditoría"
        verbose_name_plural = "Registros de Auditoría"
        ordering = ["-timestamp"]

    def __str__(self):
        return (
            f"{self.usuario} — {self.accion} {self.modelo} "
            f"({self.timestamp:%d/%m/%Y %H:%M})"
        )

    def save(self, *args, **kwargs):
        # INMUTABLE: solo permite creación
        if self.pk:
            raise ValidationError("Los registros de auditoría son inmutables.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # INMUTABLE: no permite eliminación
        raise ValidationError("Los registros de auditoría no se pueden eliminar.")