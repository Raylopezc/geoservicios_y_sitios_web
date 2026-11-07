import requests
import geopandas as gpd
from pathlib import Path

url = "https://services6.arcgis.com/Ex2fmFOuTOHRZtML/ArcGIS/rest/services/Veredas_Boyaca_2024/FeatureServer/0/query"

params = {
    "where": "NOMB_MPIO = 'TUNJA'",
    "outFields": "NOMB_MPIO,NOMBRE_VER,CODIGO_VER",
    "outSR": "4326",
    "f": "geojson"
}

respuesta = requests.get(url, params=params, timeout=60)
respuesta.raise_for_status()

datos = respuesta.json()

gdf_tunja = gpd.GeoDataFrame.from_features(
    datos["features"],
    crs="EPSG:4326"
)

salida = Path("nivelacion/salidas/veredas_tunja.geojson")
salida.parent.mkdir(parents=True, exist_ok=True)

gdf_tunja.to_file(salida, driver="GeoJSON")

print("DESCARGA COMPLETADA")
print("TOTAL DE VEREDAS:", len(gdf_tunja))
print("SISTEMA DE REFERENCIA:", gdf_tunja.crs)
print("ARCHIVO GENERADO:", salida)
