from django.core.exceptions import ValidationError
from django.db import models


class CatalogoObservacion(models.Model):
    class Familia(models.TextChoices):
        PARTICIPACION = "participacion", "Participación"
        TRABAJO_ACADEMICO = "trabajo_academico", "Trabajo académico"
        ATENCION = "atencion", "Atención"
        CONVIVENCIA = "convivencia", "Convivencia"
        ESTADO_OBSERVABLE = "estado_observable", "Estado observable"
        EVOLUCION_POSITIVA = "evolucion_positiva", "Evolución positiva"
        OTRA = "otra", "Otra situación"

    class Caracter(models.TextChoices):
        POSITIVO = "positivo", "Positivo"
        NEUTRO = "neutro", "Neutro"
        ATENCION = "atencion", "Atención"

    nombre = models.CharField(max_length=150, verbose_name="Nombre")
    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción",
        help_text="Definición y criterio de uso para reducir interpretaciones",
    )
    familia = models.CharField(
        max_length=30,
        choices=Familia.choices,
        verbose_name="Familia",
    )
    caracter = models.CharField(
        max_length=20,
        choices=Caracter.choices,
        default=Caracter.NEUTRO,
        verbose_name="Carácter",
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    version = models.PositiveIntegerField(default=1, verbose_name="Versión")
    creado_por = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="catalogo_creado",
        verbose_name="Creado por",
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Catálogo de Observación"
        verbose_name_plural = "Catálogo de Observaciones"
        ordering = ["familia", "nombre"]
        constraints = [
            models.UniqueConstraint(
                fields=["nombre", "version"],
                name="unico_nombre_version_catalogo",
            )
        ]

    def __str__(self):
        return f"{self.nombre} (v{self.version})"


class Observacion(models.Model):
    alumno = models.ForeignKey(
        "alumnos.Alumno",
        on_delete=models.PROTECT,
        related_name="observaciones",
        verbose_name="Alumno",
    )
    docente = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.PROTECT,
        related_name="observaciones_realizadas",
        verbose_name="Docente",
    )
    materia = models.ForeignKey(
        "estructura_escolar.Materia",
        on_delete=models.PROTECT,
        related_name="observaciones",
        verbose_name="Materia",
        null=True,
        blank=True,
        help_text="Opcional para observaciones de preceptoría",
    )
    curso = models.ForeignKey(
        "estructura_escolar.Curso",
        on_delete=models.PROTECT,
        related_name="observaciones",
        verbose_name="Curso",
    )
    catalogo = models.ForeignKey(
        CatalogoObservacion,
        on_delete=models.PROTECT,
        related_name="observaciones",
        verbose_name="Categoría",
    )
    ciclo_lectivo = models.ForeignKey(
        "ciclos_lectivos.CicloLectivo",
        on_delete=models.PROTECT,
        related_name="observaciones",
        verbose_name="Ciclo Lectivo",
    )
    fecha_hora = models.DateTimeField(
        verbose_name="Fecha y hora",
        help_text="Momento del hecho observado",
    )
    turno = models.CharField(
        max_length=20,
        choices=[("manana", "Mañana"), ("tarde", "Tarde")],
        verbose_name="Turno",
    )
    comentario = models.TextField(
        blank=True,
        verbose_name="Comentario",
        help_text="Comentario opcional con contexto adicional",
    )
    dentro_horario = models.BooleanField(
        default=False,
        verbose_name="Dentro del horario de clase",
    )
    anulada = models.BooleanField(default=False, verbose_name="Anulada")
    motivo_anulacion = models.TextField(
        blank=True,
        verbose_name="Motivo de anulación",
    )
    anulada_por = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="observaciones_anuladas",
        verbose_name="Anulada por",
    )
    fecha_anulacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de anulación",
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Observación"
        verbose_name_plural = "Observaciones"
        ordering = ["-fecha_hora"]

    def __str__(self):
        return (
            f"{self.alumno} — {self.catalogo.nombre} "
            f"({self.fecha_hora:%d/%m/%Y})"
        )

    def clean(self):
        if self.anulada and not self.motivo_anulacion:
            raise ValidationError("Toda anulación requiere un motivo.")

    @property
    def vigente(self):
        return not self.anulada