from flask import Blueprint, render_template, request, url_for

from simulacion.motor import MotorSimulacion

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

    # Solo uno de los dos puede estar completo
    if (hora_fin and cant_sim):
        return render_template(
            "formulario-simulacion.html",
            error_title="Parámetros en conflicto",
            error="Solo podés completar uno de los campos: «Horario hasta» o «Cantidad de simulaciones», no ambos a la vez.",
            hora_fin=hora_fin,
            cant_sim=cant_sim,
            seed=seed,
        )

    # Al menos uno de los dos debe estar completo
    if not hora_fin and not cant_sim:
        return render_template(
            "formulario-simulacion.html",
            error="Debés completar al menos uno de los campos: «Horario hasta» o «Cantidad de simulaciones».",
            hora_fin=hora_fin,
            cant_sim=cant_sim,
            seed=seed,
        )
    # Creacion del controller
    motor = MotorSimulacion(seed, hora_fin, cant_sim)
    motor.ejecutar()
    filas_serializables = [f.como_dict() for f in motor.vector_estado.filas]
    return render_template("resultados.html", filas=filas_serializables)