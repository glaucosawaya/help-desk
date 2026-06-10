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
    TicketAttachment,
    Notification,
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
from django.http import JsonResponse
from django.utils import timezone


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

        comments = self.object.comments.select_related(
            "user").order_by("created_at")

        context["comment_form"] = TicketCommentForm()
        context["comments_preview"] = comments[:3]
        context["comments_all"] = comments

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

        form.instance.requester = self.request.user

        response = super().form_valid(form)

        TicketHistory.objects.create(
            ticket=self.object,
            user=self.request.user,
            action="Chamado criado"
        )

        arquivos = self.request.FILES.getlist(
            "anexos"
        )

        for arquivo in arquivos:

            TicketAttachment.objects.create(
                ticket=self.object,
                file=arquivo
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

        novo_status = request.POST.get("status")
        mensagem = request.POST.get("waiting_message")

        ticket.status = novo_status

        if novo_status == Ticket.Status.WAITING_USER:
            ticket.waiting_message = mensagem
        else:
            ticket.waiting_message = None

        if novo_status == Ticket.Status.RESOLVED:

            ticket.resolved_by = request.user
            ticket.resolved_at = timezone.now()

            Notification.objects.create(
                recipient=ticket.requester,
                ticket=ticket,
                message=(
                    f"Seu chamado {ticket.codigo} foi resolvido. "
                    "Clique para aprovar ou rejeitar a solução."
                )
            )

        ticket.save()

    if novo_status == Ticket.Status.WAITING_USER and mensagem:

        Notification.objects.create(
            recipient=ticket.requester,
            ticket=ticket,
            message="O técnico solicitou mais informações."
        )

        TicketHistory.objects.create(
            ticket=ticket,
            user=request.user,
            action=f"Aguardando usuário: {mensagem}"
        )

    else:

        Notification.objects.create(
            recipient=ticket.requester,
            ticket=ticket,
            message=(
                f"Seu chamado {ticket.codigo} "
                f"foi atualizado para "
                f"{ticket.get_status_display()}."
            )
        )

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
def adicionar_comentario(request, pk):

    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method == "POST":

        comentario = request.POST.get("comment")

        if comentario:

            TicketComment.objects.create(
                ticket=ticket,
                user=request.user,
                comment=comentario
            )

            TicketHistory.objects.create(
                ticket=ticket,
                user=request.user,
                action=f"Comentário: {comentario}"
            )
            if (
                request.user == ticket.requester
                and ticket.status == Ticket.Status.WAITING_USER
                and ticket.assigned_to
            ):

                Notification.objects.create(
                    recipient=ticket.assigned_to,
                    ticket=ticket,
                    message=(
                        f"{request.user.nome_exibicao} "
                        f"respondeu ao chamado {ticket.codigo}."
                    )
                )

                TicketHistory.objects.create(
                    ticket=ticket,
                    user=request.user,
                    action="Usuário respondeu à solicitação do técnico."
                )

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":

        return JsonResponse({
            "success": True,
            "user": request.user.nome_exibicao,
            "comment": comentario,
            "created_at": timezone.localtime().strftime("%d/%m %H:%M"),
        })

    return redirect(
        "ticket-detail",
        pk=pk
    )


class NotificationListView(LoginRequiredMixin, ListView):

    model = Notification

    template_name = "tickets/notifications.html"

    context_object_name = "notifications"

    paginate_by = 20

    def get_queryset(self):

        return Notification.objects.filter(
            recipient=self.request.user
        ).select_related(
            "ticket"
        )


@login_required
def marcar_notificacao_lida(request, pk):

    notification = get_object_or_404(
        Notification,
        pk=pk,
        recipient=request.user
    )

    notification.is_read = True
    notification.save()

    return redirect(
        "ticket-detail",
        pk=notification.ticket.id
    )


@login_required
def approve_resolution(request, pk):

    ticket = get_object_or_404(Ticket, pk=pk)

    if request.user != ticket.requester:
        return redirect("ticket-detail", pk=pk)

    if request.method == "POST":

        action = request.POST.get("action")

        if action == "confirm":

            ticket.status = Ticket.Status.CLOSED

            TicketHistory.objects.create(
                ticket=ticket,
                user=request.user,
                action="Resolução aprovada pelo usuário"
            )

        elif action == "reject":

            ticket.status = Ticket.Status.DEVELOPMENT

            TicketHistory.objects.create(
                ticket=ticket,
                user=request.user,
                action="Resolução rejeitada pelo usuário"
            )

        ticket.save()

    return redirect("ticket-detail", pk=pk)
