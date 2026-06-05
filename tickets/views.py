from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
)

from .models import Ticket
from .forms import TicketForm
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404


class TicketDetailView(
    LoginRequiredMixin,
    DetailView
):

    model = Ticket

    template_name = "tickets/detail.html"

    context_object_name = "ticket"

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

        return super().form_valid(form)


class TicketListView(
    LoginRequiredMixin,
    ListView
):

    model = Ticket

    template_name = "tickets/list.html"

    context_object_name = "tickets"

    ordering = ["-created_at"]

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

    return redirect(
        "ticket-detail",
        pk=pk
    )    