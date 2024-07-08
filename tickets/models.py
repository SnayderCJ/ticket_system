from django.db import models
from django.contrib.auth.models import User


class Estado(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=100) 
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Ticket(models.Model):
    '''Representa un ticket de soporte técnico.'''

    PRIORIDAD_BAJA = 'Baja'
    PRIORIDAD_MEDIA = 'Media'
    PRIORIDAD_ALTA = 'Alta'
    PRIORIDAD_URGENTE = 'Urgente'

    ESTADO_ABIERTO = 'Abierto'
    ESTADO_CERRADO = 'Cerrado'  # Eliminamos las opciones "En Proceso" y "Resuelto"

    PRIORIDAD_CHOICES = [
        (PRIORIDAD_BAJA, 'Baja'),
        (PRIORIDAD_MEDIA, 'Media'),
        (PRIORIDAD_ALTA, 'Alta'),
        (PRIORIDAD_URGENTE, 'Urgente'),
    ]

    ESTADO_CHOICES = [
        (ESTADO_ABIERTO, 'Abierto'),
        (ESTADO_CERRADO, 'Cerrado'),  # Solo dejamos "Abierto" y "Cerrado"
    ]

    id_ticket = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='tickets') 
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='Media')
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='Abierto')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ticket {self.id_ticket}: {self.titulo} - {self.cliente} '
