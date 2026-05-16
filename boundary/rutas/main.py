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
    tiempo = request.form.get("tiempo")
    max_iter = request.form.get("max_iteraciones")
    i = request.form.get("i")
    j = request.form.get("j")
    seed = request.form.get("seed")

    # crear motor con vector y generador por defecto
    motor = MotorSimulacion()

    # generar una fila de ejemplo para que la vista muestre algo
    fila = FilaVectorEstado()
    try:
        fila.iteracion = int(max_iter) if max_iter else 1
    except Exception:
        fila.iteracion = 1
    fila.hora_simulada = float(tiempo) if tiempo else 0.0
    fila.evento_simulado = "EjemploInicio"
    fila.agregar_variable_auxiliar("param_i", i)
    fila.agregar_variable_auxiliar("param_j", j)
    if seed:
        fila.agregar_rnd("seed", seed)

    motor.agregar_fila_vector(fila)

    # renderizar resultados inmediatamente (sin persistencia por ahora)
    filas_serializables = [f.como_dict() for f in motor.vector_estado.filas]
    return render_template("resultados.html", filas=filas_serializables)


@bp.route("/simulacion/resultados")
def simulacion_resultados():
    # ruta placeholder: sin almacenamiento persistente no hay resultados previos
    return render_template("resultados.html", filas=[])
    # El resultado no debera encontrarse aparte de las estadisticas. Las estadisticas se mostraran encima de la tabla. A su vez habra un boton para copiar todos los datos de las variables automaticamente.