from django.db import models


class PreceptorTurno(models.Model):
    """
    Vincula a un usuario con rol preceptor con el turno de su ámbito.

    Permite que el preceptor vea solo los alumnos de su turno sin
    modificar el modelo Usuario existente.
    """

    preceptor = models.OneToOneField(
        "usuarios.Usuario",
        on_delete=models.CASCADE,
        related_name="preceptor_turno",
        verbose_name="Preceptor",
    )
    turno = models.ForeignKey(
        "estructura_escolar.Turno",
        on_delete=models.PROTECT,
        related_name="preceptores",
        verbose_name="Turno",
    )

    class Meta:
        verbose_name = "Preceptor - Turno"
        verbose_name_plural = "Preceptores - Turnos"

    def __str__(self):
        return f"{self.preceptor} — {self.turno}"


class SolicitudInfo(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        RESPONDIDA = "respondida", "Respondida"
        RECHAZADA = "rechazada", "Rechazada"

    alumno = models.ForeignKey(
        "alumnos.Alumno",
        on_delete=models.PROTECT,
        related_name="solicitudes_info",
        verbose_name="Alumno",
    )
    solicitante = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.PROTECT,
        related_name="solicitudes_realizadas",
        verbose_name="Solicitante",
    )
    motivo = models.TextField(verbose_name="Motivo")
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
        verbose_name="Estado",
    )
    respuesta = models.TextField(blank=True, verbose_name="Respuesta")
    respondido_por = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="solicitudes_respondidas",
        verbose_name="Respondido por",
    )
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Solicitud de Información"
        verbose_name_plural = "Solicitudes de Información"
        ordering = ["-fecha_solicitud"]

    def __str__(self):
        return (
            f"{self.solicitante} → {self.alumno} "
            f"({self.get_estado_display()})"
        )


class Intervencion(models.Model):
    class Tipo(models.TextChoices):
        ENTREVISTA = "entrevista", "Entrevista"
        CONTACTO_FAMILIA = "contacto_familia", "Contacto con familia/tutor"
        SEGUIMIENTO = "seguimiento", "Seguimiento pedagógico"
        DERIVACION = "derivacion", "Derivación institucional"
        ACOMPANAMIENTO = "acompanamiento", "Acompañamiento"
        ACTIVIDAD_ESPECIAL = (
            "actividad_especial",
            "Propuesta de actividad especial",
        )
        OPORTUNIDAD = "oportunidad", "Acceso a proyecto/beca/oportunidad"
        CIERRE = "cierre", "Cierre de seguimiento"
        OTRA = "otra", "Otra"

    alumno = models.ForeignKey(
        "alumnos.Alumno",
        on_delete=models.PROTECT,
        related_name="intervenciones",
        verbose_name="Alumno",
    )
    responsable = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.PROTECT,
        related_name="intervenciones_realizadas",
        verbose_name="Responsable",
    )
    tipo = models.CharField(
        max_length=30,
        choices=Tipo.choices,
        verbose_name="Tipo",
    )
    descripcion = models.TextField(verbose_name="Descripción")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")

    class Meta:
        verbose_name = "Intervención"
        verbose_name_plural = "Intervenciones"
        ordering = ["-fecha"]

    def __str__(self):
        return (
            f"{self.alumno} — {self.get_tipo_display()} "
            f"({self.fecha:%d/%m/%Y})"
        )
