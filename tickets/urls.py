from django.urls import path

from .views import (
    TicketCreateView,
    TicketListView,
    TicketDetailView,
    alterar_status,
    assumir_chamado,
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
]
