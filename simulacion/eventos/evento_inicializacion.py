from datetime import datetime, time

from simulacion.estadisticas import FilaVectorEstado
from simulacion.eventos.evento import Evento
from simulacion.eventos.evento_llegada import EventoLlegada
from simulacion.generador_variables_aleatorias import GestorVariablesAleatorias
from simulacion.objetos import PuestoAspirado, TunelLavado


class EventoInicializacion(Evento):
    """Evento inicial: crea la primera fila y agenda la primera llegada."""

    def __init__(self):
        t = datetime.combine(datetime.now(), time(9, 0, 0))
        super().__init__(t, "Inicializacion")
        self._primera_fila = None

    def _ejecutar(self, motor):
        self._primera_fila = FilaVectorEstado()
        self._primera_fila.iteracion = 1
        self._primera_fila.hora_simulada = self.tiempo
        self._primera_fila.evento_simulado = self.nombre

        self._primera_fila.tunel = TunelLavado()
        self._primera_fila.puestoAspirado1 = PuestoAspirado(1)
        self._primera_fila.puestoAspirado2 = PuestoAspirado(2)

        generador = GestorVariablesAleatorias()
        # Generar un RND para la llegada del primer auto
        self._primera_fila.rndLlegada = motor.generarRND()
        # Calcular el tiempo de llegada del primer auto | el generador retorna un timedelta
        self._primera_fila.tiempoLlegada = self.tiempo + generador.tiempoLlegada(self._primera_fila.rndLlegada)

    def _generar_eventos(self, motor):
        '''Agregar el evento a la cola'''
        motor.calendario.agregar_evento(EventoLlegada(self._primera_fila.tiempoLlegada))

    def _actualizar_estadisticas(self, motor):
        motor.registro.registrar_jornada(self.tiempo)
        motor.agregar_fila_vector(self._primera_fila)
