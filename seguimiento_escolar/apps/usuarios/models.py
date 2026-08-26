from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        DOCENTE = "docente", "Docente"
        PRECEPTOR = "preceptor", "Preceptor"
        DIRECTIVO = "directivo", "Directivo"
        ADMIN = "admin", "Admin"

    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.DOCENTE,
        verbose_name="Rol",
        help_text="Rol institucional del usuario",
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.get_full_name() or self.username}"

    @property
    def es_docente(self):
        return self.rol == self.Rol.DOCENTE

    @property
    def es_preceptor(self):
        return self.rol == self.Rol.PRECEPTOR

    @property
    def es_directivo(self):
        return self.rol == self.Rol.DIRECTIVO

    @property
    def es_admin(self):
        return self.rol == self.Rol.ADMIN