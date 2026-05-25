from datetime import datetime, time, timedelta

from simulacion.estadisticas import FilaVectorEstado, RegistroEstadisticas


def test_fila_vector_estado_inicializa_acumuladores_estadisticos():
    fila = FilaVectorEstado()

    assert fila.clientesPerdidos == 0
    assert fila.tiempoInicioBloqueoTunel is None
    assert fila.tiempoTunelBloqueado == timedelta(0)
    assert fila.tiempoFinSimulacion is None
    assert fila.tiempoHorasExtras == timedelta(0)


def test_fila_vector_estado_serializa_tiempos_en_hh_mm_ss():
    fila = FilaVectorEstado()
    fila.tiempoTunelBloqueado = timedelta(minutes=15)
    fila.tiempoHorasExtras = timedelta(minutes=30)

    serializada = fila.como_dict()

    assert serializada["tiempo_tunel_bloqueado"] == "00:15:00"
    assert serializada["tiempo_horas_extras"] == "00:30:00"


def test_registro_estadisticas_calcula_metricas_finales_del_enunciado():
    fila = FilaVectorEstado()
    fila.clientesPerdidos = 3
    fila.tiempoTunelBloqueado = timedelta(minutes=45)
    fila.tiempoFinSimulacion = datetime(2026, 5, 24, 21, 30)
    fila.tiempoHorasExtras = timedelta(minutes=30)

    registro = RegistroEstadisticas()
    metricas = registro.calcular_metricas_finales(
        fila,
        tiempo_inicio=datetime(2026, 5, 24, 9, 0),
        tiempo_cierre=time(21, 0),
    )

    assert metricas["clientes_perdidos_por_capacidad"] == 3
    assert metricas["porcentaje_tiempo_tunel_bloqueado"] == 6
    assert metricas["tiempo_horas_extras"] == timedelta(minutes=30)
    assert metricas["tiempo_horas_extras_minutos"] == 30
