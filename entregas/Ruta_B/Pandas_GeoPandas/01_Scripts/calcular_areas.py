import geopandas as gpd
from pathlib import Path

archivo = Path("nivelacion/datos/veredas_boyaca.geojson")

gdf = gpd.read_file(archivo)

print("CRS ORIGINAL:", gdf.crs)

gdf_proyectado = gdf.to_crs(epsg=9377)

gdf_proyectado["area_ha"] = (
    gdf_proyectado.geometry.area / 10000
)

mayores = gdf_proyectado.sort_values(
    "area_ha",
    ascending=False
).head(5)

print("\nLAS CINCO VEREDAS CON MAYOR AREA:")
print(
    mayores[["NOMB_MPIO", "NOMBRE_VER", "area_ha"]]
    .to_string(index=False)
)

salida = Path("nivelacion/salidas/areas_veredas_boyaca.csv")

gdf_proyectado.drop(columns="geometry").to_csv(
    salida,
    index=False,
    encoding="utf-8-sig"
)

print("\nCRS FINAL:", gdf_proyectado.crs)
print("ARCHIVO GENERADO:", salida)
