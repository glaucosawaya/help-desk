from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import User


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite seu usuário"
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite sua senha"
            }
        )
    )


class UserCreateForm(
    UserCreationForm
):

    class Meta:

        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "setor",
            "telefone",
        ]

    def __init__(
        self,
        *args,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )

        for field in self.fields.values():

            field.widget.attrs.update(
                {
                    "class": "form-control"
                }
            )

        if self.errors:

            for field_name in self.errors:

                self.fields[
                    field_name
                ].widget.attrs.update(
                    {
                        "class":
                        "form-control is-invalid"
                    }
                )


class UserUpdateForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "setor",
            "telefone",
        ]


class ProfileUpdateForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
            "setor",
            "telefone",
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.update(
                {
                    "class": "form-control"
                }
            )
