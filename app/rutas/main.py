from flask import Blueprint, jsonify

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return "Eco-Clean Simulation API"


@bp.route("/api/status")
def status():
    return jsonify({"status": "ok"})
