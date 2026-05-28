from abc import ABC, abstractmethod
from copy import deepcopy

from simulacion.generador_variables_aleatorias import GestorVariablesAleatorias


class Evento(ABC):
    """Clase base para eventos."""

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
        """Actualiza las estadísticas del motor en función del resultado del evento."""
        if self.fila_actual is not None:
            motor.agregar_fila_vector(self.fila_actual)

    def _obtener_fila_base(self, motor):
            if hasattr(motor, "obtener_fila_base"):
                return motor.obtener_fila_base()

            if getattr(motor, "fila_actual", None) is not None:
                return motor.fila_actual

            if motor.fila_actual is not None:
                return motor.fila_actual
            return motor.vector_estado.getActual()
    
    def _copiar_fila(self, fila):
        """Copia completa de la fila anterior.

        Usamos deepcopy porque la fila contiene objetos mutables y anidados
        (tunel, puestos, autos y cola). Una copia manual es ruidosa y facil de
        desactualizar cada vez que se agrega una columna al vector de estado.
        """
        return deepcopy(fila)
    
    def _ocupar_puesto_aspirado(self, motor, puesto, auto, generador):
        from simulacion.eventos.evento_fin_aspirado import EventoFinAspirado
        auto.estado = "EnAspirado"
        puesto.ocupar(auto)

        rnd = motor.generarRND()
        tiempo_fin = self.tiempo + generador.tiempoAspirado(rnd)

        if puesto.id == 1:
            self.fila_actual.rndAspirado1 = rnd
            self.fila_actual.tiempoAspirado1 = tiempo_fin
        else:
            self.fila_actual.rndAspirado2 = rnd
            self.fila_actual.tiempoAspirado2 = tiempo_fin

        motor.calendario.agregar_evento(EventoFinAspirado(tiempo_fin, puesto.id))

    def _iniciar_lavado_desde_cola(self, motor):
        from simulacion.eventos.evento_fin_lavado import EventoFinLavado
        generador = GestorVariablesAleatorias()
        auto = self.fila_actual.colaLavado.desencolar_auto()
        auto.estado = "EnLavado"
        self.fila_actual.tunel.ocupar(auto)
        self.fila_actual.rndLavado = motor.generarRND()
        self.fila_actual.tiempoLavado = self.tiempo + generador.tiempoLavado(self.fila_actual.rndLavado)

        motor.calendario.agregar_evento(EventoFinLavado(self.fila_actual.tiempoLavado))

    def _preparar_fila(self, fila_actual, fila_anterior=None):
        iteracion_anterior = fila_anterior.iteracion if fila_anterior is not None else 0
        fila_actual.iteracion = iteracion_anterior + 1
        fila_actual.hora_simulada = self.tiempo
        fila_actual.evento_simulado = self.nombre

        fila_actual.accionLlegada = ""

        fila_actual.rndLlegada = None
        fila_actual.rndLavado = None
        fila_actual.rndFlagAspirado = None
        fila_actual.flagAspirado = None
        fila_actual.rndAspirado1 = None
        fila_actual.rndAspirado2 = None