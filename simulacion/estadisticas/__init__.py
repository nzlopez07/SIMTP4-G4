"""Registro y cálculo de métricas y vector de estado."""

from .vector_estado import FilaVectorEstado, VectorEstado


class RegistroEstadisticas:
    """Contenedor de métricas y acumuladores."""

    def __init__(self):
        self.clientesPerdidos = 0
        self.tiempoTunelBloqueado = 0
        self.tiempoHorasExtras = 0


__all__ = [
    "FilaVectorEstado",
    "VectorEstado",
    "RegistroEstadisticas",
]
