import random

from simulacion.estadisticas.vector_estado import VectorEstado
from simulacion.estadisticas.registro_estadisticas import RegistroEstadisticas
from simulacion.motor.calendario_eventos import CalendarioEventos


class MotorSimulacion:
    """Nucleo que controlara la simulacion."""

    def __init__(self, seed=None, hora_fin=None, cant_sim=None, vector_estado=None):
        if seed == "":
            seed = None

        if seed is None or isinstance(seed, int):
            random.seed(seed)

        self.seed = seed
        self.hora_fin = hora_fin
        self.cant_sim = cant_sim

        self.vector_estado = vector_estado if isinstance(vector_estado, VectorEstado) else VectorEstado()

        # Ventana operativa de dos filas para generar la siguiente iteracion.
        self.fila_anterior = None
        self.fila_actual = None

        # registro de metricas separado
        self.registro = RegistroEstadisticas()

        # reloj e iterador
        self.reloj = 0.0
        self.iteracion = 0

        # calendario/agenda de eventos
        self.calendario = CalendarioEventos()

    def agregar_fila_vector(self, fila):
        """Agregar una fila al vector de estado."""
        self.fila_anterior = self.fila_actual
        self.fila_actual = fila
        self.vector_estado.agregar(fila)

    def ejecutar(self, max_iteraciones=None, tiempo_max=None):
        """Bucle principal de la simulacion pendiente de implementacion."""
        raise NotImplementedError

    def generarRND(self):
        return random.random()
