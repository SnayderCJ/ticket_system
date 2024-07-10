from django.core.management.base import BaseCommand
import json
from tickets.models import Ticket, Cliente

class Command(BaseCommand):
    help = 'Cargar cola de tickets desde un archivo JSON'

    def handle(self, *args, **options):
        try:
            with open("cola_tickets.json", "r") as f:
                data = json.load(f)

            # Validación de datos (opcional, pero recomendada)
            for ticket_data in data:
                if ticket_data.get("prioridad") not in [choice[0] for choice in Ticket.PRIORIDAD_CHOICES]:
                    raise ValueError(f"Prioridad inválida: {ticket_data['prioridad']}")
                if ticket_data.get("estado") not in [choice[0] for choice in Ticket.ESTADO_CHOICES]:
                    raise ValueError(f"Estado inválido: {ticket_data['estado']}")

            # Cargar clientes primero
            clientes_creados = {}
            for ticket_data in data:
                cliente_nombre = ticket_data["cliente"]
                if cliente_nombre not in clientes_creados:
                    cliente, _ = Cliente.objects.get_or_create(nombre=cliente_nombre)
                    clientes_creados[cliente_nombre] = cliente

            # Cargar tickets después de los clientes
            for ticket_data in data:
                cliente = clientes_creados[ticket_data["cliente"]]
                Ticket.objects.create(
                    cliente=cliente,
                    titulo=ticket_data["titulo"],
                    descripcion=ticket_data["descripcion"],
                    prioridad=ticket_data["prioridad"],
                    estado=ticket_data["estado"],
                    fecha_creacion=ticket_data["fecha_creacion"],
                )

            self.stdout.write(self.style.SUCCESS('Cola de tickets cargada con éxito.'))
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING('No se encontró el archivo de cola de tickets.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al cargar la cola de tickets: {e}'))