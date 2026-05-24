class TunelLavado:
    """Recurso que representa el tunel de lavado."""

    def __init__(self):
        self.estado = "Libre"
        self.auto_actual = None
        self.horaInicioBloqueado = None

    def esta_libre(self):
        return self.estado == "Libre"

    def esta_bloqueado(self):
        return self.estado == "Bloqueado"

    def ocupar(self, auto):
        if not self.esta_libre():
            raise Exception("No se puede ocupar: el tunel de lavado no esta libre.")

        self.auto_actual = auto
        self.estado = "Ocupado"

    def liberar(self):
        if self.auto_actual is None:
            raise Exception("No se puede liberar: el tunel de lavado ya esta libre.")

        self.auto_actual = None
        self.estado = "Libre"
        self.horaInicioBloqueado = None

    def bloquear(self, tiempo_inicio):
        self.estado = "Bloqueado"
        self.horaInicioBloqueado = tiempo_inicio
