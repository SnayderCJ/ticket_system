import json
from django.db.models import Q
from django.apps import AppConfig
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Ticket, Cliente
from .forms import TicketForm, ClienteForm, TicketUpdateForm, TicketFilter
from .cola import quicksort, busqueda_binaria, Cola,render_to_pdf
from .cola import Nodo, Cola, quicksort, busqueda_binaria

cola_tickets = Cola()

# -------------------------
# Vistas para la página de inicio
# -------------------------
def home(request):
    """Renderiza la página de inicio (home.html)."""
    return render(request, "pages/home.html")


# -------------------------
# Vistas para gestión de tickets
# -------------------------
def index(request):
    queryset = Ticket.objects.all().order_by("fecha_creacion")  # Ordenar por fecha de creación (ascendente)
    filter_form = TicketFilter(request.GET, queryset=queryset)
    tickets = filter_form.qs  

    search_query = request.GET.get('q')
    if search_query:
        tickets = tickets.filter(titulo__icontains=search_query)

    # Convertir el QuerySet en una lista para poder usarla con la cola
    tickets_list = list(tickets)

    # Encolar los tickets (sin ordenar)
    cola_tickets = Cola()
    for ticket in tickets_list:
        cola_tickets.encolar(ticket)

    return render(request, 'pages/index.html', {
        'tickets': cola_tickets,
        'filter_form': filter_form,
        'prioridades': Ticket.PRIORIDAD_CHOICES
    })

def anadir_ticket(request):
    """Muestra un formulario para crear un nuevo ticket y lo guarda si es válido."""
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.usuario_asignado = request.user
            ticket.save()
            messages.success(request, "Ticket añadido con éxito.")
            return redirect("tickets_en_espera")
    else:
        form = TicketForm()
    return render(request, "pages/anadirTickets.html", {"form": form})


def tickets_en_espera(request):
    """Muestra la lista de tickets en espera (estado 'Abierto'), ordenados por fecha de creación."""

    queryset = Ticket.objects.filter(estado="Abierto").order_by("fecha_creacion")  # Ordenar por fecha de creación (ascendente)
    filter_form = TicketFilter(request.GET, queryset=queryset)
    tickets = filter_form.qs

    search_query = request.GET.get('q')
    if search_query:
        tickets = tickets.filter(titulo__icontains=search_query)

    # Convertir el QuerySet en una lista para poder usarla con la cola
    tickets_list = list(tickets)

    # Encolar los tickets (sin ordenar)
    cola_tickets = Cola()
    for ticket in tickets_list:
        cola_tickets.encolar(ticket)

    return render(request, "pages/clienteEnEspera.html", {
        'tickets': cola_tickets,
        'filter_form': filter_form,
        'prioridades': Ticket.PRIORIDAD_CHOICES})


def tickets_atendidos(request):
    queryset = Ticket.objects.filter(estado="Cerrado").order_by("fecha_creacion")  # FIFO
    filter_form = TicketFilter(request.GET, queryset=queryset)
    tickets = filter_form.qs

    search_query = request.GET.get('q')
    if search_query:
        tickets = tickets.filter(titulo__icontains=search_query)

    # Convertir el QuerySet en una lista para poder usarla con la cola
    tickets_list = list(tickets)

    # Encolar los tickets (sin ordenar)
    cola_tickets = Cola()
    for ticket in tickets_list:
        cola_tickets.encolar(ticket)

    if request.GET.get('pdf'):  # Verificar si se solicita un PDF
        # Pasar la cola de tickets al contexto
        context = {'tickets': cola_tickets}
        return render_to_pdf('pages/pdf_tickets_atendidos.html', context)

    return render(request, 'pages/clienteAtendidos.html', {
        'tickets': cola_tickets,
        'filter_form': filter_form,
        'prioridades': Ticket.PRIORIDAD_CHOICES
    })

def atender_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id_ticket=ticket_id)

    if request.method == "POST":
        form = TicketUpdateForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save()  # Guarda el ticket para obtener el estado actualizado

            if ticket.estado == Ticket.ESTADO_ABIERTO:  # Si el estado es Abierto
                messages.success(request, "Ticket atendido y abierto con éxito.")
                return redirect("tickets_en_espera")  # Redirige a tickets en espera
            elif ticket.estado == Ticket.ESTADO_CERRADO:  # Si el estado es Cerrado
                messages.success(request, "Ticket atendido y cerrado con éxito.")
                return redirect("tickets_atendidos")   # Redirige a tickets atendidos

    else:
        form = TicketUpdateForm(instance=ticket)

    return render(request, "pages/atenderTicket.html", {"ticket": ticket, "form": form})


# -------------------------
# Vistas para gestión de clientes
# -------------------------


def agregar_cliente(request):
    """Muestra un formulario para agregar un nuevo cliente y lo guarda si es válido."""
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente añadido con éxito.")  
            return redirect("anadir_ticket")
    else:
        form = ClienteForm()
    return render(request, "pages/agregarCliente.html", {"form": form})


def ver_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    ticket_id = request.GET.get('ticket_id')  # Obtener el ID del ticket de la URL

    if ticket_id:
        ticket = get_object_or_404(Ticket, id_ticket=ticket_id, cliente=cliente)
    else:
        ticket = None  # Si no se proporciona un ticket_id, no mostrar ningún ticket

    return render(request, "pages/verCliente.html", {"cliente": cliente, "ticket": ticket})


# -------------------------
# Vistas para guardar/cargar y ordenar tickets
# -------------------------


def guardar_cola(request):
    """Guarda la cola de tickets abiertos en un archivo JSON."""
    tickets = Ticket.objects.filter(estado="Abierto").order_by("fecha_creacion")
    data = [
        {
            "id_ticket": ticket.id_ticket,
            "cliente": ticket.cliente.nombre,
            "descripcion": ticket.descripcion,
            "prioridad": ticket.prioridad,
            "fecha_creacion": ticket.fecha_creacion.isoformat(),
        }
        for ticket in tickets
    ]
    with open("cola_tickets.json", "w") as f:
        json.dump(data, f)
    messages.success(request, "Cola de tickets guardada con éxito.")
    return redirect("index")


def cargar_cola(request):
    """Carga la cola de tickets desde un archivo JSON."""
    try:
        with open("cola_tickets.json", "r") as f:
            data = json.load(f)
        for ticket_data in data:
            cliente, _ = Cliente.objects.get_or_create(nombre=ticket_data["cliente"])
            Ticket.objects.create(
                id_ticket=ticket_data["id_ticket"],
                cliente=cliente,
                descripcion=ticket_data["descripcion"],
                prioridad=ticket_data["prioridad"],
                fecha_creacion=ticket_data["fecha_creacion"],
                estado="Abierto",
            )
        messages.success(request, "Cola de tickets cargada con éxito.")
    except FileNotFoundError:
        messages.warning(request, "No se encontró el archivo de cola de tickets.")
    return redirect("index")


def ordenar_tickets(request):
    """Ordena los tickets en espera por prioridad (usando quicksort)."""
    tickets = Ticket.objects.filter(estado="Abierto").order_by("fecha_creacion")
    tickets_ordenados = quicksort(tickets, lambda ticket: ticket.prioridad)
    return render(request, "pages/clienteEnEspera.html", {"tickets": tickets_ordenados})


def buscar_ticket(request):
    """Busca tickets según un término de búsqueda."""
    if request.method == "GET":
        query = request.GET.get("q")
        if query:
            resultados = busqueda_lineal(Ticket.objects.all(), query)
            return render(
                request,
                "pages/resultados_busqueda.html",
                {"resultados": resultados, "query": query},
            )
    return render(request, "pages/buscar_ticket.html")


# -------------------------
# Guardar cola
# -------------------------

def guardar_cola(request):
    tickets = Ticket.objects.filter(estado="Abierto").order_by("fecha_creacion")
    data = [
        {
            "cliente": ticket.cliente.nombre,
            "titulo": ticket.titulo,
            "descripcion": ticket.descripcion,
            "prioridad": ticket.prioridad,
            "estado": ticket.estado,
            "fecha_creacion": ticket.fecha_creacion.isoformat(),
        }
        for ticket in tickets
    ]
    try:
        with open("cola_tickets.json", "w") as f:
            json.dump(data, f)
        messages.success(request, "Cola de tickets guardada con éxito.")
    except Exception as e:
        messages.error(request, f"Error al guardar la cola de tickets: {e}")
    return redirect("index")

