import requests
import geopandas as gpd
from pathlib import Path

# ==================================================
# ACTIVIDAD B1 - PANDAS Y GEOPANDAS
# ==================================================

carpeta_salida = Path("nivelacion/salidas")
carpeta_salida.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# EJERCICIO 1. DESCARGA DE VEREDAS DE TUNJA
# --------------------------------------------------

print("\n========================================")
print("EJERCICIO 1: DESCARGA DE VEREDAS DE TUNJA")
print("========================================")

url = (
    "https://services6.arcgis.com/Ex2fmFOuTOHRZtML/"
    "ArcGIS/rest/services/Veredas_Boyaca_2024/"
    "FeatureServer/0/query"
)

params = {
    "where": "NOMB_MPIO = 'TUNJA'",
    "outFields": "NOMB_MPIO,NOMBRE_VER,CODIGO_VER",
    "outSR": "4326",
    "f": "geojson"
}

respuesta = requests.get(url, params=params, timeout=60)
respuesta.raise_for_status()

datos = respuesta.json()

if "features" not in datos:
    raise ValueError("El servicio no devolvió entidades geográficas.")

gdf_tunja = gpd.GeoDataFrame.from_features(
    datos["features"],
    crs="EPSG:4326"
)

archivo_tunja = carpeta_salida / "veredas_tunja.geojson"
gdf_tunja.to_file(archivo_tunja, driver="GeoJSON")

print("TOTAL DE VEREDAS:", len(gdf_tunja))
print("CRS:", gdf_tunja.crs)
print("ARCHIVO:", archivo_tunja)

# --------------------------------------------------
# EJERCICIOS 2 Y 3. ANALISIS DE BOYACA
# --------------------------------------------------

print("\n========================================")
print("LECTURA DEL ARCHIVO DE VEREDAS DE BOYACA")
print("========================================")

archivo = Path("nivelacion/datos/veredas_boyaca.geojson")

if not archivo.exists():
    raise FileNotFoundError(f"No se encuentra el archivo: {archivo}")

gdf = gpd.read_file(archivo)

print("TOTAL DE REGISTROS:", len(gdf))
print("CRS ORIGINAL:", gdf.crs)

if gdf.crs is None:
    raise ValueError("El archivo de veredas no tiene CRS definido.")

# --------------------------------------------------
# EJERCICIO 2. CONTEO POR MUNICIPIO
# --------------------------------------------------

print("\n========================================")
print("EJERCICIO 2: CONTEO DE VEREDAS")
print("========================================")

conteo = (
    gdf.groupby("NOMB_MPIO")
    .size()
    .reset_index(name="TOTAL_VEREDAS")
    .sort_values("TOTAL_VEREDAS", ascending=False)
)

print("\nDIEZ MUNICIPIOS CON MAS VEREDAS:")
print(conteo.head(10).to_string(index=False))

archivo_conteo = carpeta_salida / "conteo_veredas_municipio.csv"

conteo.to_csv(
    archivo_conteo,
    index=False,
    encoding="utf-8-sig"
)

print("ARCHIVO:", archivo_conteo)

# --------------------------------------------------
# EJERCICIO 3. REPROYECCION Y CALCULO DE AREAS
# --------------------------------------------------

print("\n========================================")
print("EJERCICIO 3: CALCULO DE AREAS")
print("========================================")

gdf_proyectado = gdf.to_crs(epsg=9377)

gdf_proyectado["area_ha"] = (
    gdf_proyectado.geometry.area / 10000
)

mayores = (
    gdf_proyectado
    .sort_values("area_ha", ascending=False)
    .head(5)
)

print("CRS FINAL:", gdf_proyectado.crs)

print("\nCINCO VEREDAS CON MAYOR AREA:")
print(
    mayores[["NOMB_MPIO", "NOMBRE_VER", "area_ha"]]
    .to_string(index=False)
)

archivo_areas = carpeta_salida / "areas_veredas_boyaca.csv"

gdf_proyectado.drop(columns="geometry").to_csv(
    archivo_areas,
    index=False,
    encoding="utf-8-sig"
)

print("ARCHIVO:", archivo_areas)

# --------------------------------------------------
# FINALIZACION
# --------------------------------------------------

print("\n========================================")
print("ACTIVIDAD B1 FINALIZADA")
print("========================================")
print("Se generaron los tres productos de la actividad.")
