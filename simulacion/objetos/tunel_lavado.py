class TunelLavado:
    """Recurso que representa el túnel de lavado."""
    def __init__(self):
        self.estado = "Libre"  # Libre | Ocupado | Bloqueado (se puede hacer un patron de estado para si esta libre ocupado o bloqueado y generar las funciones esLibre esOcupado etc)
        self.auto_actual: Auto = None  # id del auto

    def esta_libre(self):
        """Indica si el túnel de lavado está libre."""
        # return self.auto_actual is None and self.estado != "Bloqueado"
        return self.estado == "Libre"
    
    def esta_bloqueado(self):
        """Indica si el túnel de lavado está bloqueado."""
        return self.estado == "Bloqueado"
    
    def ocupar(self, auto):
        """Ocupar el túnel de lavado con un auto."""
        if not self.esta_libre():
            raise Exception("No se puede ocupar: el túnel de lavado no está libre.")
        self.auto_actual = auto
        self.estado = "Ocupado"

    def liberar(self):
        """Liberar el túnel de lavado."""
        if self.auto_actual is None:
            raise Exception("No se puede liberar: el túnel de lavado ya está libre.")
        self.auto_actual = None
        self.estado = "Libre"

    def bloquear(self):
        """Bloquear el túnel de lavado."""
        self.auto_actual = None
        self.estado = "Bloqueado"