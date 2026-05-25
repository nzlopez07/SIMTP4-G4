from datetime import datetime, time, timedelta

from simulacion.eventos.evento import Evento
from simulacion.eventos.evento_fin_lavado import EventoFinLavado

from simulacion.estadisticas import FilaVectorEstado
from simulacion.generador_variables_aleatorias import GestorVariablesAleatorias
from simulacion.objetos import Auto


class EventoLlegada(Evento):
    def __init__(self, tiempo: datetime):
        super().__init__(tiempo, "Llegada")
        self.fila_actual = None
        self._fila_anterior = None
        self._auto = None
        self._generador = None
        self._termino_anticipado = False

    def _ejecutar(self, motor):
        self._fila_anterior = motor.fila_actual
        self.fila_actual = self._copiar_fila(self._fila_anterior)
        self.fila_actual.iteracion = self._fila_anterior.iteracion + 1
        self.fila_actual.hora_simulada = self.tiempo
        self.fila_actual.evento_simulado = self.nombre

        self.fila_actual.contadorAutos = self._fila_anterior.contadorAutos + 1
        id = self.fila_actual.contadorAutos
        self._auto = Auto(id, self.tiempo)

        if self.tiempo.time() >= time(21, 0, 0):
            self.fila_actual.accionLlegada = "Fuera de horario"
            self._termino_anticipado = True
            return

        self._generador = GestorVariablesAleatorias()
        self.fila_actual.rndLlegada = motor.generarRND()
        self.fila_actual.tiempoLlegada = self.tiempo + self._generador.tiempoLlegada(self.fila_actual.rndLlegada)
        motor.calendario.agregar_evento(EventoLlegada(self.fila_actual.tiempoLlegada))

        if self._fila_anterior.colaAutos >= 5:
            self.fila_actual.accionLlegada = f"A{id} se retira"
            self.fila_actual.clientesPerdidos = self._fila_anterior.clientesPerdidos + 1
            self._termino_anticipado = True
            return

        self.fila_actual.accionLlegada = f"A{id} ingresa"

    def _generar_eventos(self, motor):
        if self._termino_anticipado:
            if self.fila_actual.accionLlegada == "Fuera de horario":
                from simulacion.eventos.evento_nuevo_dia import EventoNuevoDia
                siguiente_dia = (self.tiempo + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
                motor.calendario.agregar_evento(EventoNuevoDia(siguiente_dia))
            return

        if not self._fila_anterior.tunel.esta_libre():
            self.fila_actual.colaAutos = self._fila_anterior.colaAutos + 1
            self._auto.estado = "EnCola"
            self.fila_actual.autos.append(self._auto)
        else:
            self._auto.estado = "EnLavado"
            self._fila_anterior.tunel.ocupar(self._auto)
            self.fila_actual.rndLavado = motor.generarRND()
            self.fila_actual.tiempoLavado = self.tiempo + self._generador.tiempoLavado(self.fila_actual.rndLavado)
            motor.calendario.agregar_evento(EventoFinLavado(self.fila_actual.tiempoLavado))

    def _actualizar_estadisticas(self, motor):
        motor.agregar_fila_vector(self.fila_actual)

    def _copiar_fila(self, fila_anterior):
        """" 
        Copiar los valores necesarios de la fila anterior a la actual 
        Datos que se tienen que copiar:
            tiempoLavado   # si ya hay un evento finLavado ya creado
            tiempoAspirado 1 y 2    # si ya hay un evento finAspirado ya creado
                
            colaAutos
            autos

            clientesPerdidos
            tiempoHorasExtras
            tiempoTunelBloqueado

            tunel
            puestoAspirado 1 y 2

        Con esto se operará sobre la fila actual directamente, para de esa forma en caso de no requerir modificación
        se mantendrán los mismos valores. Esto ahorrará if else y hará el código más limpio.
        """

        fila = FilaVectorEstado()

        fila.tiempoLavado = fila_anterior.tiempoLavado
        fila.tiempoAspirado1 = fila_anterior.tiempoAspirado1
        fila.tiempoAspirado2 = fila_anterior.tiempoAspirado2

        fila.colaAutos = fila_anterior.colaAutos
        fila.autos = fila_anterior.autos

        fila.clientesPerdidos = fila_anterior.clientesPerdidos
        fila.tiempoHorasExtras = fila_anterior.tiempoHorasExtras
        fila.tiempoTunelBloqueado = fila_anterior.tiempoTunelBloqueado

        fila.tunel = fila_anterior.tunel
        fila.puestoAspirado1 = fila_anterior.puestoAspirado1
        fila.puestoAspirado2 = fila_anterior.puestoAspirado2

        return fila
