class Auto:
    """Representa un vehículo en la simulación."""
    def __init__(self):
        self.id = None  # Identificador único del auto
        self.estado = None  # Estado actual del auto (ej. 'esperando', 'lavando', 'aspirando', etc.)
        self.requiereAspirado = None  # Indica si el auto requiere aspirado (True/False)
        self.horaLlegada = None  # Hora de llegada del auto al lavadero
    pass
