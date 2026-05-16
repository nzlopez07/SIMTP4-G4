from simulacion.randoms import GeneradorAleatorio


class GeneradorUniforme(GeneradorAleatorio):
    """Estrategia: distribución uniforme entre 0 y 1."""

    def generar(self) -> float:
        return self._rnd.random()
