import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Ticket, Cliente
from .forms import TicketForm, ClienteForm, TicketUpdateForm


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
    """Muestra la lista de todos los tickets, ordenados por fecha de creación descendente."""
    tickets = Ticket.objects.all().order_by("-fecha_creacion")
    return render(request, "pages/index.html", {"tickets": tickets})


def anadir_ticket(request):
    """Muestra un formulario para crear un nuevo ticket y lo guarda si es válido."""
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.usuario_asignado = (
                request.user
            )  # Asigna el usuario actual si está autenticado
            ticket.save()
            messages.success(request, "Ticket añadido con éxito.")
            return redirect("index")
    else:
        form = TicketForm()
    return render(request, "pages/anadir_ticket.html", {"form": form})


def tickets_en_espera(request):
    """Muestra la lista de tickets en espera (estado 'Abierto'), ordenados por fecha de creación."""
    tickets = Ticket.objects.filter(estado="Abierto").order_by("fecha_creacion")
    return render(request, "pages/tickets_en_espera.html", {"tickets": tickets})


def tickets_atendidos(request):
    """Muestra la lista de tickets atendidos (estados diferentes a 'Abierto'), ordenados por fecha de creación descendente."""
    tickets = Ticket.objects.exclude(estado="Abierto").order_by("-fecha_creacion")
    return render(request, "pages/tickets_atendidos.html", {"tickets": tickets})


def atender_ticket(request, ticket_id):
    """Permite ver y actualizar el estado de un ticket."""
    ticket = get_object_or_404(Ticket, id_ticket=ticket_id)
    if request.method == "POST":
        form = TicketUpdateForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Ticket atendido y cerrado con éxito.")
            return redirect("index")
    else:
        form = TicketUpdateForm(instance=ticket)
    return render(
        request, "pages/atender_ticket.html", {"ticket": ticket, "form": form}
    )


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
            return redirect("agregar_cliente")
    else:
        form = ClienteForm()
    return render(request, "pages/agregar_cliente.html", {"form": form})


def ver_cliente(request, cliente_id):
    """Muestra los detalles de un cliente y sus tickets asociados."""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    tickets = cliente.tickets.all()
    return render(
        request, "pages/ver_cliente.html", {"cliente": cliente, "tickets": tickets}
    )

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
    tickets_ordenados = quicksort(
        tickets, lambda ticket: ticket.prioridad
    )  # Ordenar por prioridad (puedes cambiar el criterio)
    return render(request, "tickets_en_espera.html", {"tickets": tickets_ordenados})


def buscar_ticket(request):
    """Busca tickets según un término de búsqueda."""
    if request.method == "GET":
        query = request.GET.get("q")
        if query:
            resultados = busqueda_lineal(Ticket.objects.all(), query)
            return render(
                request,
                "resultados_busqueda.html",
                {"resultados": resultados, "query": query},
            )
    return render(request, "buscar_ticket.html")


# -------------------------
# Funciones auxiliares (quicksort y busqueda_lineal)
# -------------------------

def quicksort(arr, key=lambda x: x):
    """Implementación del algoritmo quicksort."""
    if len(arr) < 2:
        return arr
    else:
        pivote = arr[0]
        menores = [i for i in arr[1:] if key(i) <= key(pivote)]
        mayores = [i for i in arr[1:] if key(i) > key(pivote)]
        return quicksort(menores, key) + [pivote] + quicksort(mayores, key)


def busqueda_lineal(arr, query):
    """Implementación de la búsqueda lineal."""
    resultados = []
    for elemento in arr:
        if (
            query.lower() in str(elemento).lower()
        ):  # Búsqueda insensible a mayúsculas/minúsculas
            resultados.append(elemento)
    return resultados
