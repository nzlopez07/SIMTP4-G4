class Auto:
    """Representa un vehículo en la simulación."""
    def __init__(self, id, horaLlegada, estado="", requiereAspirado=None):
        self.id = id  # Identificador único del auto
        self.estado = estado  # Estado actual del auto - EnCola | EnLavado | EsperandoAspirado | EnAspirado
        self.requiereAspirado = requiereAspirado  # Indica si el auto requiere aspirado (True/False)
        self.horaLlegada = horaLlegada  # Hora de llegada del auto al lavadero
