from django.urls import path

from .views import (
    TicketCreateView,
    TicketListView,
    TicketDetailView,
    NotificationListView,
    alterar_status,
    assumir_chamado,
    adicionar_comentario,
    marcar_notificacao_lida,
    approve_resolution,
)


urlpatterns = [

    path(
        "",
        TicketListView.as_view(),
        name="ticket-list"
    ),

    path(
        "novo/",
        TicketCreateView.as_view(),
        name="ticket-create"
    ),

    path(
        "<int:pk>/",
        TicketDetailView.as_view(),
        name="ticket-detail"
    ),
    path(
        "<int:pk>/alterar-status/",
        alterar_status,
        name="ticket-change-status"
    ),
    path(
        "<int:pk>/assumir/",
        assumir_chamado,
        name="ticket-assume"
    ),
    path(
        "<int:pk>/comentario/",
        adicionar_comentario,
        name="ticket-comment"
    ),
    path(
        "notifications/",
        NotificationListView.as_view(),
        name="notification-list",
    ),
    path(
        "notifications/<int:pk>/open/",
        marcar_notificacao_lida,
        name="notification-open",
    ),
    path(
        "<int:pk>/approve-resolution/",
        approve_resolution,
        name="ticket-approve-resolution"
    ),
]
