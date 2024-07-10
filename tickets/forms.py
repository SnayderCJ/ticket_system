import django_filters
from django import forms
from django.core.validators import RegexValidator
from .models import Cliente, Ticket

class ClienteForm(forms.ModelForm):
    telefono = forms.CharField(
        label='Teléfono',
        max_length=10,
        validators=[
            RegexValidator(r'^\d{10}$', 'El teléfono debe tener 10 dígitos numéricos.'),
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Cliente
        fields = ["nombre", "email", "telefono"]
        labels = {
            'nombre': 'Nombre',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['cliente', 'titulo', 'descripcion', 'prioridad']
        labels = {
            'cliente': 'Cliente',
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'prioridad': 'Prioridad',
        }
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'prioridad': forms.Select(attrs={'class': 'form-control'}),
        }

class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["estado"]
        labels = {
            'estado': 'Estado',
        }
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }


class TicketFilter(django_filters.FilterSet):
    prioridad = django_filters.MultipleChoiceFilter(
        choices=Ticket.PRIORIDAD_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Ticket
        fields = ['prioridad']
