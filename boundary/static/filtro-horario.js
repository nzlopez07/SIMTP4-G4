(function () {
  "use strict";

  var COL_HORA   = 1;
  var COL_EVENTO = 2;

  var RE_FORMATO = /^\d+:\d{2}:\d{2}$/;

  function formatoValido(valor) {
    return RE_FORMATO.test(valor);
  }

  function parseHoras(hms) {
    var partes = hms.split(":");
    if (partes.length !== 3) return NaN;
    return parseInt(partes[0], 10) + parseInt(partes[1], 10) / 60 + parseInt(partes[2], 10) / 3600;
  }

  function precomputarHoras(tbody) {
    var dia = 1;
    Array.from(tbody.rows).forEach(function (row) {
      var horaSimulada = row.cells[COL_HORA]   ? row.cells[COL_HORA].textContent.trim()   : "";
      var evento       = row.cells[COL_EVENTO] ? row.cells[COL_EVENTO].textContent.trim() : "";

      if (evento.includes("Nuevo día")) dia++;

      var horaDecimal = parseHoras(horaSimulada);
      row.dataset.horaTotal = isNaN(horaDecimal) ? -1 : horaDecimal + (dia - 1) * 24;
    });
  }

  function actualizarContador(tbody) {
    var total    = tbody.rows.length;
    var visibles = Array.from(tbody.rows).filter(function (r) {
      return r.style.display !== "none";
    }).length;

    var el = document.getElementById("filtro-count");
    if (!el) return;

    el.textContent = visibles === total
      ? total + " filas"
      : visibles + " de " + total + " filas";
  }

  function aplicarFiltro(tbody, desde, cantRegistros) {
    var contadorDesde = 0;

    Array.from(tbody.rows).forEach(function (row) {
      var horaTotal = parseFloat(row.dataset.horaTotal);
      var pasaDesde = desde === null || horaTotal >= desde;

      var visible;
      if (!pasaDesde) {
        visible = false;
      } else if (cantRegistros === null) {
        visible = true;
      } else {
        visible = contadorDesde < cantRegistros;
        contadorDesde++;
      }

      row.style.display = visible ? "" : "none";
    });

    actualizarContador(tbody);
  }

  function limpiarFiltro(tbody, inputDesde, inputCantRegistros) {
    inputDesde.value = "";
    if (inputCantRegistros) inputCantRegistros.value = "";
    Array.from(tbody.rows).forEach(function (r) { r.style.display = ""; });
    actualizarContador(tbody);
  }

  document.addEventListener("DOMContentLoaded", function () {
    var tabla = document.querySelector(".results-table");
    if (!tabla) return;

    var tbody = tabla.querySelector("tbody");
    if (!tbody) return;

    precomputarHoras(tbody);
    actualizarContador(tbody);

    var btnAplicar       = document.getElementById("filtro-aplicar");
    var btnLimpiar       = document.getElementById("filtro-limpiar");
    var inputDesde       = document.getElementById("filtro-desde");
    var inputCantRegistros = document.getElementById("filtro-cant-registros");

    function ejecutarFiltro() {
      var desdeStr = inputDesde ? inputDesde.value.trim() : "";
      var cantStr  = inputCantRegistros ? inputCantRegistros.value.trim() : "";

      if (desdeStr !== "" && !formatoValido(desdeStr)) {
        mostrarModalError(
          "Formato de hora incorrecto",
          "El campo «Desde» debe respetar el formato HH:MM:SS. " +
          "Solo se permiten dígitos (0–9) y el carácter «:»."
        );
        return;
      }

      var cantRegistros = cantStr !== "" ? parseInt(cantStr, 10) : null;
      if (cantRegistros !== null && (isNaN(cantRegistros) || cantRegistros < 1)) {
        mostrarModalError(
          "Cantidad inválida",
          "El campo «Cantidad Registros» debe ser un número entero mayor a 0."
        );
        return;
      }

      var desde = desdeStr !== "" ? parseHoras(desdeStr) : null;
      aplicarFiltro(tbody, desde, cantRegistros);
    }

    if (btnAplicar) btnAplicar.addEventListener("click", ejecutarFiltro);

    if (btnLimpiar) {
      btnLimpiar.addEventListener("click", function () {
        limpiarFiltro(tbody, inputDesde, inputCantRegistros);
      });
    }

    [inputDesde, inputCantRegistros].forEach(function (input) {
      if (input) {
        input.addEventListener("keydown", function (e) {
          if (e.key === "Enter") ejecutarFiltro();
        });
      }
    });
  });
})();
