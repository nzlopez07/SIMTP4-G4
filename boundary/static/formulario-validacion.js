function _cerrarModalConflicto() {
  var el = document.getElementById('error-modal-conflicto');
  if (el) el.style.display = 'none';
}

function _validarFormulario(e) {
  var horaFin = document.getElementById('hora_fin').value.trim();
  var cantSim = document.getElementById('cant_sim').value.trim();
  if (horaFin && cantSim) {
    e.preventDefault();
    var el = document.getElementById('error-modal-conflicto');
    if (el) el.style.display = 'flex';
    return false;
  }
  return true;
}

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') _cerrarModalConflicto();
});
