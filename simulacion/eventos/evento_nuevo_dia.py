from datetime import datetime

from simulacion.eventos.evento import Evento
from simulacion.eventos.evento_llegada import EventoLlegada
from simulacion.objetos import ColaLavado, TunelLavado, PuestoAspirado
from simulacion.generador_variables_aleatorias import GestorVariablesAleatorias


class EventoNuevoDia(Evento):
    def __init__(self, tiempo: datetime):
        super().__init__(tiempo, "Nuevo día")
        self._nueva_fila = None

    def _ejecutar(self, motor):
        fila_anterior = motor.fila_actual
        self._nueva_fila = self._copiar_fila(fila_anterior)
        self._preparar_fila(self._nueva_fila, fila_anterior)

        generador = GestorVariablesAleatorias()
        self._nueva_fila.rndLlegada = motor.generarRND()
        self._nueva_fila.tiempoLlegada = self.tiempo + generador.tiempoLlegada(self._nueva_fila.rndLlegada)

    def _generar_eventos(self, motor):
        motor.calendario.agregar_evento(EventoLlegada(self._nueva_fila.tiempoLlegada))

    def _actualizar_estadisticas(self, motor):
        motor.agregar_fila_vector(self._nueva_fila)
