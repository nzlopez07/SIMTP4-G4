from collections import deque
from simulacion.objetos.auto import Auto


class ColaLavado:
    """Cola FIFO para el túnel de lavado."""

    CAPACIDAD_MAXIMA = 5

    def __init__(self):
        self.autos: deque[Auto] = deque()

    def esta_llena(self):
        """Indica si la cola de lavado está llena."""
        return len(self.autos) >= self.CAPACIDAD_MAXIMA

    def esta_vacia(self):
        return len(self.autos) == 0

    def encolar_auto(self, auto):
        """Agrega un auto a la cola de lavado."""
        if self.esta_llena():
            raise Exception("No se puede encolar: la cola de lavado está llena.")
        auto.estado = "EnCola"
        self.autos.append(auto)

    def desencolar_auto(self):
        """Remueve y devuelve el auto al frente de la cola de lavado."""
        if self.esta_vacia():
            raise Exception("No se puede desencolar: la cola de lavado está vacía.")
        return self.autos.popleft()

    def contar(self):
        """Cuenta la cantidad de autos en la cola"""
        return len(self.autos)

    def como_dict(self):
        while (i = 0; i < self.contar(); i++) {
            self.autos[i].como_dict()
        }