from abc import ABC, abstractmethod
from copy import deepcopy


class Evento(ABC):
    """Clase base para eventos de la simulacion."""

    def __init__(self, tiempo, nombre):
        self.tiempo = tiempo
        self.nombre = nombre
        self.fila_actual = None

    def __lt__(self, otroEvento):
        """Permite ordenar eventos por tiempo dentro del calendario."""
        return self.tiempo < otroEvento.tiempo

    def procesar(self, motor):
        """Template Method: define el orden comun de procesamiento."""
        self._validar_procesamiento(motor)
        self._ejecutar(motor)
        self._generar_eventos(motor)
        self._actualizar_estadisticas(motor)

    def _validar_procesamiento(self, motor):
        pass

    @abstractmethod
    def _ejecutar(self, motor):
        pass

    @abstractmethod
    def _generar_eventos(self, motor):
        pass

    def _actualizar_estadisticas(self, motor):
        if self.fila_actual is not None:
            motor.agregar_fila_vector(self.fila_actual)

    def _obtener_fila_base(self, motor):
        if hasattr(motor, "obtener_fila_base"):
            return motor.obtener_fila_base()

        if getattr(motor, "fila_actual", None) is not None:
            return motor.fila_actual

        return motor.vector_estado.getActual()

    def _copiar_fila(self, fila):
        """Copia completa de la fila anterior.

        Usamos deepcopy porque la fila contiene objetos mutables y anidados
        (tunel, puestos, autos y cola). Una copia manual es ruidosa y facil de
        desactualizar cada vez que se agrega una columna al vector de estado.
        """
        return deepcopy(fila)

    def _preparar_fila(self, fila_actual, fila_anterior=None):
        iteracion_anterior = fila_anterior.iteracion if fila_anterior is not None else 0
        fila_actual.iteracion = iteracion_anterior + 1
        fila_actual.hora_simulada = self.tiempo
        fila_actual.evento_simulado = self.nombre

        fila_actual.rndLlegada = None
        fila_actual.rndLavado = None
        fila_actual.rndFlagAspirado = None
        fila_actual.rndAspirado1 = None
        fila_actual.rndAspirado2 = None