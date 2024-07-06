from django import forms
from .models import Cliente, Ticket

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "email", "telefono"]  # Incluimos el campo 'empresa'
        labels = {
            'nombre': 'Nombre',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['cliente', 'titulo', 'descripcion', 'prioridad']  # Quitamos 'estado'
        labels = {
            'cliente': 'Cliente',
            'titulo': 'Título',  # Agregamos la etiqueta para 'titulo'
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
        fields = ["estado"]  # Cambiamos 'atendido' por 'estado'
        labels = {
            'estado': 'Estado',
        }
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
