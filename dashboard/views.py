from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from tickets.models import (
    Ticket,
    TicketHistory,
)


class DashboardView(
    LoginRequiredMixin,
    TemplateView
):

    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(
            **kwargs
        )

        if self.request.user.role in [
            "ADMIN",
            "TECNICO"
        ]:

            tickets = Ticket.objects.all()

        else:

            tickets = Ticket.objects.filter(
                requester=self.request.user
            )

        context["total_tickets"] = tickets.count()

        context["open_tickets"] = tickets.filter(
            status=Ticket.Status.OPEN
        ).count()

        context["analysis_tickets"] = tickets.filter(
            status=Ticket.Status.ANALYSIS
        ).count()

        context["resolved_tickets"] = tickets.filter(
            status=Ticket.Status.RESOLVED
        ).count()

        context["critical_tickets"] = tickets.filter(
            priority=Ticket.Priority.CRITICAL
        ).count()

        context["ultimos_chamados"] = (
            tickets
            .select_related(
                "requester",
                "assigned_to"
            )
            .order_by("-created_at")[:4]
        )

        context["ultimas_movimentacoes"] = (
            TicketHistory.objects
            .select_related(
                "ticket",
                "user"
            )
            .filter(
                ticket__in=tickets
            )
            .order_by("-created_at")[:4]
        )

        return context
