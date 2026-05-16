import math
from simulacion.randoms import GeneradorAleatorio


class GeneradorExponencial(GeneradorAleatorio):
    """Estrategia: distribución exponencial por transformación inversa."""

    def __init__(self, media: float, seed=None):
        super().__init__(seed)
        self._media = media

    def generar(self) -> float:
        rnd = self._rnd.random()
        return -self._media * math.log(1 - rnd)
