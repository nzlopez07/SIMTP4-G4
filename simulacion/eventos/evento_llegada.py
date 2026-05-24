from datetime import time

from simulacion.eventos.evento import Evento
from simulacion.eventos.evento_fin_lavado import EventoFinLavado
from simulacion.generador_variables_aleatorias import GestorVariablesAleatorias
from simulacion.objetos import Auto


class EventoLlegada(Evento):
    """Evento que procesa la llegada de un auto al lavadero."""

    HORA_CIERRE = time(21, 0, 0)

    def __init__(self, tiempo):
        super().__init__(tiempo, "Llegada")
        self.auto = None
        self.cliente_perdido = False

    def _ejecutar(self, motor):
        fila_anterior = self._obtener_fila_base(motor)
        self.fila_actual = self._copiar_fila(fila_anterior)
        self._preparar_fila(self.fila_actual, fila_anterior)

        if self._fuera_de_horario():
            self.fila_actual.accionLlegada = "Fuera de horario"
            return

        self.auto = self._crear_auto()

        if self.fila_actual.colaAutos >= 5:
            self._registrar_cliente_perdido()
            return

        self.fila_actual.accionLlegada = f"A{self.auto.id} ingresa"

        if self.fila_actual.tunel.esta_libre():
            self._iniciar_lavado(motor, self.auto)
        else:
            self._encolar_auto(self.auto)

    def _generar_eventos(self, motor):
        if self._fuera_de_horario():
            return

        self._generar_proxima_llegada(motor)

    def _actualizar_estadisticas(self, motor):
        if self.cliente_perdido:
            motor.registro.registrar_cliente_perdido()

        super()._actualizar_estadisticas(motor)

    def _crear_auto(self):
        self.fila_actual.contadorAutos += 1
        return Auto(self.fila_actual.contadorAutos, self.tiempo)

    def _registrar_cliente_perdido(self):
        self.auto.estado = "Retirado"
        self.cliente_perdido = True
        self.fila_actual.clientesPerdidos += 1
        self.fila_actual.accionLlegada = f"A{self.auto.id} se retira"

    def _encolar_auto(self, auto):
        auto.estado = "EnCola"
        self.fila_actual.colaAutos += 1
        self.fila_actual.autos.append(auto)

    def _iniciar_lavado(self, motor, auto):
        generador = GestorVariablesAleatorias()

        auto.estado = "EnLavado"
        self.fila_actual.tunel.ocupar(auto)
        self.fila_actual.rndLavado = motor.generarRND()
        self.fila_actual.tiempoLavado = self.tiempo + generador.tiempoLavado(
            self.fila_actual.rndLavado
        )

        motor.calendario.agregar_evento(EventoFinLavado(self.fila_actual.tiempoLavado))

    def _generar_proxima_llegada(self, motor):
        generador = GestorVariablesAleatorias()

        self.fila_actual.rndLlegada = motor.generarRND()
        self.fila_actual.tiempoLlegada = self.tiempo + generador.tiempoLlegada(
            self.fila_actual.rndLlegada
        )

        if self.fila_actual.tiempoLlegada.time() < self.HORA_CIERRE:
            motor.calendario.agregar_evento(EventoLlegada(self.fila_actual.tiempoLlegada))

    def _fuera_de_horario(self):
        return self.tiempo.time() >= self.HORA_CIERRE
