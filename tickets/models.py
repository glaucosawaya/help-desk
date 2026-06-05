from django.conf import settings
from django.db import models


class Ticket(models.Model):

    class Category(models.TextChoices):
        ERROR = "ERROR", "Erro"
        QUESTION = "QUESTION", "Dúvida"
        IMPROVEMENT = "IMPROVEMENT", "Melhoria"

    class Priority(models.TextChoices):
        LOW = "LOW", "Baixa"
        MEDIUM = "MEDIUM", "Média"
        HIGH = "HIGH", "Alta"
        CRITICAL = "CRITICAL", "Crítica"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Aberto"
        ANALYSIS = "ANALYSIS", "Em análise"
        WAITING_USER = "WAITING_USER", "Aguardando usuário"
        WAITING_THIRD_PARTY = "WAITING_THIRD_PARTY", "Aguardando terceiro"
        DEVELOPMENT = "DEVELOPMENT", "Em desenvolvimento"
        TESTING = "TESTING", "Em teste"
        RESOLVED = "RESOLVED", "Resolvido"
        CLOSED = "CLOSED", "Fechado"

    title = models.CharField(
        "Título",
        max_length=255
    )

    system_name = models.CharField(
        "Sistema",
        max_length=150
    )

    category = models.CharField(
        "Categoria",
        max_length=20,
        choices=Category.choices,
        default=Category.ERROR
    )

    priority = models.CharField(
        "Prioridade",
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )

    status = models.CharField(
        "Status",
        max_length=30,
        choices=Status.choices,
        default=Status.OPEN
    )

    description = models.TextField(
        "Descrição"
    )

    error_message = models.TextField(
        "Mensagem Técnica do Erro",
        blank=True,
        null=True
    )

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Solicitante",
        on_delete=models.CASCADE,
        related_name="requested_tickets"
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Responsável",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets"
    )

    created_at = models.DateTimeField(
        "Data de Criação",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        "Última Atualização",
        auto_now=True
    )
    @property
    def codigo(self):

        return f"HD-{self.id:06d}"

    def __str__(self):
        return self.title
    
class TicketHistory(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="history"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    action = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

    def __str__(self):

        return self.action    

class TicketComment(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

    def __str__(self):

        return f"{self.user} - {self.ticket.codigo}"