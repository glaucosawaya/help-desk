from django.contrib.auth.models import (
    AbstractUser,
    UserManager,
)
from django.db import models


class CustomUserManager(UserManager):

    def create_superuser(self, username, email=None, password=None, **extra_fields):

        extra_fields.setdefault("role", User.Role.ADMIN)

        return super().create_superuser(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )


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
    objects = CustomUserManager()

    @property
    def nome_exibicao(self):

        nome = (
            f"{self.first_name} {self.last_name}"
        ).strip()

        return nome or self.username
