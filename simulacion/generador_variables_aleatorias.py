from math import log
from datetime import timedelta


class GestorVariablesAleatorias():
    def tiempoLlegada(self, rnd):
        duracion = -12 * log(1 - rnd)
        return timedelta(seconds=round(duracion * 60))
    
    def tiempoLavado(self, rnd):
        # 10 + rnd * (15 - 10)
        duracion = 10 + rnd * (5)
        return timedelta(seconds=round(duracion * 60))
    
    def tiempoAspirado(self, rnd):
        duracion = -20 * log(1 - rnd)
        return timedelta(seconds=round(duracion * 60))
    
    def aspirado(self, rnd):
        # aspirado 0 a 0.199 | no aspirado 0.2 a 0.999
        if rnd < 0.2:
            return True
        else:
            return False