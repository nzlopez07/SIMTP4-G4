from datetime import timedelta


class RegistroEstadisticas:
    """Contenedor de métricas y acumuladores."""

    def __init__(self):
        self.clientesPerdidos = 0
        self.tiempoTunelBloqueado = timedelta(0)
        self.tiempoHorasExtras = timedelta(0)

    def registrar_cliente_perdido(self):
        self.clientesPerdidos += 1
    
    def iniciar_bloqueo_tunel(self, tiempo_inicio):
        self.tiempoInicioBloqueo = tiempo_inicio

    def finalizar_bloqueo_tunel(self, tiempo_fin):
        if hasattr(self, 'tiempoInicioBloqueo'):
            self.tiempoTunelBloqueado += tiempo_fin - self.tiempoInicioBloqueo
            del self.tiempoInicioBloqueo  # Limpiar el atributo para evitar errores futuros
    
    def registrar_fin_simulacion(self, tiempo_fin_simulacion, tiempo_cierre_tunel):
        if tiempo_fin_simulacion > tiempo_cierre_tunel:
            self.tiempoHorasExtras += tiempo_fin_simulacion - tiempo_cierre_tunel

    def calcular_metricas_finales(self):
        """Calcular métricas finales."""
        self.ClientesPerdidosPorCapacidad = self.clientesPerdidos
        self.PorcentajeTiempoBloqueadoPorAspirado = (self.tiempoTunelBloqueado / self.tiempo_final_simulacion) * 100 if self.tiempo_final_simulacion > 0 else 0
        self.PromedioHorasExtras = self.tiempoHorasExtras / self.iteraciones if self.iteraciones > 0 else 0