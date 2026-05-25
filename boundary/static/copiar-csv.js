(function () {
  "use strict";

  function escaparCSV(texto) {
    // Reemplaza el guión de celdas vacías por cadena vacía
    var s = texto.replace(/—|–/g, "");
    if (s.indexOf(",") !== -1 || s.indexOf('"') !== -1 || s.indexOf("\n") !== -1) {
      return '"' + s.replace(/"/g, '""') + '"';
    }
    return s;
  }

  function construirCSV(tabla) {
    var tbody = tabla.querySelector("tbody");

    var headers = Array.from(tabla.querySelectorAll("thead tr:last-child th")).map(function (th) {
      return escaparCSV(th.textContent.trim());
    });

    var filas = Array.from(tbody.rows)
      .filter(function (r) { return r.style.display !== "none"; })
      .map(function (row) {
        return Array.from(row.cells).map(function (td) {
          return escaparCSV(td.textContent.trim());
        }).join(",");
      });

    return [headers.join(",")].concat(filas).join("\n");
  }

  document.addEventListener("DOMContentLoaded", function () {
    var tabla = document.querySelector(".results-table");
    var btn   = document.getElementById("btn-copiar-csv");
    var hint  = document.getElementById("tabla-acciones-hint");
    if (!tabla || !btn) return;

    btn.addEventListener("click", function () {
      var csv = construirCSV(tabla);
      navigator.clipboard.writeText(csv).then(function () {
        if (hint) {
          hint.textContent = "¡Copiado al portapapeles!";
          hint.classList.add("tabla-acciones__hint--ok");
          setTimeout(function () {
            hint.textContent = "Copia los registros visibles con encabezado";
            hint.classList.remove("tabla-acciones__hint--ok");
          }, 2500);
        }
      }).catch(function () {
        mostrarModalError(
          "Error al copiar",
          "No se pudo acceder al portapapeles. Verificá que el navegador tenga permiso."
        );
      });
    });
  });
})();
