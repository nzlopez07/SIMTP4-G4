

class EventoInicializacion:
    def __init__(self, tiempo):
        self.tiempo = tiempo

    def ejecutar(self, simulacion):
        # Aquí puedes agregar la lógica de inicialización de la simulación
        print(f"Simulación inicializada en el tiempo {self.tiempo}")