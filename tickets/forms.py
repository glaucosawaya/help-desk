from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):

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