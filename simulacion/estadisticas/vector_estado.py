"""Estructuras para el vector de estado de la simulacion."""
from collections import deque   # deque es una cola FIFO

from simulacion.objetos import TunelLavado, PuestoAspirado


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

        self.tunel: TunelLavado
        self.puestoAspirado1: PuestoAspirado
        self.puestoAspirado2: PuestoAspirado


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
        """
        Con esto nos aseguramos que en memoria solo tendremos como máximo 2 vectores estados (Anterior y Actual)
            filas[0] - vectorEstadoAnterior
            filas[1] - vectorEstadoActual
        """
        if len(self.filas) <= 1:
            return self.filas.append(fila)

        self.filas[0] = self.filas[1]
        self.filas[1] = fila

    def getAnterior(self):
        if len(self.filas) == 0:
            raise Exception("No hay ningún vector estado")
        if len(self.filas) == 1:
            raise Exception("Aún no existe vector estado anterior")
        return self.filas[0]

    def getActual(self):
        if len(self.filas) == 0:
            raise Exception("No hay ningún vector estado")
        if len(self.filas) == 1:
            return self.filas[0]
        return self.filas[1]