"""Estructuras para el vector de estado de la simulacion."""

from datetime import datetime, timedelta

from simulacion.objetos import ColaLavado, PuestoAspirado, TunelLavado


def _serializar(valor):
    """Convierte valores del vector a tipos simples para JSON."""
    if isinstance(valor, datetime):
        return valor.strftime("%H:%M:%S")
    if isinstance(valor, timedelta):
        minutos = valor.total_seconds() / 60
        if minutos.is_integer():
            return int(minutos)
        return round(minutos, 2)
    return valor


def _serializar_auto(auto):
    if auto is None:
        return None

    return {
        "id": auto.id,
        "estado": auto.estado,
        "requiere_aspirado": auto.requiereAspirado,
        "hora_llegada": _serializar(auto.horaLlegada),
    }


def _serializar_tunel(tunel):
    if tunel is None:
        return None

    return {
        "estado": tunel.estado,
        "auto_actual": _serializar_auto(tunel.auto_actual),
        "hora_inicio_bloqueado": _serializar(tunel.horaInicioBloqueado),
    }


def _serializar_puesto(puesto):
    if puesto is None:
        return None

    return {
        "id": puesto.id,
        "estado": puesto.estado,
        "auto_actual": _serializar_auto(puesto.auto_actual),
    }


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
        self.colaLavado = ColaLavado()

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
            "tiempo_aspirado_2": _serializar(self.tiempoAspirado2),
            "contador_autos": self.contadorAutos,
            "cola_autos": len(self.colaLavado.autos),
            "clientes_perdidos": self.clientesPerdidos,
            "tiempo_horas_extras": _serializar(self.tiempoHorasExtras),
            "tiempo_tunel_bloqueado": _serializar(self.tiempoTunelBloqueado),
            "tunel": _serializar_tunel(self.tunel),
            "puesto_aspirado_1": _serializar_puesto(self.puestoAspirado1),
            "puesto_aspirado_2": _serializar_puesto(self.puestoAspirado2),
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
