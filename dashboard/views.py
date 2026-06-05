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

        context = super().get_context_data(**kwargs)

        context["total_tickets"] = Ticket.objects.count()

        context["open_tickets"] = Ticket.objects.filter(
            status=Ticket.Status.OPEN
        ).count()

        context["analysis_tickets"] = Ticket.objects.filter(
            status=Ticket.Status.ANALYSIS
        ).count()

        context["resolved_tickets"] = Ticket.objects.filter(
            status=Ticket.Status.RESOLVED
        ).count()

        context["critical_tickets"] = Ticket.objects.filter(
            priority=Ticket.Priority.CRITICAL
        ).count()
        
        context["ultimos_chamados"] = (Ticket.objects
            .select_related(
                "requester",
                "assigned_to"
            )
            .order_by("-created_at")[:5]
        )

        context["ultimas_movimentacoes"] = (
            TicketHistory.objects
            .select_related(
                "ticket",
                "user"
            )
            .order_by("-created_at")[:10]
        )

        return context
