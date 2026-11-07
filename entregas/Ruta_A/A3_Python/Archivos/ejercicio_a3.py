import json
from collections import Counter
import pandas as pd

# Leer los datos de provincias y municipios
with open("datos/provincias_boyaca.geojson", encoding="utf-8") as f:
    datos = json.load(f)

print("=" * 50)
print("PARTE 1: CONTEO SIN PANDAS")
print("=" * 50)

conteo = Counter(
    feat["properties"]["provincia"]
    for feat in datos["features"]
)

for provincia, cantidad in conteo.most_common():
    print(f"{provincia:20} {cantidad}")

print("\nProvincias distintas:", len(conteo))

print("\n" + "=" * 50)
print("PARTE 2: CONTEO CON PANDAS")
print("=" * 50)

props = [f["properties"] for f in datos["features"]]
df = pd.DataFrame(props)

print(df.groupby("provincia").size().sort_values(ascending=False))
print("\nProvincias distintas:", df["provincia"].nunique())