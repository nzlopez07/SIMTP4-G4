from datetime import datetime

from simulacion.eventos.evento import Evento
from simulacion.eventos.evento_llegada import EventoLlegada
from simulacion.estadisticas import FilaVectorEstado
from simulacion.objetos import TunelLavado, PuestoAspirado
from simulacion.generador_variables_aleatorias import GestorVariablesAleatorias


class EventoNuevoDia(Evento):
    def __init__(self, tiempo: datetime):
        super().__init__(tiempo, "Nuevo día")
        self._nueva_fila = None

    def _ejecutar(self, motor):
        fila_anterior = motor.fila_actual

        self._nueva_fila = FilaVectorEstado()
        self._nueva_fila.iteracion = fila_anterior.iteracion + 1
        self._nueva_fila.hora_simulada = self.tiempo
        self._nueva_fila.evento_simulado = self.nombre

        self._nueva_fila.tunel = TunelLavado()
        self._nueva_fila.puestoAspirado1 = PuestoAspirado(1)
        self._nueva_fila.puestoAspirado2 = PuestoAspirado(2)

        generador = GestorVariablesAleatorias()
        self._nueva_fila.rndLlegada = motor.generarRND()
        self._nueva_fila.tiempoLlegada = self.tiempo + generador.tiempoLlegada(self._nueva_fila.rndLlegada)

    def _generar_eventos(self, motor):
        motor.calendario.agregar_evento(EventoLlegada(self._nueva_fila.tiempoLlegada))

    def _actualizar_estadisticas(self, motor):
        motor.agregar_fila_vector(self._nueva_fila)
