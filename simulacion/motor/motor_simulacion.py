import random
from datetime import datetime, time

from simulacion.estadisticas.vector_estado import VectorEstado
from simulacion.estadisticas.registro_estadisticas import RegistroEstadisticas
from simulacion.motor.calendario_eventos import CalendarioEventos


class MotorSimulacion:
    """Nucleo que controlara la simulacion."""

    def __init__(
        self,
        seed: int | None = None,
        hora_fin: str | None = None,
        cant_sim: int | None = None,
        vector_estado: VectorEstado | None = None,
        calendario: CalendarioEventos | None = None,
        registro: RegistroEstadisticas | None = None,
    ):
        self._seed = seed
        self._hora_fin = hora_fin
        self._cant_sim = cant_sim
        self._vector_estado = vector_estado or VectorEstado()
        self._calendario = calendario or CalendarioEventos()
        self._registro = registro or RegistroEstadisticas()

        self._fila_anterior = None
        self._fila_actual = None
        self._reloj = 0.0
        self._iteracion = 0

        if isinstance(seed, int):
            random.seed(seed)

    @property
    def fila_anterior(self):
        return self._fila_anterior

    @property
    def fila_actual(self):
        return self._fila_actual

    @property
    def vector_estado(self) -> VectorEstado:
        return self._vector_estado

    @property
    def calendario(self) -> CalendarioEventos:
        return self._calendario

    @property
    def registro(self) -> RegistroEstadisticas:
        return self._registro

    @property
    def cant_sim(self) -> int | None:
        return self._cant_sim

    @cant_sim.setter
    def cant_sim(self, value: int | None):
        self._cant_sim = value

    @property
    def hora_fin(self) -> str | None:
        return self._hora_fin

    def agregar_fila_vector(self, fila) -> None:
        """Desplaza la ventana deslizante y registra la fila en el historial."""
        self._fila_anterior = self._fila_actual
        self._fila_actual = fila
        self._vector_estado.agregar(fila)

    def generarRND(self) -> float:
        return random.random()

    def ejecutar(self, max_iteraciones: int | None = None, tiempo_max=None) -> None:
        from simulacion.eventos.evento_inicializacion import EventoInicializacion
        from simulacion.eventos.evento_llegada import EventoLlegada

        if max_iteraciones is not None:
            self._cant_sim = max_iteraciones

        EventoInicializacion().ejecutar(self)

        while not self._calendario.esta_vacio():
            if self._condicion_de_parada_alcanzada():
                break
            evento = self._calendario.obtener_proximo()
            self._despachar(evento)

        self._finalizar()

    def _despachar(self, evento) -> None:
        from simulacion.eventos.evento_llegada import EventoLlegada
        if isinstance(evento, EventoLlegada):
            evento.ejecutar(self, self._fila_actual)
        else:
            evento.procesar(self)

    def _condicion_de_parada_alcanzada(self) -> bool:
        if self._cant_sim is not None:
            return len(self._vector_estado) >= self._cant_sim
        return False

    def _finalizar(self) -> None:
        if len(self._vector_estado) == 0:
            return
        fila_final = self._vector_estado.getActual()
        hora_cierre = self._resolver_hora_cierre()
        self._registro.registrar_fin_simulacion(fila_final.hora_simulada, hora_cierre)

    def _resolver_hora_cierre(self) -> datetime:
        if self._hora_fin is None:
            return datetime.combine(datetime.today(), time(21, 0, 0))
        h, m, s = map(int, self._hora_fin.split(":"))
        return datetime.combine(datetime.today(), time(h, m, s))
