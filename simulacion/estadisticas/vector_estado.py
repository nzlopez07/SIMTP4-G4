"""Estructuras para el vector de estado de la simulacion."""

from collections import deque
from datetime import datetime, timedelta

from simulacion.objetos import PuestoAspirado, TunelLavado


def _serializar(valor):
    """Convierte datetime y timedelta a str para JSON."""
    if isinstance(valor, datetime):
        return valor.strftime("%H:%M:%S")
    if isinstance(valor, timedelta):
        total = int(valor.total_seconds())
        h, rem = divmod(total, 3600)
        m, s = divmod(rem, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
    return valor


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
        self.tiempoFinSimulacion = None
        self.tiempoHorasExtras = timedelta(0)
        self.tiempoTunelBloqueado = timedelta(0)

        self.tunel: TunelLavado = None
        self.puestoAspirado1: PuestoAspirado = None
        self.puestoAspirado2: PuestoAspirado = None

    def como_dict(self):
        return {
            "iteracion": self.iteracion,
            "hora_simulada": _serializar(self.hora_simulada),
            "evento_simulado": self.evento_simulado,
            "rnd_llegada": self.rndLlegada,
            "tiempo_llegada": _serializar(self.tiempoLlegada),
            "accion_llegada": self.accionLlegada,
            "rnd_lavado": self.rndLavado,
            "tiempo_lavado": _serializar(self.tiempoLavado),
            "rnd_flag_aspirado": self.rndFlagAspirado,
            "flag_aspirado": self.flagAspirado,
            "rnd_aspirado_1": self.rndAspirado1,
            "tiempo_aspirado_1": _serializar(self.tiempoAspirado1),
            "rnd_aspirado_2": self.rndAspirado2,
            "tiempo_aspirado_2": self.tiempoAspirado2,
            "contador_autos": self.contadorAutos,
            "cola_autos": self.colaAutos,
            "clientes_perdidos": self.clientesPerdidos,
            "tiempo_horas_extras": _serializar(self.tiempoHorasExtras),
            "tiempo_tunel_bloqueado": _serializar(self.tiempoTunelBloqueado),
        }

class VectorEstado:
    """Historial completo de filas generadas por la simulacion."""

    def __init__(self):
        self.filas = []

    def agregar(self, fila):
        self.filas.append(fila)

    def getActual(self):
        if len(self.filas) == 0:
            raise Exception("No hay ningun vector estado")
        return self.filas[-1]

    def __len__(self):
        return len(self.filas)

    def __iter__(self):
        return iter(self.filas)
