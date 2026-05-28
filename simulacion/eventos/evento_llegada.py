from datetime import time, timedelta

from simulacion.eventos.evento import Evento
from simulacion.eventos.evento_fin_lavado import EventoFinLavado
from simulacion.generador_variables_aleatorias import GestorVariablesAleatorias
from simulacion.objetos import Auto


class EventoLlegada(Evento):
    """Evento que procesa la llegada de un auto al lavadero."""

    HORA_CIERRE = time(21, 0, 0)

    def __init__(self, tiempo):
        super().__init__(tiempo, "Llegada")
        self.fila_actual = None
        self._fila_anterior = None
        self._auto = None
        self._generador = None
        self._termino_anticipado = False

    def _ejecutar(self, motor):
        self._fila_anterior = motor.fila_actual
        self.fila_actual = self._copiar_fila(self._fila_anterior)
        self._preparar_fila(self.fila_actual, self._fila_anterior)

        if self.tiempo.time() >= time(21, 0, 0):
            self.fila_actual.accionLlegada = "Fuera de horario"
            self.fila_actual.tiempoLlegada = None
            self._termino_anticipado = True
            return

        self.fila_actual.contadorAutos = self._fila_anterior.contadorAutos + 1
        id = self.fila_actual.contadorAutos
        self._auto = Auto(id, self.tiempo)

        self._generador = GestorVariablesAleatorias()
        self.fila_actual.rndLlegada = motor.generarRND()
        self.fila_actual.tiempoLlegada = self.tiempo + self._generador.tiempoLlegada(self.fila_actual.rndLlegada)
        motor.calendario.agregar_evento(EventoLlegada(self.fila_actual.tiempoLlegada))

        if self._fila_anterior.colaLavado.esta_llena():
            self.fila_actual.accionLlegada = f"A{id} se retira"
            self.fila_actual.clientesPerdidos = self._fila_anterior.clientesPerdidos + 1
            self._termino_anticipado = True
            return

        self.fila_actual.accionLlegada = f"A{id} ingresa"

    def _generar_eventos(self, motor):
        if self._termino_anticipado:
            if self.fila_actual.accionLlegada == "Fuera de horario":
                from simulacion.eventos.evento_nuevo_dia import EventoNuevoDia
                siguiente_dia = (self.tiempo + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
                motor.calendario.agregar_evento(EventoNuevoDia(siguiente_dia))
            return

        if not self._fila_anterior.tunel.esta_libre():
            self.fila_actual.colaLavado.encolar_auto(self._auto)
        else:
            self._auto.estado = "EnLavado"
            self.fila_actual.tunel.ocupar(self._auto)
            self.fila_actual.rndLavado = motor.generarRND()
            self.fila_actual.tiempoLavado = self.tiempo + self._generador.tiempoLavado(self.fila_actual.rndLavado)
            motor.calendario.agregar_evento(EventoFinLavado(self.fila_actual.tiempoLavado))

    def _actualizar_estadisticas(self, motor):
        motor.agregar_fila_vector(self.fila_actual)
