import requests

url = "https://services6.arcgis.com/Ex2fmFOuTOHRZtML/ArcGIS/rest/services/Veredas_Boyaca_2024/FeatureServer/0/query"

params = {
    "where": "NOMB_MPIO = 'TUNJA'",
    "outFields": "NOMB_MPIO,NOMBRE_VER,CODIGO_VER",
    "outSR": "4326",
    "f": "geojson"
}

respuesta = requests.get(url, params=params, timeout=60)

print("CODIGO HTTP:", respuesta.status_code)

respuesta.raise_for_status()

datos = respuesta.json()
veredas = datos.get("features", [])

print("NUMERO DE VEREDAS:", len(veredas))

if veredas:
    print("PRIMERA VEREDA:", veredas[0]["properties"])
else:
    print("NO SE ENCONTRARON REGISTROS")
