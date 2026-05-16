class Auto:
    """Representa un vehículo en la simulación."""
    def __init__(self):
        self.id = None  # Identificador único del auto
        self.estado = None  # Estado actual del auto (ej. 'esperando', 'lavando', 'aspirando', etc.)
        self.requiereAspirado = None  # Indica si el auto requiere aspirado (True/False)
        self.horaLlegada = None  # Hora de llegada del auto al lavadero
    pass


class ColaLavado:
    """Cola FIFO para el túnel de lavado."""
    def __init__(self):
        self.autos: list[Auto] = []  # vector de autos en la cola.
        self.capacidadMaxima = None  # es un numero fijo para nuestro dominio = 5
    pass


class TunelLavado:
    """Recurso que representa el túnel de lavado."""
    def __init__(self):
        self.estado = None  # Libre | Ocupado | Bloqueado (se puede hacer un patron de estado para si esta libre ocupado o bloqueado y generar las funciones esLibre esOcupado etc)
        self.auto_actual: Auto = None  # id del auto
    pass


class PuestoAspirado:
    """Recurso que representa un puesto de aspirado."""
    def __init__(self):
        self.id = None 
        self.auto_actual: Auto = None  # id del auto que determina si esta libre o ocupado
    pass
