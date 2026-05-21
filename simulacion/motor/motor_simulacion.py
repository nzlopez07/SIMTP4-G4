from simulacion.randoms.generador_aleatorio import GeneradorAleatorio
from simulacion.estadisticas.vector_estado import VectorEstado
from simulacion.estadisticas.registro_estadisticas import RegistroEstadisticas
from simulacion.eventos import Evento, EventoLlegada, EventoFinLavado, EventoFinAspirado
from simulacion.motor.calendario_eventos import CalendarioEventos

import random
class MotorSimulacion:
    """Núcleo que controlará la simulación.

    Ahora el motor puede recibir por inyección una instancia de GeneradorAleatorio
    y una instancia de VectorEstado (historial). Si no se proveen, se crean
    instancias por defecto.
    """

    def __init__(self, seed, vector_estado=None): # no estoy segura que tan correcto es pasarle el generador al motor como inicializador
        # inyección de dependencias: generador de números y vector de estado
        
        # self.seed = seed
        # No hace falta que el gestor guarde la seed, con hacer random.seed queda seteada
        # Si seed = None => no se rompe, usara de seed otra cosa (reloj del sistema por ejemplo)
        if seed is None or isinstance(seed, int):
            random.seed(seed)

        # self.generador = generador(seed)

        
        self.vector_estado = vector_estado if vector_estado is not None else VectorEstado()

        # registro de métricas separado
        self.registro = RegistroEstadisticas()

        # reloj e iterador
        self.reloj = 0.0
        self.iteracion = 0

        # calendario/agenda de eventos (se implementará aparte)
        self.calendario = CalendarioEventos()

    def agregar_fila_vector(self, fila):
        """Agregar una fila al vector de estado."""
        self.vector_estado.agregar(fila)

    def ejecutar(self, max_iteraciones=None, tiempo_max=None):
        """Bucle principal de la simulación (esqueleto).

        Por ahora es solo un stub; la implementación real iterará sobre el
        calendario de eventos y generará filas para el vector de estado.
        """
        raise NotImplementedError
    
    def generarRND(self):
        return random.random()