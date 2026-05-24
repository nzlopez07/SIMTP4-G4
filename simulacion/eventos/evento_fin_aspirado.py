from copy import deepcopy

from simulacion.eventos.evento import Evento
from simulacion.generador_variables_aleatorias import GestorVariablesAleatorias


class EventoFinAspirado(Evento):
    """Evento que procesa la liberacion de un puesto de aspirado."""

    def __init__(self, tiempo, puesto_id):
        super().__init__(tiempo, "Fin aspirado")
        self.puesto_id = puesto_id
        self.fila_actual = None
        self.puesto = None
        self.auto_finalizado = None
        self.bloqueo_finalizado = False

    def _validar_procesamiento(self, motor):
        fila = self._obtener_fila_base(motor)
        puesto = self._obtener_puesto(fila)

        if puesto is None:
            raise Exception(f"No existe el puesto de aspirado {self.puesto_id}.")

        if puesto.esta_libre():
            raise Exception(f"No se puede procesar fin de aspirado: el puesto {self.puesto_id} esta libre.")

    def _ejecutar(self, motor):
        fila_anterior = self._obtener_fila_base(motor)
        self.fila_actual = self._copiar_fila(fila_anterior)
        self._preparar_fila(self.fila_actual, fila_anterior)

        self.puesto = self._obtener_puesto(self.fila_actual)
        self.auto_finalizado = self.puesto.auto_actual
        self.auto_finalizado.estado = "Finalizado"
        self.puesto.liberar()

        if self.fila_actual.tunel.esta_bloqueado():
            self._desbloquear_tunel_y_pasar_auto_a_aspirado(motor)

    def _generar_eventos(self, motor):
        if self.fila_actual.tunel.esta_libre() and self.fila_actual.colaAutos > 0:
            self._iniciar_lavado_desde_cola(motor)

    def _actualizar_estadisticas(self, motor):
        if self.bloqueo_finalizado:
            motor.registro.finalizar_bloqueo_tunel(self.tiempo)

        motor.agregar_fila_vector(self.fila_actual)

    def _desbloquear_tunel_y_pasar_auto_a_aspirado(self, motor):
        auto_bloqueado = self.fila_actual.tunel.auto_actual

        if auto_bloqueado is None:
            raise Exception("El tunel esta bloqueado, pero no conserva el auto bloqueado.")

        generador = GestorVariablesAleatorias()
        self.fila_actual.tunel.liberar()
        self._registrar_tiempo_bloqueado()
        self._ocupar_puesto_aspirado(motor, self.puesto, auto_bloqueado, generador)
        self.bloqueo_finalizado = True

    def _registrar_tiempo_bloqueado(self):
        inicio = getattr(self.fila_actual.tunel, "horaInicioBloqueado", None)

        if inicio is None:
            return

        self.fila_actual.tiempoTunelBloqueado += self.tiempo - inicio
        self.fila_actual.tunel.horaInicioBloqueado = None

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
        from simulacion.eventos.evento_fin_lavado import EventoFinLavado

        generador = GestorVariablesAleatorias()
        auto = self.fila_actual.autos.popleft()
        auto.estado = "EnLavado"

        self.fila_actual.colaAutos -= 1
        self.fila_actual.tunel.ocupar(auto)
        self.fila_actual.rndLavado = motor.generarRND()
        self.fila_actual.tiempoLavado = self.tiempo + generador.tiempoLavado(self.fila_actual.rndLavado)

        motor.calendario.agregar_evento(EventoFinLavado(self.fila_actual.tiempoLavado))

    def _obtener_puesto(self, fila):
        if self.puesto_id == 1:
            return fila.puestoAspirado1

        if self.puesto_id == 2:
            return fila.puestoAspirado2

        return None

    def _preparar_fila(self, fila_actual, fila_anterior):
        fila_actual.iteracion = fila_anterior.iteracion + 1
        fila_actual.hora_simulada = self.tiempo
        fila_actual.evento_simulado = f"{self.nombre} puesto {self.puesto_id}"

    def _obtener_fila_base(self, motor):
        if motor.fila_actual is not None:
            return motor.fila_actual

        return motor.vector_estado.getActual()

    def _copiar_fila(self, fila):
        return deepcopy(fila)
