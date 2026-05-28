class Auto:
    """Representa un vehículo en la simulación."""
    def __init__(self, id, horaLlegada, estado="", requiereAspirado=None):
        self.id = id  # Identificador único del auto
        self.estado = estado  # Estado actual del auto - EnCola | EnLavado | EsperandoAspirado | EnAspirado | Finalizado | Retirado
        self.requiereAspirado = requiereAspirado  # Indica si el auto requiere aspirado (True/False)
        self.horaLlegada = horaLlegada  # Hora de llegada del auto al lavadero

    def cambiarEstado(self, estado):
        match estado:
            case 1:
                self.estado = "EnCola"
            case 2:
                self.estado = "EnLavado"
            case 3:
                self.estado = "EsperandoAspirado"
            case 4:
                self.estado = "EnAspirado"
            case 5:
                self.estado = "Finalizado"
            case _:
                self.estado = "Retirado"

    def necesitaAspirado(self, boolean):
        if boolean == 1:
            self.requiereAspirado = True
        else:
            self.requiereAspirado = False

    def como_dict(self):
        return {
            "id": self.id,
            "estado": self.estado,
            "requiereAspirado": self.requiereAspirado,
            "horaLlegada": self.horaLlegada,
        }
