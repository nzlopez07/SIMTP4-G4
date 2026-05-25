from copy import deepcopy

from simulacion.generador_variables_aleatorias import GestorVariablesAleatorias


class Evento:
    """Clase base para eventos."""

    def __init__(self, tiempo, nombre):
        self.tiempo = tiempo
        self.nombre = nombre

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
        pass

    def _obtener_fila_base(self, motor):
        if motor.fila_actual is not None:
            return motor.fila_actual
        return motor.vector_estado.getActual()

    def _copiar_fila(self, fila):
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
        auto = self.fila_actual.autos.popleft()
        auto.estado = "EnLavado"

        self.fila_actual.colaAutos -= 1
        self.fila_actual.tunel.ocupar(auto)
        self.fila_actual.rndLavado = motor.generarRND()
        self.fila_actual.tiempoLavado = self.tiempo + generador.tiempoLavado(self.fila_actual.rndLavado)

        motor.calendario.agregar_evento(EventoFinLavado(self.fila_actual.tiempoLavado))
