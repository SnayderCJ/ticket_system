const tipoFiltroSelect = document.getElementById("tipo_filtro");
const filtroPrioridadDiv = document.getElementById("filtro-prioridad");
const filtroTituloDiv = document.getElementById("filtro-titulo");

tipoFiltroSelect.addEventListener("change", () => {
  if (tipoFiltroSelect.value === "prioridad") {
    filtroPrioridadDiv.style.display = "block";
    filtroTituloDiv.style.display = "none";
  } else {
    filtroPrioridadDiv.style.display = "none";
    filtroTituloDiv.style.display = "block";
  }
});
