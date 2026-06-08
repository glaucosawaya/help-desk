from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    UserLoginView,
    UserPasswordChangeView,
    UserListView,
    UserCreateView,
    UserUpdateView,
    ProfileUpdateView,
)

urlpatterns = [

    path(
        "login/",
        UserLoginView.as_view(),
        name="login"
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout"
    ),

    path(
        "senha/",
        UserPasswordChangeView.as_view(),
        name="change-password"
    ),
    path(
        "usuarios/",
        UserListView.as_view(),
        name="user-list"
    ),

    path(
        "usuarios/novo/",
        UserCreateView.as_view(),
        name="user-create"
    ),
    path(
        "usuarios/<int:pk>/editar/",
        UserUpdateView.as_view(),
        name="user-update"
    ),
    path(
        "perfil/",
        ProfileUpdateView.as_view(),
        name="profile"
    ),

]
