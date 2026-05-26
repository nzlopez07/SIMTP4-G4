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

        # Copiar stats acumuladas del dia anterior; no crear fila vacia
        self._nueva_fila = self._copiar_fila(fila_anterior)
        self._nueva_fila.iteracion = fila_anterior.iteracion + 1
        self._nueva_fila.hora_simulada = self.tiempo
        self._nueva_fila.evento_simulado = self.nombre

        # Estado transitorio que empieza limpio en cada jornada
        self._nueva_fila.tunel = TunelLavado()
        self._nueva_fila.puestoAspirado1 = PuestoAspirado(1)
        self._nueva_fila.puestoAspirado2 = PuestoAspirado(2)
        self._nueva_fila.colaLavado = ColaLavado()
        self._nueva_fila.tiempoInicioBloqueoTunel = None

        # Columnas de evento: solo rndLlegada y tiempoLlegada se rellenan aqui
        self._nueva_fila.rndLavado = None
        self._nueva_fila.tiempoLavado = None
        self._nueva_fila.rndFlagAspirado = None
        self._nueva_fila.flagAspirado = None
        self._nueva_fila.rndAspirado1 = None
        self._nueva_fila.tiempoAspirado1 = None
        self._nueva_fila.rndAspirado2 = None
        self._nueva_fila.tiempoAspirado2 = None
        self._nueva_fila.accionLlegada = ""

        generador = GestorVariablesAleatorias()
        self._nueva_fila.rndLlegada = motor.generarRND()
        self._nueva_fila.tiempoLlegada = self.tiempo + generador.tiempoLlegada(self._nueva_fila.rndLlegada)

    def _generar_eventos(self, motor):
        motor.calendario.agregar_evento(EventoLlegada(self._nueva_fila.tiempoLlegada))

    def _actualizar_estadisticas(self, motor):
        motor.registro.registrar_jornada(self.tiempo)
        motor.agregar_fila_vector(self._nueva_fila)
