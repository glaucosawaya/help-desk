from django.contrib.auth.views import LoginView
from .forms import LoginForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
)

from .models import User
from .forms import (
    UserCreateForm,
    UserUpdateForm,
    ProfileUpdateForm,
)
from .mixins import AdminOnlyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView


class UserLoginView(LoginView):

    template_name = "accounts/login.html"

    authentication_form = LoginForm


class UserPasswordChangeView(
    PasswordChangeView
):

    template_name = (
        "accounts/change_password.html"
    )

    success_url = reverse_lazy(
        "dashboard"
    )

    def get_form(self, form_class=None):

        form = super().get_form(form_class)

        for field in form.fields.values():

            field.widget.attrs.update(
                {
                    "class": "form-control"
                }
            )

        return form


class UserListView(
    LoginRequiredMixin,
    AdminOnlyMixin,
    ListView
):

    model = User

    template_name = (
        "accounts/user_list.html"
    )

    context_object_name = "users"


class UserCreateView(
    LoginRequiredMixin,
    AdminOnlyMixin,
    CreateView
):

    model = User

    form_class = UserCreateForm

    template_name = (
        "accounts/user_create.html"
    )

    success_url = reverse_lazy(
        "user-list"
    )

    def get_form(self, form_class=None):

        form = super().get_form(form_class)

        for field in form.fields.values():

            field.widget.attrs.update(
                {
                    "class": "form-control"
                }
            )

        return form


class UserUpdateView(
    LoginRequiredMixin,
    AdminOnlyMixin,
    UpdateView
):

    model = User

    form_class = UserUpdateForm

    template_name = "accounts/user_update.html"

    success_url = reverse_lazy(
        "user-list"
    )

    def get_form(self, form_class=None):

        form = super().get_form(form_class)

        for field in form.fields.values():

            field.widget.attrs.update(
                {
                    "class": "form-control"
                }
            )

        return form


class ProfileUpdateView(
    LoginRequiredMixin,
    UpdateView
):

    model = User

    form_class = ProfileUpdateForm

    template_name = "accounts/profile.html"

    success_url = reverse_lazy(
        "dashboard"
    )

    def get_object(self):

        return self.request.user
