from flask import Blueprint, jsonify, render_template, request, redirect, url_for

from simulacion.motor import MotorSimulacion
from simulacion.estadisticas import FilaVectorEstado, RegistroEstadisticas

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("pagina-inicio.html")

@bp.route("/formulario")
def simulacion_form():
    return render_template("formulario-simulacion.html")


@bp.route("/simulacion/ejecutar", methods=["POST"])
def simulacion_ejecutar():
    # leer parámetros del formulario (sin validación por ahora)
    hora_inicio = request.form.get("hora_inicio")
    hora_fin = request.form.get("hora_fin")
    seed = request.form.get("seed")

    # crear motor con vector y generador por defecto
    motor = MotorSimulacion()

    # generar una fila de ejemplo para que la vista muestre algo
    fila = FilaVectorEstado()
    fila.iteracion = 1
    fila.hora_simulada = 0.0   
    motor.agregar_fila_vector(fila)
    fila.evento_simulado = "InicioSimulacion"
    fila.agregar_variable_auxiliar("hora_inicio", hora_inicio)
    fila.agregar_variable_auxiliar("hora_fin", hora_fin)
    if seed:
        fila.agregar_rnd("seed", seed)
        
    # renderizar resultados inmediatamente (sin persistencia por ahora)
    filas_serializables = [f.como_dict() for f in motor.vector_estado.filas]
    return render_template("resultados.html", filas=filas_serializables)


@bp.route("/simulacion/resultados")
def simulacion_resultados():
    # ruta placeholder: sin almacenamiento persistente no hay resultados previos
    return render_template("resultados.html", filas=[])
    # El resultado no debera encontrarse aparte de las estadisticas. Las estadisticas se mostraran encima de la tabla. A su vez habra un boton para copiar todos los datos de las variables automaticamente.