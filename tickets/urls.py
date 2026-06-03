from django.urls import path

from .views import (
    TicketCreateView,
    TicketListView,
    TicketDetailView,
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
]
