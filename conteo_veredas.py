import geopandas as gpd
from pathlib import Path

archivo = Path("nivelacion/datos/veredas_boyaca.geojson")

gdf = gpd.read_file(archivo)

print("TOTAL DE REGISTROS:", len(gdf))
print("SISTEMA DE REFERENCIA:", gdf.crs)

conteo = (
    gdf.groupby("NOMB_MPIO")
    .size()
    .reset_index(name="TOTAL_VEREDAS")
    .sort_values("TOTAL_VEREDAS", ascending=False)
)

print("\n10 MUNICIPIOS CON MAYOR NUMERO DE VEREDAS:")
print(conteo.head(10).to_string(index=False))

salida = Path("nivelacion/salidas/conteo_veredas_municipio.csv")
conteo.to_csv(salida, index=False, encoding="utf-8-sig")

print("\nARCHIVO GENERADO:", salida)
