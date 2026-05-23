from datetime import datetime, time
from evento import Evento
from evento_llegada import EventoLlegada
from simulacion.estadisticas import FilaVectorEstado
from simulacion.objetos import TunelLavado, PuestoAspirado
# importar GeneradorVariablesAleatorias


class EventoInicializacion(Evento):
    def __init__(self):
        t = datetime.combine(datetime.now(), time(9,0,0))
        super().__init__(t, "Inicialización")

    def ejecutar(self, motor):
        primera_fila = FilaVectorEstado()
        primera_fila.iteracion = 1
        primera_fila.hora_simulada = self.tiempo
        primera_fila.evento_simulado = self.nombre

        primera_fila.tunel = TunelLavado()
        primera_fila.puestoAspirado1 = PuestoAspirado(1)
        primera_fila.puestoAspirado2 = PuestoAspirado(2)

        # Generar un RND para la llegada del primer auto
        primera_fila.rndLlegada = motor.generarRND()
        # Calcular el tiempo de llegada del primer auto | el generador retorna un timedelta
        #primera_fila.tiempoLlegada = self.tiempo + generador.tiempoLlegada(primera_fila.rndLlegada)

        # Agregar el evento a la cola
        motor.calendario.agregar_evento(EventoLlegada(primera_fila.tiempoLlegada))

        # Agregar la fila al vector de estado
        motor.agregar_fila_vector(primera_fila)