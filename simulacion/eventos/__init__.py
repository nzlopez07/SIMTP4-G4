"""Eventos de la simulación: clases base y específicas (esqueleto)."""


class Evento:
    """Clase base para eventos."""

    def __init__(self, tiempo=0):
        self.tiempo = tiempo

    def procesar(self, motor):
        """Procesa el evento sobre el `motor` (implementación en el futuro)."""
        raise NotImplementedError


class EventoLlegada(Evento):
    pass


class EventoFinLavado(Evento):
    pass


class EventoFinAspirado(Evento):
    pass
