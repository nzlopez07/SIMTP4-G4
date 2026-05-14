def test_imports():
    from simulacion.motor import MotorSimulacion
    from simulacion.eventos import Evento
    from simulacion.objetos import Auto

    assert MotorSimulacion is not None
    assert Evento is not None
    assert Auto is not None
