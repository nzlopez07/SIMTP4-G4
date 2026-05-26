"""Estructuras para el vector de estado de la simulacion."""

from datetime import datetime, timedelta

from simulacion.objetos import ColaLavado, PuestoAspirado, TunelLavado


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


def _serializar_auto(auto):
    if auto is None:
        return None
    return f"A{auto.id} ({auto.estado})"


def _serializar_autos(autos):
    return ", ".join(_serializar_auto(auto) for auto in autos)


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
        self.tiempoFinBloqueoTunel = None
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
            "cola_autos_detalle": _serializar_autos(self.colaLavado.autos),
            "tunel_estado": self.tunel.estado if self.tunel is not None else None,
            "tunel_auto_actual": _serializar_auto(self.tunel.auto_actual) if self.tunel is not None else None,
            "tunel_hora_inicio_bloqueo": _serializar(self.tunel.horaInicioBloqueado) if self.tunel is not None else None,
            "puesto_aspirado_1_estado": self.puestoAspirado1.estado if self.puestoAspirado1 is not None else None,
            "puesto_aspirado_1_auto_actual": _serializar_auto(self.puestoAspirado1.auto_actual) if self.puestoAspirado1 is not None else None,
            "puesto_aspirado_2_estado": self.puestoAspirado2.estado if self.puestoAspirado2 is not None else None,
            "puesto_aspirado_2_auto_actual": _serializar_auto(self.puestoAspirado2.auto_actual) if self.puestoAspirado2 is not None else None,
            "tunel_bloqueado": self.tunel.esta_bloqueado() if self.tunel is not None else False,
            "tiempo_inicio_bloqueo_tunel": _serializar(self.tiempoInicioBloqueoTunel),
            "tiempo_fin_bloqueo_tunel": _serializar(self.tiempoFinBloqueoTunel),
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
