from django.core.exceptions import ValidationError
from django.db import models


class Alumno(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = "activo", "Activo"
        INACTIVO = "inactivo", "Inactivo"
        EGRESADO = "egresado", "Egresado"
        TRASLADADO = "trasladado", "Trasladado"

    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    dni = models.CharField(max_length=20, verbose_name="DNI", blank=True)
    fecha_nacimiento = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de nacimiento",
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.ACTIVO,
        verbose_name="Estado",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"


class AsignacionAlumnoCurso(models.Model):
    class Condicion(models.TextChoices):
        REGULAR = "regular", "Regular"
        REPITENTE = "repitente", "Repitente"
        MOVILIDAD = "movilidad", "Movilidad"

    alumno = models.ForeignKey(
        Alumno,
        on_delete=models.PROTECT,
        related_name="asignaciones_curso",
        verbose_name="Alumno",
    )
    curso = models.ForeignKey(
        "estructura_escolar.Curso",
        on_delete=models.PROTECT,
        related_name="alumnos_asignados",
        verbose_name="Curso",
    )
    ciclo_lectivo = models.ForeignKey(
        "ciclos_lectivos.CicloLectivo",
        on_delete=models.PROTECT,
        related_name="asignaciones_alumnos",
        verbose_name="Ciclo Lectivo",
    )
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")
    fecha_fin = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de fin",
    )
    condicion = models.CharField(
        max_length=20,
        choices=Condicion.choices,
        default=Condicion.REGULAR,
        verbose_name="Condición",
    )
    activa = models.BooleanField(default=True, verbose_name="Activa")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Asignación Alumno-Curso"
        verbose_name_plural = "Asignaciones Alumno-Curso"
        ordering = ["ciclo_lectivo", "curso", "alumno"]
        constraints = [
            models.UniqueConstraint(
                fields=["alumno", "curso", "ciclo_lectivo"],
                name="unica_asignacion_alumno_curso_ciclo",
            )
        ]

    def __str__(self):
        return f"{self.alumno} → {self.curso} ({self.ciclo_lectivo})"

    def clean(self):
        if self.fecha_fin and self.fecha_fin <= self.fecha_inicio:
            raise ValidationError(
                "La fecha de fin debe ser posterior a la fecha de inicio."
            )