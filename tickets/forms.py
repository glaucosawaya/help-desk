from django import forms
from .models import (Ticket,
                     TicketComment)


class MultipleFileInput(forms.ClearableFileInput):

    allow_multiple_selected = True


class MultipleFileField(forms.FileField):

    widget = MultipleFileInput

    def clean(self, data, initial=None):

        if isinstance(data, (list, tuple)):

            return [
                super(MultipleFileField, self).clean(
                    file,
                    initial
                )
                for file in data
            ]

        return super().clean(data, initial)


class TicketForm(forms.ModelForm):

    anexos = MultipleFileField(
        required=False,
        widget=MultipleFileInput(
            attrs={
                "class": "form-control",
                "accept": "image/*",
            }
        )
    )

    class Meta:

        model = Ticket

        fields = [
            "title",
            "system_name",
            "category",
            "priority",
            "description",
            "error_message",
        ]

        labels = {
            "title": "Título",
            "system_name": "Sistema",
            "category": "Categoria",
            "priority": "Prioridade",
            "description": "Descrição do Problema",
            "error_message": "Mensagem Técnica do Erro",
        }

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex.: Erro ao importar arquivo"
                }
            ),

            "system_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex.: PGFN"
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "priority": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Descreva detalhadamente o problema encontrado"
                }
            ),

            "error_message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Cole aqui a mensagem técnica apresentada pelo sistema"
                }
            ),
        }


class TicketStatusForm(forms.ModelForm):

    class Meta:

        model = Ticket

        fields = [
            "status"
        ]


class TicketCommentForm(forms.ModelForm):

    class Meta:

        model = TicketComment

        fields = [
            "comment"
        ]

        labels = {
            "comment": "Comentário"
        }

        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": "Digite uma observação..."
                }
            )
        }


class TicketCommentForm(forms.ModelForm):

    class Meta:

        model = TicketComment

        fields = ["comment"]

        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Digite seu comentário..."
                }
            )
        }
