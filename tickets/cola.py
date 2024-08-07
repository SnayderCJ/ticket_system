from io import BytesIO # nos ayuda a convertir un html en pdf
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


class Nodo:
    def __init__(self, data=None):
        self.data = data  # Dato que almacena el nodo
        self.next = None  # Puntero al siguiente nodo en la cola

class Cola:
    def __init__(self):
        self.frente = None  # Puntero al frente de la cola
        self.final = None   # Puntero al final de la cola

    def encolar(self, item):
        # Crear un nuevo nodo con el ítem
        nuevo_nodo = Nodo(item)
        if self.final:
            # Si la cola no está vacía, apuntar el final actual al nuevo nodo
            self.final.next = nuevo_nodo
        self.final = nuevo_nodo  # Actualizar el final de la cola
        if not self.frente:
            # Si la cola estaba vacía, actualizar también el frente
            self.frente = nuevo_nodo

    def desencolar(self):
        if self.frente:
            # Obtener el dato del frente de la cola
            item = self.frente.data
            # Mover el frente al siguiente nodo
            self.frente = self.frente.next
            if not self.frente:
                # Si la cola quedó vacía, también actualizar el final
                self.final = None
            return item
        raise Exception("La cola está vacía")  # Lanzar excepción si la cola está vacía

    def esta_vacia(self):
        return self.frente is None  # Verificar si la cola está vacía

    def __iter__(self):
        # Hacer que la cola sea iterable
        actual = self.frente
        while actual:
            yield actual.data
            actual = actual.next


def quicksort(arr, key=lambda x: x, reverse=False):
    if len(arr) < 2:
        return arr
    else:
        pivot = arr[0]
        menores = [i for i in arr[1:] if key(i) <= key(pivot)]
        mayores = [i for i in arr[1:] if key(i) > key(pivot)]
        if reverse:  # Ordenar en reversa si reverse es True
            return quicksort(mayores, key, reverse) + [pivot] + quicksort(menores, key, reverse)
        else:
            return quicksort(menores, key, reverse) + [pivot] + quicksort(mayores, key, reverse)

def busqueda_binaria(arr, objetivo, key=lambda x: x):
    bajo, alto = 0, len(arr) - 1  # Definimos los límites inferior y superior
    resultados = []  # Lista para almacenar los resultados
    while bajo <= alto:
        medio = (bajo + alto) // 2  # Calculamos el índice medio
        if key(arr[medio]) < objetivo:
            bajo = medio + 1  # Ajustamos el límite inferior
        elif key(arr[medio]) > objetivo:
            alto = medio - 1  # Ajustamos el límite superior
        else:
            # Si encontramos el objetivo, exploramos a izquierda y derecha para encontrar todos los elementos iguales
            izquierda = medio
            while izquierda >= 0 and key(arr[izquierda]) == objetivo:
                izquierda -= 1
            derecha = medio
            while derecha < len(arr) and key(arr[derecha]) == objetivo:
                derecha += 1
            # Agregamos los elementos encontrados a la lista de resultados
            resultados = arr[izquierda + 1:derecha]
            break
    return resultados  # Devolvemos la lista de resultados

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
