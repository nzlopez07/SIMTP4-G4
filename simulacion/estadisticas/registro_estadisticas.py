from datetime import datetime, time, timedelta


class RegistroEstadisticas:
    """Calcula y consolida las metricas solicitadas por el enunciado."""

    def __init__(self):
        self.clientesPerdidos = 0
        self.tiempoInicioBloqueoTunel = None
        self.tiempoTunelBloqueado = timedelta(0)
        self.tiempoFinSimulacion = None
        self.tiempoHorasExtras = timedelta(0)
        self.cantidadJornadas = 0
        self._fechas_jornadas = set()
        self._fecha_inicio_overtime = None
        self._overtime_previo = timedelta(0)

    def registrar_jornada(self, tiempo_inicio=None) -> None:
        if isinstance(tiempo_inicio, datetime):
            fecha = tiempo_inicio.date()
            if fecha in self._fechas_jornadas:
                return

            self._fechas_jornadas.add(fecha)
            self.cantidadJornadas = len(self._fechas_jornadas)
            return

        if self.cantidadJornadas == 0:
            self.cantidadJornadas = 1

    def actualizar_horas_extras(self, fila) -> None:
        """Escribe tiempoHorasExtras en la fila si la hora simulada supera las 21:00."""
        if not isinstance(fila.hora_simulada, datetime):
            return

        self.registrar_jornada(fila.hora_simulada)

        fecha = fila.hora_simulada.date()
        cierre_hoy = datetime.combine(fecha, time(21, 0, 0))

        if fila.hora_simulada <= cierre_hoy:
            return

        if self._fecha_inicio_overtime != fecha:
            # Primera vez que se cruza las 21:00 en este día: guardar el acumulado previo
            self._fecha_inicio_overtime = fecha
            self._overtime_previo = fila.tiempoHorasExtras

        fila.tiempoHorasExtras = self._overtime_previo + (fila.hora_simulada - cierre_hoy)

    def registrar_cliente_perdido(self, fila=None):
        self.clientesPerdidos += 1

        if fila is not None:
            fila.clientesPerdidos = self.clientesPerdidos

    def iniciar_bloqueo_tunel(self, tiempo_inicio, fila=None):
        self.tiempoInicioBloqueoTunel = tiempo_inicio

        if fila is not None:
            fila.tiempoInicioBloqueoTunel = tiempo_inicio

    def finalizar_bloqueo_tunel(self, tiempo_fin, fila=None):
        tiempo_inicio = self.tiempoInicioBloqueoTunel

        if tiempo_inicio is None and fila is not None:
            tiempo_inicio = fila.tiempoInicioBloqueoTunel

        if tiempo_inicio is None and fila is not None and fila.tunel is not None:
            tiempo_inicio = fila.tunel.horaInicioBloqueado

        if tiempo_inicio is None:
            return

        duracion = tiempo_fin - tiempo_inicio
        self.tiempoTunelBloqueado += duracion
        self.tiempoInicioBloqueoTunel = None

        if fila is not None:
            fila.tiempoTunelBloqueado = self.tiempoTunelBloqueado
            fila.tiempoInicioBloqueoTunel = None

    def registrar_fin_simulacion(self, tiempo_fin_simulacion, tiempo_cierre, fila=None):
        self.tiempoFinSimulacion = tiempo_fin_simulacion

        if fila is not None:
            fila.tiempoFinSimulacion = tiempo_fin_simulacion
            self.actualizar_horas_extras(fila)
            self.tiempoHorasExtras = fila.tiempoHorasExtras
        else:
            self.tiempoHorasExtras = self._calcular_horas_extras(
                tiempo_fin_simulacion,
                tiempo_cierre,
            )

    def calcular_metricas_finales(
        self,
        fila,
        tiempo_inicio=None,
        tiempo_cierre=None,
        cantidad_jornadas=None,
    ):
        """Devuelve las tres metricas pedidas por la consigna."""
        tiempo_total = self._calcular_tiempo_total_simulacion(fila, tiempo_inicio)
        tiempo_bloqueado = fila.tiempoTunelBloqueado
        tiempo_horas_extras = fila.tiempoHorasExtras
        jornadas = self._resolver_cantidad_jornadas(
            cantidad_jornadas,
            fila,
            tiempo_inicio,
        )

        if (
            tiempo_cierre is not None
            and fila.tiempoFinSimulacion is not None
            and tiempo_horas_extras == timedelta(0)
        ):
            tiempo_horas_extras = self._calcular_horas_extras(
                fila.tiempoFinSimulacion,
                tiempo_cierre,
            )

        tiempo_promedio_horas_extras = tiempo_horas_extras / jornadas

        return {
            "clientes_perdidos_por_capacidad": fila.clientesPerdidos,
            "porcentaje_tiempo_tunel_bloqueado": self._calcular_porcentaje(
                tiempo_bloqueado,
                tiempo_total,
            ),
            "tiempo_horas_extras": tiempo_horas_extras,
            "tiempo_horas_extras_minutos": self._a_minutos(tiempo_horas_extras),
            "tiempo_promedio_horas_extras": tiempo_promedio_horas_extras,
            "tiempo_promedio_horas_extras_minutos": self._a_minutos(
                tiempo_promedio_horas_extras,
            ),
            "cantidad_jornadas": jornadas,
        }

    def _calcular_tiempo_total_simulacion(self, fila, tiempo_inicio):
        if fila.tiempoFinSimulacion is None:
            return timedelta(0)

        if tiempo_inicio is None:
            tiempo_inicio = self._inicio_desde_fin(fila.tiempoFinSimulacion)

        return fila.tiempoFinSimulacion - tiempo_inicio

    def _calcular_horas_extras(self, tiempo_fin_simulacion, tiempo_cierre):
        if isinstance(tiempo_cierre, time):
            tiempo_cierre = datetime.combine(tiempo_fin_simulacion.date(), tiempo_cierre)

        if tiempo_fin_simulacion <= tiempo_cierre:
            return timedelta(0)

        return tiempo_fin_simulacion - tiempo_cierre

    def _calcular_porcentaje(self, parte, total):
        total_minutos = self._a_minutos(total)

        if total_minutos == 0:
            return 0

        return self._a_minutos(parte) / total_minutos * 100

    def _a_minutos(self, valor):
        if isinstance(valor, timedelta):
            return valor.total_seconds() / 60

        return valor

    def _resolver_cantidad_jornadas(self, cantidad_jornadas, fila, tiempo_inicio):
        if cantidad_jornadas is not None:
            return max(1, int(cantidad_jornadas))

        if self.cantidadJornadas > 0:
            return self.cantidadJornadas

        if isinstance(tiempo_inicio, datetime) and fila.tiempoFinSimulacion is not None:
            dias = (fila.tiempoFinSimulacion.date() - tiempo_inicio.date()).days + 1
            return max(1, dias)

        return 1

    def _inicio_desde_fin(self, tiempo_fin_simulacion):
        return datetime.combine(tiempo_fin_simulacion.date(), time(9, 0, 0))
