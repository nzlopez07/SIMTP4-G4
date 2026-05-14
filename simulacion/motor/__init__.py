"""Esqueleto del Motor de Simulación."""

from ..estadisticas import VectorEstado, RegistroEstadisticas
from ..randoms import GeneradorAleatorio


class MotorSimulacion:
    """Núcleo que controlará la simulación.

    Ahora el motor puede recibir por inyección una instancia de GeneradorAleatorio
    y una instancia de VectorEstado (historial). Si no se proveen, se crean
    instancias por defecto.
    """

    def __init__(self, generador=None, vector_estado=None):
        # inyección de dependencias: generador de números y vector de estado
        self.generador = generador if generador is not None else GeneradorAleatorio()
        self.vector_estado = vector_estado if vector_estado is not None else VectorEstado()

        # registro de métricas separado
        self.registro = RegistroEstadisticas()

        # reloj e iterador
        self.reloj = 0.0
        self.iteracion = 0

        # calendario/agenda de eventos (se implementará aparte)
        self.calendario = None

    def agregar_fila_vector(self, fila):
        """Agregar una fila al vector de estado."""
        self.vector_estado.agregar(fila)

    def ejecutar(self, max_iteraciones=None, tiempo_max=None):
        """Bucle principal de la simulación (esqueleto).

        Por ahora es solo un stub; la implementación real iterará sobre el
        calendario de eventos y generará filas para el vector de estado.
        """
        raise NotImplementedError
