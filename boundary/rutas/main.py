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
    hora_fin    = request.form.get("hora_fin",    "").strip()
    cant_sim    = request.form.get("cant_sim",    "").strip()
    seed        = request.form.get("seed",        "").strip()

    # Al menos uno de los dos grupos debe estar completo
    if not hora_fin and not cant_sim:
        return render_template(
            "formulario-simulacion.html",
            error="Debés completar al menos uno de los campos: «Horario hasta» o «Cantidad de simulaciones».",
            hora_fin=hora_fin,
            cant_sim=cant_sim,
            seed=seed,
        )

    # crear motor con vector y generador por defecto
    ## A lo sumo guardar la seed y pasársela por separado al motor para que la use en su generador???
    motor = MotorSimulacion(seed, hora_fin, cant_sim)
    motor.ejecutar()
    # return render_template("resultados.html", filas=filas_serializables)


@bp.route("/simulacion/resultados")
def simulacion_resultados():
    # ruta placeholder: sin almacenamiento persistente no hay resultados previos
    return render_template("resultados.html", filas=[])
    # El resultado no debera encontrarse aparte de las estadisticas. Las estadisticas se mostraran encima de la tabla. A su vez habra un boton para copiar todos los datos de las variables automaticamente.