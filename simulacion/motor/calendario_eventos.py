import heapq

class CalendarioEventos:
    def __init__(self):
        self._eventos = []

    def agregar_evento(self,evento):
        heapq.heappush(self._eventos,evento)

    def obtener_proximo(self):
        return heapq.heappop(self._eventos) if self._eventos else None

    def esta_vacio(self):
        return len(self._eventos) == 0