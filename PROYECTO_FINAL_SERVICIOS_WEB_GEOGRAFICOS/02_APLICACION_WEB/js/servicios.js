
/* =========================================
   VISOR GEOGRÁFICO DE COLOMBIA
   Configuración de servicios GeoServer
========================================= */

// Dirección del servidor GeoServer
const GEOSERVER_URL = "http://localhost:8080/geoserver";

// Workspace del proyecto
const WORKSPACE = "taller";

// Servicio WMS
const WMS_URL = `${GEOSERVER_URL}/${WORKSPACE}/wms`;

// Servicio WFS
const WFS_URL = `${GEOSERVER_URL}/${WORKSPACE}/ows`;

// Capas geográficas disponibles
const CAPAS = {
    departamentos: {
        nombre: "taller:departamentos",
        titulo: "Departamentos de Colombia",
        geometria: "MULTIPOLYGON"
    },

    municipios: {
        nombre: "taller:Municipios",
        titulo: "Municipios de Colombia",
        geometria: "MULTIPOLYGON"
    }
};

// Configuración de visualización WMS
const CONFIG_WMS = {
    service: "WMS",
    version: "1.1.1",
    request: "GetMap",
    format: "image/png",
    transparent: true,
    srs: "EPSG:4326"
};

// Función para construir una solicitud WFS
function construirURLWFS(nombreCapa, cantidad = 100) {

    const parametros = new URLSearchParams({
        service: "WFS",
        version: "2.0.0",
        request: "GetFeature",
        typeNames: nombreCapa,
        count: cantidad,
        outputFormat: "application/json"
    });

    return `${WFS_URL}?${parametros.toString()}`;
}

// Función para consultar entidades mediante WFS
async function consultarCapaWFS(nombreCapa, cantidad = 100) {

    const url = construirURLWFS(nombreCapa, cantidad);

    const respuesta = await fetch(url);

    if (!respuesta.ok) {
        throw new Error(
            `Error consultando GeoServer: HTTP ${respuesta.status}`
        );
    }

    return await respuesta.json();
}

console.log("Configuración de servicios GeoServer cargada.");
console.log("WMS:", WMS_URL);
console.log("WFS:", WFS_URL);
