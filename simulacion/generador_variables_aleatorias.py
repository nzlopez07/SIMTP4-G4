from math import log


class GestorVariablesAleatorias():
    def tiempoLlegada(rnd):
        return -12 * log(1 - rnd)
    
    def tiempoLavado(rnd):
        # 10 + rnd * (15 - 10)
        return 10 + rnd * (5)
    
    def tiempoAspirado(rnd):
        return -20 * log(1 - rnd)
    
    def aspirado(rnd):
        # aspirado 0 a 0.199 | no aspirado 0.2 a 0.999
        if rnd < 0.2:
            return True
        else:
            return False