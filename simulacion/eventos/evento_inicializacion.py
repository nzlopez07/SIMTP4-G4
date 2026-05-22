from eventos import Evento
from ..estadisticas.vector_estado import FilaVectorEstado
# importar GeneradorVariablesAleatorias
from evento_llegada import EventoLlegada

class EventoInicializacion(Evento):
    def __init__(self, tiempo):
        super().__init__(tiempo, "Inicialización")

    def ejecutar(self, motor):
        primera_fila = FilaVectorEstado()
        primera_fila.iteracion = 1
        primera_fila.hora_simulada = 9.0
        primera_fila.evento_simulado = self.nombre

        # Generar un RND para la llegada del primer auto
        primera_fila.rndLlegada = motor.generarRND()
        # Calcular el tiempo de llegada del primer auto
        #primera_fila.tiempoLlegada = generador.tiempoLlegada(primera_fila.rndLlegada) + self.tiempo

        # Agregar el evento a la cola
        motor.calendario.agregar_evento(EventoLlegada(primera_fila.tiempoLlegada))

        # Agregar la fila al vector de estado
        motor.agregar_fila_vector(primera_fila)