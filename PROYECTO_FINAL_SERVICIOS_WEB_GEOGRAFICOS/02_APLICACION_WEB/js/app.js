
/* =========================================
   VISOR GEOGRÁFICO DE COLOMBIA
   Controlador principal de la aplicación
========================================= */

// Controles HTML
const controlDepartamentos = document.getElementById("capaDepartamentos");
const controlMunicipios = document.getElementById("capaMunicipios");

// Verificar que los controles existan
if (!controlDepartamentos || !controlMunicipios) {
    console.error("No se encontraron los controles de las capas.");
}

// Sincronizar visibilidad de departamentos
controlDepartamentos.addEventListener("change", function () {

    if (this.checked) {
        mapa.addLayer(capaDepartamentos);
        console.log("Departamentos activados.");
    } else {
        mapa.removeLayer(capaDepartamentos);
        console.log("Departamentos desactivados.");
    }
});

// Sincronizar visibilidad de municipios
controlMunicipios.addEventListener("change", function () {

    if (this.checked) {
        mapa.addLayer(capaMunicipios);
        console.log("Municipios activados.");
    } else {
        mapa.removeLayer(capaMunicipios);
        console.log("Municipios desactivados.");
    }
});

// Sincronizar controles laterales cuando se usan
// los controles de capas propios de Leaflet
mapa.on("overlayadd", function (evento) {

    if (evento.layer === capaDepartamentos) {
        controlDepartamentos.checked = true;
    }

    if (evento.layer === capaMunicipios) {
        controlMunicipios.checked = true;
    }
});

mapa.on("overlayremove", function (evento) {

    if (evento.layer === capaDepartamentos) {
        controlDepartamentos.checked = false;
    }

    if (evento.layer === capaMunicipios) {
        controlMunicipios.checked = false;
    }
});

// Ajustar el mapa al cambiar el tamaño de la ventana
window.addEventListener("resize", function () {
    mapa.invalidateSize();
});

// Mensaje inicial del panel
panelInformacion.innerHTML = `
    <p><strong>Visor geográfico de Colombia</strong></p>
    <p>Active una capa y seleccione una entidad en el mapa
    para consultar su información.</p>
`;

console.log("Aplicación geográfica inicializada correctamente.");
