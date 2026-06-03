from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        TECNICO = "TECNICO", "Técnico"
        COLABORADOR = "COLABORADOR", "Colaborador"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.COLABORADOR
    )

    telefone = models.CharField(
        max_length=20,
        blank=True
    )

    setor = models.CharField(
        max_length=100,
        blank=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )