from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Página de inicio
    path('tickets/', views.index, name='index'),  # Lista de todos los tickets
    path('tickets/anadir/', views.anadir_ticket, name='anadir_ticket'),
    path('tickets/en-espera/', views.tickets_en_espera, name='tickets_en_espera'),
    path('tickets/atendidos/', views.tickets_atendidos, name='tickets_atendidos'),
    path('tickets/ordenar/', views.ordenar_tickets, name='ordenar_tickets'),
    path('tickets/buscar/', views.buscar_ticket, name='buscar_ticket'),
    path('tickets/guardar/', views.guardar_cola, name='guardar_cola'),
    path('tickets/cargar/', views.cargar_cola, name='cargar_cola'),
    path('tickets/atender/<int:ticket_id>/', views.atender_ticket, name='atender_ticket'),
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/<int:cliente_id>/', views.ver_cliente, name='ver_cliente'),
]
