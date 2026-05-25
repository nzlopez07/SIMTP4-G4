function _validarFormulario(e) {
  var horaFin = document.getElementById("hora_fin").value.trim();
  var cantSim = document.getElementById("cant_sim").value.trim();

  if (horaFin && cantSim) {
    e.preventDefault();
    mostrarModalError(
      "Parámetros en conflicto",
      "Solo podés completar uno de los campos: «Horario hasta» o «Cantidad de simulaciones», no ambos a la vez."
    );
    return false;
  }

  return true;
}
