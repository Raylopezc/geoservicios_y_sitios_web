
/* =========================================
   VISOR GEOGRÁFICO DE COLOMBIA
   Módulo de visualización cartográfica
========================================= */

// Coordenadas centrales de Colombia
const CENTRO_COLOMBIA = [4.5709, -74.2973];

// Inicialización del mapa
const mapa = L.map("mapa", {
    center: CENTRO_COLOMBIA,
    zoom: 5,
    minZoom: 4,
    maxZoom: 18,
    zoomControl: true
});

// Mapa base de Esri World Street Map
const mapaBase = L.tileLayer(
    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
    {
        attribution: "Tiles &copy; Esri",
        maxZoom: 19
    }
).addTo(mapa);

// Capa WMS de departamentos
const capaDepartamentos = L.tileLayer.wms(
    WMS_URL,
    {
        layers: CAPAS.departamentos.nombre,
        format: "image/png",
        transparent: true,
        version: "1.1.1"
    }
);

// Capa WMS de municipios
const capaMunicipios = L.tileLayer.wms(
    WMS_URL,
    {
        layers: CAPAS.municipios.nombre,
        format: "image/png",
        transparent: true,
        version: "1.1.1"
    }
);

// Departamentos visibles inicialmente
capaDepartamentos.addTo(mapa);

// Control de capas
const capasBase = {
    "Mapa base": mapaBase
};

const capasSuperpuestas = {
    "Departamentos": capaDepartamentos,
    "Municipios": capaMunicipios
};

L.control.layers(
    capasBase,
    capasSuperpuestas,
    {
        collapsed: false
    }
).addTo(mapa);

// Escala cartográfica
L.control.scale({
    imperial: false,
    metric: true
}).addTo(mapa);

// Ajustar el mapa al territorio colombiano
const limitesColombia = L.latLngBounds(
    [-4.5, -82.0],
    [13.8, -66.5]
);

mapa.fitBounds(limitesColombia);

// Eventos de las capas
mapa.on("overlayadd", function(evento) {
    console.log("Capa activada:", evento.name);
});

mapa.on("overlayremove", function(evento) {
    console.log("Capa desactivada:", evento.name);
});

console.log("Mapa de Colombia inicializado correctamente.");
