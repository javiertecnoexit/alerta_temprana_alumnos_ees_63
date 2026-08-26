from django.core.exceptions import ValidationError
from django.db import models


class CicloLectivo(models.Model):
    class Estado(models.TextChoices):
        PLANIFICADO = "planificado", "Planificado"
        ACTIVO = "activo", "Activo"
        CERRADO = "cerrado", "Cerrado"

    anio = models.PositiveIntegerField(
        verbose_name="Año",
        help_text="Año del ciclo lectivo (ej: 2026)",
    )
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de fin")
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PLANIFICADO,
        verbose_name="Estado",
    )
    activo = models.BooleanField(
        default=True,
        help_text="Indica si este ciclo está disponible para uso",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ciclo Lectivo"
        verbose_name_plural = "Ciclos Lectivos"
        ordering = ["-anio"]
        constraints = [
            models.UniqueConstraint(
                fields=["anio"],
                condition=models.Q(activo=True),
                name="unico_ciclo_activo_por_anio",
            )
        ]

    def __str__(self):
        return f"Ciclo {self.anio} ({self.get_estado_display()})"

    def clean(self):
        # Validación de coherencia de fechas
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_inicio >= self.fecha_fin:
                raise ValidationError(
                    "La fecha de inicio debe ser anterior a la fecha de fin."
                )

        # Regla de negocio: un ciclo cerrado no se reabre
        if self.pk:
            estado_anterior = CicloLectivo.objects.get(pk=self.pk).estado
            if (
                estado_anterior == self.Estado.CERRADO
                and self.estado != self.Estado.CERRADO
            ):
                raise ValidationError(
                    {"estado": "Un ciclo cerrado no se puede reabrir."}
                )