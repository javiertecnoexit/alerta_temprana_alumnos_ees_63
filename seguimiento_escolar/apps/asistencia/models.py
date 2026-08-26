from django.db import models


class RegistroAsistencia(models.Model):
    class Estado(models.TextChoices):
        PRESENTE = "presente", "Presente"
        AUSENTE = "ausente", "Ausente"
        TARDANZA = "tardanza", "Tardanza"
        JUSTIFICADO = "justificado", "Justificado"

    alumno = models.ForeignKey(
        "alumnos.Alumno",
        on_delete=models.PROTECT,
        related_name="asistencias",
        verbose_name="Alumno",
    )
    curso = models.ForeignKey(
        "estructura_escolar.Curso",
        on_delete=models.PROTECT,
        related_name="asistencias",
        verbose_name="Curso",
    )
    materia = models.ForeignKey(
        "estructura_escolar.Materia",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="asistencias",
        verbose_name="Materia",
    )
    docente = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.PROTECT,
        related_name="asistencias_registradas",
        verbose_name="Docente",
    )
    ciclo_lectivo = models.ForeignKey(
        "ciclos_lectivos.CicloLectivo",
        on_delete=models.PROTECT,
        related_name="asistencias",
        verbose_name="Ciclo Lectivo",
    )
    fecha = models.DateField(verbose_name="Fecha")
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PRESENTE,
        verbose_name="Estado",
    )
    hora_llegada = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Hora de llegada",
        help_text="Solo para tardanzas",
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de Asistencia"
        verbose_name_plural = "Registros de Asistencia"
        ordering = ["-fecha"]
        constraints = [
            models.UniqueConstraint(
                fields=["alumno", "fecha", "materia", "curso"],
                name="unico_registro_asistencia",
            )
        ]

    def __str__(self):
        return f"{self.alumno} — {self.get_estado_display()} ({self.fecha})"