"""Estructuras para el vector de estado de la simulacion."""
from collections import deque   # deque es una cola FIFO


class FilaVectorEstado:
    """Representa una fila del vector de estado de la simulacion."""

    def __init__(self):
        self.iteracion = 0
        self.hora_simulada = 0.0
        self.evento_simulado = ""
        
        self.rndLlegada
        self.tiempoLlegada
        self.accionLlegada = "" # A<id> ingresa | A<id> se retira  (cliente perdido)
        self.rndLavado
        self.tiempoLavado
        self.rndFlagAspirado
        self.flagAspirado
        self.rndAspirado1
        self.tiempoAspirado1
        self.rndAspirado2
        self.tiempoAspirado2
               
        self.contadorAutos = 0  # este contador sirve para generar los id de los autos
        self.colaAutos = 0
        self.autos = deque()

        self.clientesPerdidos = 0
        self.tiempoHorasExtras = 0.0
        self.tiempoTunelBloqueado = 0.0 # El porcentaje se calculará al final de la simulacion


        # self.proximos_eventos = [] # Está el 'calendario' para esto
        self.objetos = {}
        self.variables_auxiliares = {}
        
        #self.rnd_usados = {} # No se usa, ya están los atributos rnd específicos

    def agregar_proximo_evento(self, evento):
        self.proximos_eventos.append(evento)

    def agregar_objeto(self, nombre, estado=None, atributos=None):
        if atributos is None:
            atributos = {}

        self.objetos[nombre] = {
            "estado": estado,
            "atributos": atributos,
        }

    def agregar_variable_auxiliar(self, nombre, valor):
        self.variables_auxiliares[nombre] = valor

    def agregar_rnd(self, nombre, valor):
        self.rnd_usados[nombre] = valor

    def como_dict(self):
        return {
            "iteracion": self.iteracion,
            "hora_simulada": self.hora_simulada,
            "evento_simulado": self.evento_simulado,
            "proximos_eventos": list(self.proximos_eventos),
            "objetos": self.objetos,
            "variables_auxiliares": self.variables_auxiliares,
            "rnd_usados": self.rnd_usados,
        }


class VectorEstado:
    """Contenedor del historial de filas del vector de estado."""

    def __init__(self):
        self.filas = []

    def agregar(self, fila):
        self.filas.append(fila)

    def obtener(self, indice):
        return self.filas[indice]

    def quitar(self, indice):
        return self.filas.pop(indice)

    def buscar(self, criterio): ##Acá criterio sería una lambda function que recibe una fila y devuelve True si cumple la condición de búsqueda
        return [fila for fila in self.filas if criterio(fila)]

    def buscar_por_iteracion(self, iteracion):
        for fila in self.filas:
            if fila.iteracion == iteracion:
                return fila
        return None

    def limpiar(self):
        self.filas.clear()

    def __len__(self):
        return len(self.filas)

    def __iter__(self):
        return iter(self.filas)
    

    ##Pendiente a decidir según lo que diga el profe