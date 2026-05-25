// Cierra el modal activo quitándolo del DOM.
function _cerrarModal() {
  var el = document.getElementById("error-modal");
  if (el) el.remove();
}

// Crea y muestra un modal de error reutilizable en cualquier página.
function mostrarModalError(titulo, mensaje) {
  _cerrarModal();

  var overlay = document.createElement("div");
  overlay.className = "modal-overlay";
  overlay.id = "error-modal";
  overlay.setAttribute("onclick", "if(event.target===this)_cerrarModal()");

  var card = document.createElement("div");
  card.className = "modal-card";
  card.innerHTML =
    '<h2 class="modal-title">' + titulo + "</h2>" +
    '<p class="modal-message">' + mensaje + "</p>" +
    '<div class="modal-actions">' +
      '<button class="btn btn-primary" onclick="_cerrarModal()">Entendido</button>' +
    "</div>";

  overlay.appendChild(card);
  document.body.appendChild(overlay);
}

document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") _cerrarModal();
});
