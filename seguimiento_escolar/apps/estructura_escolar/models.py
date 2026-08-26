from django.core.exceptions import ValidationError
from django.db import models


class Turno(models.Model):
    class Nombre(models.TextChoices):
        MANANA = "manana", "Mañana"
        TARDE = "tarde", "Tarde"

    nombre = models.CharField(
        max_length=20,
        choices=Nombre.choices,
        unique=True,
        verbose_name="Nombre",
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"
        ordering = ["nombre"]

    def __str__(self):
        return self.get_nombre_display()


class Curso(models.Model):
    anio = models.PositiveSmallIntegerField(
        verbose_name="Año",
        help_text="Año de cursado (1 a 6)",
    )
    division = models.CharField(
        max_length=1,
        verbose_name="División",
        help_text="Letra de la división (A, B, C, D)",
    )
    turno = models.ForeignKey(
        Turno,
        on_delete=models.PROTECT,
        related_name="cursos",
        verbose_name="Turno",
    )
    ciclo_lectivo = models.ForeignKey(
        "ciclos_lectivos.CicloLectivo",
        on_delete=models.PROTECT,
        related_name="cursos",
        verbose_name="Ciclo Lectivo",
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["ciclo_lectivo", "anio", "division"]
        constraints = [
            models.UniqueConstraint(
                fields=["anio", "division", "turno", "ciclo_lectivo"],
                name="unico_curso_por_turno_ciclo",
            )
        ]

    def __str__(self):
        return f"{self.anio}° {self.division} — {self.turno}"

    def clean(self):
        if self.anio is not None and (self.anio < 1 or self.anio > 6):
            raise ValidationError("El año debe estar entre 1 y 6.")
        if self.division and (
            not self.division.isalpha() or len(self.division) != 1
        ):
            raise ValidationError("La división debe ser una única letra.")


class Materia(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre",
    )
    activa = models.BooleanField(default=True, verbose_name="Activa")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Materia"
        verbose_name_plural = "Materias"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class AsignacionDocente(models.Model):
    class Tipo(models.TextChoices):
        TITULAR = "titular", "Titular"
        SUPLENTE = "suplente", "Suplente"
        REEMPLAZO = "reemplazo", "Reemplazo"

    docente = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.PROTECT,
        related_name="asignaciones_docentes",
        verbose_name="Docente",
    )
    materia = models.ForeignKey(
        Materia,
        on_delete=models.PROTECT,
        related_name="asignaciones",
        verbose_name="Materia",
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.PROTECT,
        related_name="asignaciones_docentes",
        verbose_name="Curso",
    )
    tipo = models.CharField(
        max_length=20,
        choices=Tipo.choices,
        default=Tipo.TITULAR,
        verbose_name="Tipo",
    )
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")
    fecha_fin = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de fin",
        help_text="Vacío si la asignación está vigente sin fecha de fin",
    )
    activa = models.BooleanField(default=True, verbose_name="Activa")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Asignación Docente"
        verbose_name_plural = "Asignaciones Docentes"
        ordering = ["curso", "materia", "fecha_inicio"]

    def __str__(self):
        return (
            f"{self.docente} — {self.materia} — {self.curso} "
            f"({self.get_tipo_display()})"
        )

    def clean(self):
        if (
            self.fecha_fin
            and self.fecha_inicio
            and self.fecha_fin <= self.fecha_inicio
        ):
            raise ValidationError(
                "La fecha de fin debe ser posterior a la fecha de inicio."
            )

    @property
    def vigente(self):
        from django.utils import timezone

        hoy = timezone.localdate()
        if self.fecha_fin and hoy > self.fecha_fin:
            return False
        return self.activa


class Horario(models.Model):
    class DiaSemana(models.TextChoices):
        LUNES = "lunes", "Lunes"
        MARTES = "martes", "Martes"
        MIERCOLES = "miercoles", "Miércoles"
        JUEVES = "jueves", "Jueves"
        VIERNES = "viernes", "Viernes"

    asignacion_docente = models.ForeignKey(
        AsignacionDocente,
        on_delete=models.CASCADE,
        related_name="horarios",
        verbose_name="Asignación Docente",
    )
    dia_semana = models.CharField(
        max_length=10,
        choices=DiaSemana.choices,
        verbose_name="Día de la semana",
    )
    hora_inicio = models.TimeField(verbose_name="Hora de inicio")
    hora_fin = models.TimeField(verbose_name="Hora de fin")

    class Meta:
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"
        ordering = ["asignacion_docente", "dia_semana", "hora_inicio"]
        constraints = [
            models.UniqueConstraint(
                fields=["asignacion_docente", "dia_semana", "hora_inicio"],
                name="unico_horario_por_dia_asignacion",
            )
        ]

    def __str__(self):
        return (
            f"{self.asignacion_docente.materia} — "
            f"{self.get_dia_semana_display()} {self.hora_inicio}-{self.hora_fin}"
        )

    def clean(self):
        if (
            self.hora_inicio
            and self.hora_fin
            and self.hora_inicio >= self.hora_fin
        ):
            raise ValidationError(
                "La hora de inicio debe ser anterior a la hora de fin."
            )
