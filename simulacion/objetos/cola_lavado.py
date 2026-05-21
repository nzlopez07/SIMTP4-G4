class ColaLavado:
    """Cola FIFO para el túnel de lavado."""
    def __init__(self):
        self.autos: list[Auto] = []  # vector de autos en la cola.
        self.capacidadMaxima = 5  # es un numero fijo para nuestro dominio = 5
    

    def esta_llena(self):
        """Indica si la cola de lavado está llena."""
        return len(self.autos) >= self.capacidadMaxima
    
    def esta_bloqueada(self):
        """Indica si el túnel de lavado está bloqueado (capacidad máxima alcanzada)."""
        return self.esta_llena()
    
    def encolar_auto(self, auto):
        """Agrega un auto a la cola de lavado."""
        if self.esta_llena():
            raise Exception("No se puede encolar: la cola de lavado está llena.")
        self.autos.append(auto)

    def desencolar_auto(self):
        """Remueve y devuelve el auto al frente de la cola de lavado."""
        if not self.autos:
            raise Exception("No se puede desencolar: la cola de lavado está vacía.")
        return self.autos.pop(0)