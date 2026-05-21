from abc import ABC, abstractmethod
class Evento:
    """Clase base para eventos."""

    def __init__(self, tiempo=0):
        self.tiempo = tiempo
        self.RNDusado = None  # RND utilizado para generar el evento (si corresponde)
        self.resultadoDecision = None  # Resultado de la decisión tomada (si corresponde)

    def __lt__(self, otroEvento):
        """Permite comparar eventos por su tiempo para ordenarlos en el calendario."""
        return self.tiempo < otroEvento.tiempo

    def procesar(self, motor): ##Contratos a implementar
        """Procesa el evento sobre el `motor` (implementación en el futuro)."""
        self._validar_procesamiento(motor)
        self._ejecutar(motor)
        self._generar_eventos(motor)
        self._actualizar_estadisticas(motor)

    def _validar_procesamiento(self, motor):
        """Valida que el evento pueda ser procesado sobre el motor dado."""
        pass  # Implementar validaciones específicas según el tipo de evento

    def _ejecutar(self, motor):
        """Ejecuta la lógica principal del evento sobre el motor."""
        pass  # Implementar la lógica específica del evento

    def _generar_eventos(self, motor):
        """Genera nuevos eventos en función del resultado del evento actual."""
        pass  # Implementar la generación de nuevos eventos según el tipo de evento

    def _actualizar_estadisticas(self, motor):
        """Actualiza las estadísticas del motor en función del resultado del evento."""
        pass  # Implementar la actualización de estadísticas según el tipo de evento