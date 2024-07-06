from django.db import models
from django.contrib.auth.models import User


class Estado(models.Model):
    nombre: models.CharField = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre: models.CharField = models.CharField(max_length=100) 
    email: models.EmailField = models.EmailField()
    telefono: models.CharField = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Ticket(models.Model):
    PRIORIDAD_CHOICES: list = [
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
        ('Urgente', 'Urgente'), 
    ]

    ESTADO_CHOICES: list = [
        ('Abierto', 'Abierto'),
        ('En Proceso', 'En Proceso'),
        ('Resuelto', 'Resuelto'),
        ('Cerrado', 'Cerrado'),
    ]

    id_ticket: models.AutoField = models.AutoField(primary_key=True)
    cliente: models.ForeignKey = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='tickets') 
    titulo: models.CharField = models.CharField(max_length=200)
    descripcion: models.TextField = models.TextField()
    prioridad: models.CharField = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='Media')
    estado: models.CharField = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='Abierto')
    fecha_creacion: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ticket {self.id_ticket}: {self.titulo} - {self.cliente}'
