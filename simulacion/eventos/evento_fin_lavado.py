from copy import deepcopy

from simulacion.eventos.evento import Evento
from simulacion.eventos.evento_fin_aspirado import EventoFinAspirado
from simulacion.generador_variables_aleatorias import GestorVariablesAleatorias


class EventoFinLavado(Evento):
    """Evento que procesa la salida de un auto del tunel de lavado."""

    def __init__(self, tiempo):
        super().__init__(tiempo, "Fin lavado")
        self.fila_actual = None
        self.auto = None
        self.bloqueo_iniciado = False

    def _validar_procesamiento(self, motor):
        fila = self._obtener_fila_base(motor)

        if not hasattr(fila, "tunel"):
            raise Exception("No se puede procesar fin de lavado: la fila no tiene tunel.")

        if fila.tunel.auto_actual is None:
            raise Exception("No se puede procesar fin de lavado: el tunel no tiene auto.")

    def _ejecutar(self, motor):
        fila_anterior = self._obtener_fila_base(motor)
        self.fila_actual = self._copiar_fila(fila_anterior)
        self._preparar_fila(self.fila_actual, fila_anterior)

        self.auto = self.fila_actual.tunel.auto_actual

        generador = GestorVariablesAleatorias()
        self.fila_actual.rndFlagAspirado = motor.generarRND()
        self.fila_actual.flagAspirado = generador.aspirado(self.fila_actual.rndFlagAspirado)
        self.auto.requiereAspirado = self.fila_actual.flagAspirado

        if self.auto.requiereAspirado:
            self._procesar_auto_con_aspirado(motor, generador)
        else:
            self._finalizar_auto_sin_aspirado()

    def _generar_eventos(self, motor):
        if self.fila_actual.tunel.esta_libre() and self.fila_actual.colaAutos > 0:
            self._iniciar_lavado_desde_cola(motor)

    def _actualizar_estadisticas(self, motor):
        if self.bloqueo_iniciado:
            motor.registro.iniciar_bloqueo_tunel(self.tiempo)

        motor.agregar_fila_vector(self.fila_actual)

    def _procesar_auto_con_aspirado(self, motor, generador):
        puesto = self._buscar_puesto_libre()

        if puesto is None:
            self.auto.estado = "EsperandoAspirado"
            self.fila_actual.tunel.estado = "Bloqueado"
            self.fila_actual.tunel.horaInicioBloqueado = self.tiempo
            self.bloqueo_iniciado = True
            return

        self.fila_actual.tunel.liberar()
        self._ocupar_puesto_aspirado(motor, puesto, self.auto, generador)

    def _finalizar_auto_sin_aspirado(self):
        self.auto.estado = "Finalizado"
        self.fila_actual.tunel.liberar()

    def _buscar_puesto_libre(self):
        puestos = [self.fila_actual.puestoAspirado1, self.fila_actual.puestoAspirado2]

        for puesto in puestos:
            if puesto.esta_libre():
                return puesto

        return None

    def _ocupar_puesto_aspirado(self, motor, puesto, auto, generador):
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
        generador = GestorVariablesAleatorias()
        auto = self.fila_actual.autos.popleft()
        auto.estado = "EnLavado"

        self.fila_actual.colaAutos -= 1
        self.fila_actual.tunel.ocupar(auto)
        self.fila_actual.rndLavado = motor.generarRND()
        self.fila_actual.tiempoLavado = self.tiempo + generador.tiempoLavado(self.fila_actual.rndLavado)

        motor.calendario.agregar_evento(EventoFinLavado(self.fila_actual.tiempoLavado))

    def _preparar_fila(self, fila_actual, fila_anterior):
        fila_actual.iteracion = fila_anterior.iteracion + 1
        fila_actual.hora_simulada = self.tiempo
        fila_actual.evento_simulado = self.nombre

    def _obtener_fila_base(self, motor):
        if motor.fila_actual is not None:
            return motor.fila_actual

        return motor.vector_estado.getActual()

    def _copiar_fila(self, fila):
        return deepcopy(fila)
