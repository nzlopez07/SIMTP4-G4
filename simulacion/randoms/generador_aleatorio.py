from abc import ABC, abstractmethod
import random


class GeneradorAleatorio(ABC):
    """Interfaz abstracta para generadores de números aleatorios.
    El seed es opcional: si se pasa, la corrida es reproducible; si no, es aleatoria.
    """

    def __init__(self, seed=None):
        self._rnd = random.Random(seed)

    @abstractmethod
    def generar(self) -> float:
        """Retorna un valor según la distribución de la estrategia concreta."""
        ...
