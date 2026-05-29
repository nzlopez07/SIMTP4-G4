from datetime import datetime, timedelta

from boundary.rutas import main as rutas_main


class _FakeFila:
    def __init__(self):
        self.contadorAutos = 12
        self.hora_simulada = datetime(2026, 5, 29, 21, 30)

    def como_dict(self):
        return {
            "contador_autos": self.contadorAutos,
            "hora_simulada": self.hora_simulada.strftime("%H:%M:%S"),
        }


class _FakeVectorEstado:
    def __init__(self):
        self._fila = _FakeFila()
        self.filas = [self._fila]

    def getActual(self):
        return self._fila


class _FakeRegistro:
    def calcular_metricas_finales(self, ultima_fila, tiempo_inicio=None):
        return {
            "clientes_perdidos_por_capacidad": 3,
            "porcentaje_tiempo_tunel_bloqueado": 18.4,
            "tiempo_horas_extras": timedelta(minutes=42),
            "tiempo_horas_extras_minutos": 42,
            "tiempo_promedio_horas_extras": timedelta(minutes=7),
            "tiempo_promedio_horas_extras_minutos": 7,
            "cantidad_jornadas": 6,
        }


class _FakeMotor:
    def __init__(self, seed, hora_fin, cant_sim):
        self.seed = seed
        self.hora_fin = hora_fin
        self.cant_sim = cant_sim
        self.vector_estado = _FakeVectorEstado()
        self.registro = _FakeRegistro()

    def ejecutar(self):
        return None


def test_simulacion_ejecutar_muestra_promedio_de_horas_extras(monkeypatch):
    captured = {}

    def fake_render_template(template_name, **context):
        captured["template_name"] = template_name
        captured["context"] = context
        return "ok"

    monkeypatch.setattr(rutas_main, "MotorSimulacion", _FakeMotor)
    monkeypatch.setattr(rutas_main, "render_template", fake_render_template)

    client = rutas_main.bp.app.test_client() if hasattr(rutas_main.bp, "app") else None
    if client is None:
        from boundary import create_app

        client = create_app().test_client()

    response = client.post(
        "/simulacion/ejecutar",
        data={"hora_fin": "72:00", "cant_sim": "", "seed": "123"},
    )

    assert response.status_code == 200
    assert captured["template_name"] == "resultados.html"
    assert captured["context"]["estadisticas"]["horas_extras_minutos"] == 7