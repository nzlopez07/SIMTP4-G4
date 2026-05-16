function _cerrarModal() {
  var el = document.getElementById('error-modal');
  if (el) el.remove();
}

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') _cerrarModal();
});
