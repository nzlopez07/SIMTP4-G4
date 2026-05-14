"""Entidades dinámicas y recursos del lavadero (esqueleto)."""


class Auto:
    """Representa un vehículo en la simulación."""
    def __init__(self):
        self.id = None  # Identificador único del auto
        self.estadoActual = None  # Estado actual del auto (ej. 'esperando', 'lavando', 'aspirando', etc.)
        self.requiereAspirado = None  # Indica si el auto requiere aspirado (True/False)
        self.horaLlegada = None  # Hora de llegada del auto al lavadero
    pass


class ColaLavado:
    """Cola FIFO para el túnel de lavado."""
    pass


class TunelLavado:
    """Recurso que representa el túnel de lavado."""
    pass


class PuestoAspirado:
    """Recurso que representa un puesto de aspirado."""
    pass
