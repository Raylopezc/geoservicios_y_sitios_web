
/* =========================================
   VISOR GEOGRÁFICO DE COLOMBIA
   Módulo de consultas geográficas
========================================= */

// Referencia al panel de información
const panelInformacion = document.getElementById("informacion");

// Evitar que los atributos consultados puedan
// interpretar contenido HTML como código.
function escaparHTML(valor) {
    return String(valor ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

// Construir solicitud GetFeatureInfo de WMS
function construirURLGetFeatureInfo(evento, nombreCapa) {

    const punto = mapa.latLngToContainerPoint(evento.latlng);
    const tamano = mapa.getSize();
    const limites = mapa.getBounds();

    const bbox = [
        limites.getWest(),
        limites.getSouth(),
        limites.getEast(),
        limites.getNorth()
    ].join(",");

    const parametros = new URLSearchParams({
        SERVICE: "WMS",
        VERSION: "1.1.1",
        REQUEST: "GetFeatureInfo",
        LAYERS: nombreCapa,
        QUERY_LAYERS: nombreCapa,
        STYLES: "",
        BBOX: bbox,
        SRS: "EPSG:4326",
        WIDTH: tamano.x,
        HEIGHT: tamano.y,
        FORMAT: "image/png",
        INFO_FORMAT: "application/json",
        X: Math.round(punto.x),
        Y: Math.round(punto.y),
        FEATURE_COUNT: 5
    });

    return `${WMS_URL}?${parametros.toString()}`;
}

// Consultar una capa mediante GetFeatureInfo
async function consultarInformacion(evento, nombreCapa, titulo) {

    const url = construirURLGetFeatureInfo(evento, nombreCapa);

    const respuesta = await fetch(url);

    if (!respuesta.ok) {
        throw new Error(`Error HTTP ${respuesta.status}`);
    }

    const datos = await respuesta.json();

    if (!datos.features || datos.features.length === 0) {
        return [];
    }

    return datos.features.map(elemento => elemento.properties);
}

// Mostrar los resultados en el panel
function mostrarResultados(titulo, resultados) {

    if (resultados.length === 0) {
        return "";
    }

    let contenido = `<h3>${escaparHTML(titulo)}</h3>`;

    resultados.forEach((atributos, indice) => {

        contenido += `<div class="resultado-consulta">`;
        contenido += `<strong>Entidad ${indice + 1}</strong>`;

        Object.entries(atributos).forEach(([campo, valor]) => {

            if (valor !== null && valor !== undefined) {
                contenido += `
                    <p>
                        <strong>${escaparHTML(campo)}:</strong>
                        ${escaparHTML(valor)}
                    </p>
                `;
            }
        });

        contenido += `</div>`;
    });

    return contenido;
}

// Evento de clic sobre el mapa
mapa.on("click", async function(evento) {

    panelInformacion.innerHTML = "<p>Consultando información geográfica...</p>";

    try {

        const consultas = [];

        // Consultar departamentos si la capa está visible
        if (mapa.hasLayer(capaDepartamentos)) {
            consultas.push(
                consultarInformacion(
                    evento,
                    CAPAS.departamentos.nombre,
                    "Departamentos"
                )
            );
        }

        // Consultar municipios si la capa está visible
        if (mapa.hasLayer(capaMunicipios)) {
            consultas.push(
                consultarInformacion(
                    evento,
                    CAPAS.municipios.nombre,
                    "Municipios"
                )
            );
        }

        const resultados = await Promise.all(consultas);

        let contenido = "";

        if (resultados.length === 0) {
            contenido = "<p>Active al menos una capa para consultar información.</p>";
        } else {

            if (mapa.hasLayer(capaDepartamentos)) {
                contenido += mostrarResultados(
                    "Departamentos",
                    resultados.shift()
                );
            }

            if (mapa.hasLayer(capaMunicipios)) {
                contenido += mostrarResultados(
                    "Municipios",
                    resultados.shift()
                );
            }

            if (!contenido) {
                contenido = "<p>No se encontraron entidades en esta ubicación.</p>";
            }
        }

        panelInformacion.innerHTML = contenido;

    } catch (error) {

        console.error("Error en la consulta geográfica:", error);

        panelInformacion.innerHTML = `
            <p>No fue posible consultar GeoServer.</p>
            <p>Detalle: ${escaparHTML(error.message)}</p>
        `;
    }
});

console.log("Módulo de consultas geográficas cargado.");
