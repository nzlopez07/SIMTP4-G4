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
    assert motor.fila_actual.evento_simulado == "Llegada"
    assert motor.fila_actual.tunel.estado == "Ocupado"
    assert motor.fila_actual.tiempoLavado is not None
