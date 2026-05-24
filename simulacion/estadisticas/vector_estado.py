"""Estructuras para el vector de estado de la simulacion."""

from collections import deque
from datetime import datetime, time, timedelta

from simulacion.objetos import PuestoAspirado, TunelLavado


class FilaVectorEstado:
    """Representa una fila del vector de estado de la simulacion."""

    def __init__(self):
        self.iteracion = 0
        self.hora_simulada = 0.0
        self.evento_simulado = ""

        self.rndLlegada = None
        self.tiempoLlegada = None
        self.accionLlegada = ""
        self.rndLavado = None
        self.tiempoLavado = None
        self.rndFlagAspirado = None
        self.flagAspirado = None
        self.rndAspirado1 = None
        self.tiempoAspirado1 = None
        self.rndAspirado2 = None
        self.tiempoAspirado2 = None

        self.contadorAutos = 0
        self.colaAutos = 0
        self.autos = deque()

        self.clientesPerdidos = 0
        self.tiempoInicioBloqueoTunel = None
        self.tiempoTunelBloqueado = timedelta(0)
        self.tiempoFinSimulacion = None
        self.tiempoHorasExtras = timedelta(0)

        self.tunel: TunelLavado = None
        self.puestoAspirado1: PuestoAspirado = None
        self.puestoAspirado2: PuestoAspirado = None

    def como_dict(self):
        return {
            "iteracion": self.iteracion,
            "hora_simulada": self._serializar_valor(self.hora_simulada),
            "evento_simulado": self.evento_simulado,
            "rnd_llegada": self.rndLlegada,
            "tiempo_llegada": self._serializar_valor(self.tiempoLlegada),
            "accion_llegada": self.accionLlegada,
            "rnd_lavado": self.rndLavado,
            "tiempo_lavado": self._serializar_valor(self.tiempoLavado),
            "rnd_flag_aspirado": self.rndFlagAspirado,
            "flag_aspirado": self.flagAspirado,
            "rnd_aspirado_1": self.rndAspirado1,
            "tiempo_aspirado_1": self._serializar_valor(self.tiempoAspirado1),
            "rnd_aspirado_2": self.rndAspirado2,
            "tiempo_aspirado_2": self._serializar_valor(self.tiempoAspirado2),
            "contador_autos": self.contadorAutos,
            "cola_autos": self.colaAutos,
            "clientes_perdidos": self.clientesPerdidos,
            "tiempo_inicio_bloqueo_tunel": self._serializar_valor(
                self.tiempoInicioBloqueoTunel
            ),
            "tiempo_tunel_bloqueado": self._serializar_valor(self.tiempoTunelBloqueado),
            "tiempo_fin_simulacion": self._serializar_valor(self.tiempoFinSimulacion),
            "tiempo_horas_extras": self._serializar_valor(self.tiempoHorasExtras),
        }

    def _serializar_valor(self, valor):
        if isinstance(valor, datetime):
            return valor.isoformat()

        if isinstance(valor, time):
            return valor.isoformat()

        if isinstance(valor, timedelta):
            return valor.total_seconds() / 60

        return valor


class VectorEstado:
    """Historial completo de filas generadas por la simulacion."""

    def __init__(self):
        self.filas = []

    def agregar(self, fila):
        self.filas.append(fila)

    def getAnterior(self):
        if len(self.filas) < 2:
            raise Exception("Aun no existe vector estado anterior")
        return self.filas[-2]

    def getActual(self):
        if len(self.filas) == 0:
            raise Exception("No hay ningun vector estado")
        return self.filas[-1]

    def __len__(self):
        return len(self.filas)

    def __iter__(self):
        return iter(self.filas)
