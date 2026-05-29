from simulacion.eventos import EventoInicializacion
from simulacion.motor import MotorSimulacion


def test_inicializacion_crea_primera_fila_y_agenda_llegada():
    motor = MotorSimulacion(seed=1)

    EventoInicializacion().procesar(motor)

    assert len(motor.vector_estado.filas) == 1
    assert motor.fila_actual.evento_simulado == "Inicializacion"
    assert motor.fila_actual.tunel.esta_libre()
    assert len(motor.calendario._eventos) == 1


def test_llegada_modifica_fila_actual_sin_mutar_fila_anterior():
    motor = MotorSimulacion(seed=1)
    EventoInicializacion().procesar(motor)

    llegada = motor.calendario.obtener_proximo()
    llegada.procesar(motor)

    assert len(motor.vector_estado.filas) == 2
    assert motor.fila_anterior.evento_simulado == "Inicializacion"
    assert motor.fila_anterior.tunel.esta_libre()
    assert motor.fila_anterior.colaLavado is not motor.fila_actual.colaLavado
    assert motor.fila_actual.evento_simulado == "Llegada"
    assert motor.fila_actual.tunel.estado == "Ocupado"
    assert motor.fila_actual.tiempoLavado is not None


def test_historial_no_comparte_recursos_mutables_entre_filas():
    motor = MotorSimulacion(seed=42, cant_sim=80)

    motor.ejecutar()

    campos_mutables = (
        "colaLavado",
        "tunel",
        "puestoAspirado1",
        "puestoAspirado2",
    )

    for fila_anterior, fila_actual in zip(
        motor.vector_estado.filas,
        motor.vector_estado.filas[1:],
    ):
        for campo in campos_mutables:
            assert getattr(fila_anterior, campo) is not getattr(fila_actual, campo)


def test_fin_aspirado_limpia_inicio_de_bloqueo_al_desbloquear_tunel():
    motor = MotorSimulacion(seed=2, cant_sim=360)

    motor.ejecutar()

    filas_desbloqueadas = [
        fila
        for fila in motor.vector_estado.filas
        if fila.tiempoTunelBloqueado.total_seconds() > 0
        and not fila.tunel.esta_bloqueado()
    ]

    assert filas_desbloqueadas
    assert all(fila.tiempoInicioBloqueoTunel is None for fila in filas_desbloqueadas)


def test_fin_aspirado_registra_fin_de_bloqueo_al_desbloquear_tunel():
    motor = MotorSimulacion(seed=2, cant_sim=360)

    motor.ejecutar()

    filas_con_fin_bloqueo = [
        fila
        for fila in motor.vector_estado.filas
        if fila.tiempoFinBloqueoTunel is not None
    ]

    assert filas_con_fin_bloqueo
    assert all(fila.tiempoFinBloqueoTunel is not None for fila in filas_con_fin_bloqueo)
