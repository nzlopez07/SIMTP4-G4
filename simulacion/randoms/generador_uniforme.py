from simulacion.randoms import GeneradorAleatorio


class GeneradorUniforme(GeneradorAleatorio):
    """Estrategia: distribución uniforme entre A y B."""

    def __init__(self, a: float, b: float):
        super().__init__()
        self._a = a
        self._b = b

    def generar(self) -> float:
        return self._rnd.uniform(self._a, self._b)
