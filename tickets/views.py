from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
)

from .models import (
    Ticket,
    TicketHistory,
    TicketComment,
)
from .forms import (
    TicketForm,
    TicketCommentForm,
)
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Count
from django.http import Http404


class TicketDetailView(
    LoginRequiredMixin,
    DetailView
):

    model = Ticket

    template_name = "tickets/detail.html"

    context_object_name = "ticket"

    def get_object(self, queryset=None):

        ticket = super().get_object(queryset)

        if self.request.user.role in [
            "ADMIN",
            "TECNICO"
        ]:
            return ticket

        if ticket.requester == self.request.user:
            return ticket

        raise Http404()

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["comment_form"] = TicketCommentForm()

        return context


class TicketCreateView(
    LoginRequiredMixin,
    CreateView
):

    model = Ticket

    form_class = TicketForm

    template_name = "tickets/create.html"

    success_url = reverse_lazy(
        "ticket-list"
    )

    def form_valid(self, form):

        form.instance.requester = (
            self.request.user
        )

        response = super().form_valid(
            form
        )

        TicketHistory.objects.create(
            ticket=self.object,
            user=self.request.user,
            action="Chamado criado"
        )

        return response


class TicketListView(
    LoginRequiredMixin,
    ListView
):

    model = Ticket

    template_name = "tickets/list.html"

    context_object_name = "tickets"

    def get_queryset(self):

        queryset = (
            Ticket.objects
            .select_related(
                "requester",
                "assigned_to"
            )
            .order_by("-created_at")
        )

        if self.request.user.role in [
            "ADMIN",
            "TECNICO"
        ]:
            return queryset

        return queryset.filter(
            requester=self.request.user
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(
            **kwargs
        )

        tickets = self.get_queryset()

        context["total_tickets"] = tickets.count()

        context["open_count"] = tickets.filter(
            status="OPEN"
        ).count()

        context["analysis_count"] = tickets.filter(
            status="ANALYSIS"
        ).count()

        context["development_count"] = tickets.filter(
            status="DEVELOPMENT"
        ).count()

        context["resolved_count"] = tickets.filter(
            status="RESOLVED"
        ).count()

        return context


@login_required
def assumir_chamado(request, pk):

    ticket = get_object_or_404(
        Ticket,
        pk=pk
    )

    if request.user.role in [
        "ADMIN",
        "TECNICO"
    ]:

        ticket.assigned_to = request.user
        ticket.save()

        TicketHistory.objects.create(
            ticket=ticket,
            user=request.user,
            action="Chamado assumido"
        )

    return redirect(
        "ticket-detail",
        pk=ticket.pk
    )


@login_required
def alterar_status(request, pk):

    ticket = get_object_or_404(
        Ticket,
        pk=pk
    )

    if request.user.role not in [
        "ADMIN",
        "TECNICO"
    ]:
        return redirect(
            "ticket-detail",
            pk=pk
        )

    if request.method == "POST":

        novo_status = request.POST.get(
            "status"
        )

        ticket.status = novo_status

        ticket.save()

        TicketHistory.objects.create(
            ticket=ticket,
            user=request.user,
            action=f"Status alterado para {ticket.get_status_display()}"
        )

    return redirect(
        "ticket-detail",
        pk=pk
    )


@login_required
def adicionar_comentario(
    request,
    pk
):

    ticket = get_object_or_404(
        Ticket,
        pk=pk
    )

    if request.method == "POST":

        comentario = request.POST.get(
            "comment"
        )

        if comentario:

            TicketComment.objects.create(
                ticket=ticket,
                user=request.user,
                comment=comentario
            )

            TicketHistory.objects.create(
                ticket=ticket,
                user=request.user,
                action="Comentário adicionado"
            )

    return redirect(
        "ticket-detail",
        pk=pk
    )
