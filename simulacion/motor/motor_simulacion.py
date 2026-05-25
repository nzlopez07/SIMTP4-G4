import random
from datetime import datetime, date, time, timedelta

from simulacion.estadisticas.vector_estado import VectorEstado
from simulacion.estadisticas.registro_estadisticas import RegistroEstadisticas
from simulacion.motor.calendario_eventos import CalendarioEventos


class MotorSimulacion:
    """Nucleo que controlara la simulacion."""

    def __init__(self, seed: int | None = None, hora_fin: str | None = None, cant_sim: int | None = None, vector_estado: VectorEstado | None = None,
                 calendario: CalendarioEventos | None = None, registro: RegistroEstadisticas | None = None):
        seed     = int(seed)      if seed      not in (None, "") else None
        cant_sim = int(cant_sim)  if cant_sim  not in (None, "") else None

        self._seed = seed
        self._hora_fin = hora_fin if hora_fin not in (None, "") else None
        self._cant_sim = cant_sim
        self._vector_estado = vector_estado or VectorEstado()
        self._calendario = calendario or CalendarioEventos()
        self._registro = registro or RegistroEstadisticas()

        self._fila_anterior = None
        self._fila_actual = None

        # Punto de fin absoluto: hora_fin se interpreta como horas corridas desde medianoche del día de inicio. "21:00" con fin a las 21:00 del día 1;
        # "72:00" con fin a medianoche del día 4 (3 días completos de servicio).
        self._datetime_fin = self._calcular_datetime_fin()

        if seed is not None:
            random.seed(seed)

    def _calcular_datetime_fin(self) -> datetime | None:
        if self._hora_fin is None:
            return None
        partes = self._hora_fin.split(":")
        horas   = int(partes[0])
        minutos = int(partes[1]) if len(partes) > 1 else 0
        segundos = int(partes[2]) if len(partes) > 2 else 0
        midnight = datetime.combine(date.today(), time(0, 0, 0))
        return midnight + timedelta(hours=horas, minutes=minutos, seconds=segundos)

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
        self._registro.actualizar_horas_extras(fila)
        self._fila_anterior = self._fila_actual
        self._fila_actual = fila
        self._vector_estado.agregar(fila)

    def generarRND(self) -> float:
        return random.random()

    def ejecutar(self, max_iteraciones: int | None = None) -> None:
        from simulacion.eventos.evento_inicializacion import EventoInicializacion

        if max_iteraciones is not None:
            self._cant_sim = max_iteraciones

        EventoInicializacion().procesar(self)

        while not self._calendario.esta_vacio():
            if self._condicion_de_parada_alcanzada():
                break
            evento = self._calendario.obtener_proximo()
            self._despachar(evento)

        self._finalizar()

    def _despachar(self, evento) -> None:
        evento.procesar(self)

    def _condicion_de_parada_alcanzada(self) -> bool:
        if self._cant_sim is not None and len(self._vector_estado) >= self._cant_sim:
            return True
        if self._datetime_fin is not None and len(self._vector_estado) > 0:
            if self._vector_estado.getActual().hora_simulada >= self._datetime_fin:
                return True
        return False

    def _finalizar(self) -> None:
        if len(self._vector_estado) == 0:
            return
        fila_final = self._vector_estado.getActual()
        hora_cierre = self._resolver_hora_cierre()
        self._registro.registrar_fin_simulacion(fila_final.hora_simulada, hora_cierre, fila_final)

    def _resolver_hora_cierre(self) -> datetime:
        if self._datetime_fin is not None:
            return self._datetime_fin
        return datetime.combine(date.today(), time(21, 0, 0))