class Auto:
    """Representa un vehículo en la simulación."""
    def __init__(self, id, horaLlegada, estado="", requiereAspirado=None):
        self.id = id  # Identificador único del auto
        self.estado = estado  # Estado actual del auto - EnCola | EnLavado | EsperandoAspirado | EnAspirado | Finalizado | Retirado
        self.requiereAspirado = requiereAspirado  # Indica si el auto requiere aspirado (True/False)
        self.horaLlegada = horaLlegada  # Hora de llegada del auto al lavadero

    def cambiarEstado (self, estado): # Siendo estado un número entero que representa el estado que vamos a setear
        match (estado):
            
            case 1:
            self.estado = "EnCola"
            break

            case 2:
            self.estado = "EnLavado"
            break

            case 3:
            self.estado = "EsperandoAspirado"
            break

            case 4:
            self.estado = "EnAspirado"
            break

            case 5:
            self.estado = "Finalizado"
            break

            case _:
            self.estado = "Retirado"

    def necesitaAspirado (self, boolean): # Si en evento fin de lavado se determina que requiere aspirado
        if (boolean == 1) {
            self.requiereAspirado = True
        } else {
            self.requiereAspirado = False
        }

    def como_dict (self): # Devuelve los atributos de la clase Auto en pares variable - valor
        return {
            "id": self.id,
            "estado": self.estado,
            "requiereAspirado": self.requiereAspirado,
            "horaLlegada": self.horaLlegada,
    }
