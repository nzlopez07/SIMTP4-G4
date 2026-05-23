from datetime import datetime, time

from evento import Evento
from evento_fin_lavado import EventoFinLavado

from simulacion.estadisticas import FilaVectorEstado
from simulacion.generador_variables_aleatorias import GestorVariablesAleatorias
from simulacion.objetos import Auto


class EventoLlegada(Evento):
    def __init__(self, tiempo: datetime):
        super().__init__(tiempo, "Llegada")

    def ejecutar(self, motor, filaAnterior):
        filaActual = self.copiarFila(filaAnterior)
        filaActual.iteracion = filaAnterior.iteracion + 1
        filaActual.hora_simulada = self.tiempo
        filaActual.evento_simulado = self.nombre
       
        # Generar el nuevo auto
        filaActual.contadorAutos = filaAnterior.contadorAutos + 1
        id = filaActual.contadorAutos
        auto = Auto(id, self.tiempo)  # El estado se asignará más adelante

        
        # validar que el reloj es menor a las 21:00
        if self.tiempo.time() > time(21,0,0):
            filaActual.accionLlegada = f"Fuera de horario"
            
            return motor.agregar_fila_vector(filaActual)    # Agregar la fila al vector de estado


        # validar que la cola de autos no esté llena (max 5)
        # si está llena el cliente se retira (pierde)
        # en caso contrario se genera el auto y agrega a la cola
        if filaAnterior.colaAutos >= 5:
            filaActual.accionLlegada = f"A{id} se retira"
            filaActual.clientesPerdidos = filaAnterior.clientesPerdidos + 1
            
            return motor.agregar_fila_vector(filaActual)    # Agregar la fila al vector de estado
        else:
            filaActual.accionLlegada = f"A{id} ingresa"       


        generador = GestorVariablesAleatorias()

        # Generar la nueva llegada
        filaActual.rndLlegada = motor.generarRND()
        filaActual.tiempoLlegada = self.tiempo + generador.tiempoLlegada(filaActual.rndLlegada)

        motor.calendario.agregar_evento(EventoLlegada(filaActual.tiempoLlegada))


        # Generar evento fin lavado
        if not filaAnterior.tunel.esta_libre():
            # Si el túnel no está libre, el auto se agrega a la cola
            filaActual.colaAutos = filaAnterior.colaAutos + 1
            auto.estado = "EnCola"
            filaActual.autos.append(auto)
        else:
            auto.estado = "EnLavado"
            filaAnterior.tunel.ocupar(auto)

            filaActual.rndLavado = motor.generarRND()
            #filaActual.tiempoLavado = self.tiempo + generador.tiempoLavado(filaActual.rndLavado)
            motor.calendario.agregar_evento(EventoFinLavado(filaActual.tiempoLavado))


        return motor.agregar_fila_vector(filaActual)    # Agregar la fila al vector de estado


    def copiarFila(self, filaAnterior):
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

        fila.tiempoLavado = filaAnterior.tiempoLavado
        fila.tiempoAspirado1 = filaAnterior.tiempoAspirado1
        fila.tiempoAspirado2 = filaAnterior.tiempoAspirado2

        fila.colaAutos = filaAnterior.colaAutos
        fila.autos = filaAnterior.autos

        fila.clientesPerdidos = filaAnterior.clientesPerdidos
        fila.tiempoHorasExtras = filaAnterior.tiempoHorasExtras
        fila.tiempoTunelBloqueado = filaAnterior.tiempoTunelBloqueado

        fila.tunel = filaAnterior.tunel
        fila.puestoAspirado1 = filaAnterior.puestoAspirado1
        fila.puestoAspirado2 = filaAnterior.puestoAspirado2

        return fila