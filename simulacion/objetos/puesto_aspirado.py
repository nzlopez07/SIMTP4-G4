class PuestoAspirado:
    """Recurso que representa un puesto de aspirado."""
    def __init__(self):
        self.id = None 
        self.auto_actual: Auto = None  # id del auto que determina si esta libre o ocupado
    
    def esta_libre(self):
        """Indica si el puesto de aspirado está libre."""
        return self.auto_actual is None
    
    def ocupar(self, auto):
        """Ocupar el puesto de aspirado con un auto."""
        if not self.esta_libre():
            raise Exception("No se puede ocupar: el puesto de aspirado no está libre.")
        self.auto_actual = auto

    def liberar(self):
        """Liberar el puesto de aspirado."""
        if self.auto_actual is None:
            raise Exception("No se puede liberar: el puesto de aspirado ya está libre.")
        self.auto_actual = None