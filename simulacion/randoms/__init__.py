"""Generador aleatorio centralizado (esqueleto)."""


class GeneradorAleatorio:
    """Centraliza la generación de números aleatorios."""

    def __init__(self, seed=None):
        self.seed = seed

    def generar_uniforme(self):
        raise NotImplementedError

    def generar_exponencial(self, media):
        raise NotImplementedError
