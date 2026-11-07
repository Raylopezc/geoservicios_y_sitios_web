import requests

# ==========================================
# B2 - APIs Y JSON
# EJERCICIO 1: PAGINACION
# ==========================================

url = (
    "https://services6.arcgis.com/Ex2fmFOuTOHRZtML/"
    "ArcGIS/rest/services/Veredas_Boyaca_2024/"
    "FeatureServer/0/query"
)

# Parametros base de la consulta
base = {
    "where": "COD_DPTO=15",
    "outFields": "NOMB_MPIO,NOMBRE_VER",
    "outSR": "4326",
    "f": "geojson"
}

# Configuracion de paginacion
features = []
offset = 0
bloque = 1000
iteraciones = 0

print("INICIANDO CONSULTA DE VEREDAS DE BOYACA")
print("----------------------------------------")

while True:

    parametros = {
        **base,
        "resultOffset": offset,
        "resultRecordCount": bloque
    }

    respuesta = requests.get(
        url,
        params=parametros,
        timeout=60
    )

    respuesta.raise_for_status()
    datos = respuesta.json()

    if "error" in datos:
        raise RuntimeError(datos["error"])

    nuevos = datos.get("features", [])

    features.extend(nuevos)
    iteraciones += 1

    print(
        f"Offset {offset}: +{len(nuevos)} "
        f"(total acumulado: {len(features)})"
    )

    if len(nuevos) < bloque:
        break

    offset += bloque

# Contar municipios distintos
municipios = {
    elemento["properties"].get("NOMB_MPIO")
    for elemento in features
    if elemento.get("properties", {}).get("NOMB_MPIO")
}

print("\n========================================")
print("RESULTADOS DEL EJERCICIO B2")
print("========================================")
print("TOTAL DE VEREDAS RECUPERADAS:", len(features))
print("MUNICIPIOS DISTINTOS:", len(municipios))
print("NUMERO DE ITERACIONES:", iteraciones)
print("TAMANO DEL BLOQUE:", bloque)
print("========================================")
