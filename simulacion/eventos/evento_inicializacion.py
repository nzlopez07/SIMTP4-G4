from datetime import datetime, time

from simulacion.estadisticas import FilaVectorEstado
from simulacion.eventos.evento import Evento
from simulacion.eventos.evento_llegada import EventoLlegada
from simulacion.generador_variables_aleatorias import GestorVariablesAleatorias
from simulacion.objetos import PuestoAspirado, TunelLavado


class EventoInicializacion(Evento):
    """Evento inicial: crea la primera fila y agenda la primera llegada."""

    def __init__(self):
        tiempo = datetime.combine(datetime.now(), time(9, 0, 0))
        super().__init__(tiempo, "Inicializacion")

    def _ejecutar(self, motor):
        self.fila_actual = FilaVectorEstado()
        self._preparar_fila(self.fila_actual)

        self.fila_actual.tunel = TunelLavado()
        self.fila_actual.puestoAspirado1 = PuestoAspirado(1)
        self.fila_actual.puestoAspirado2 = PuestoAspirado(2)

    def _generar_eventos(self, motor):
        generador = GestorVariablesAleatorias()

        self.fila_actual.rndLlegada = motor.generarRND()
        self.fila_actual.tiempoLlegada = self.tiempo + generador.tiempoLlegada(
            self.fila_actual.rndLlegada
        )

        motor.calendario.agregar_evento(EventoLlegada(self.fila_actual.tiempoLlegada))
