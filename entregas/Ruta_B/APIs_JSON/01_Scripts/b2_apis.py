import requests
import pandas as pd
from pathlib import Path

# ==========================================
# B2 - APIS Y JSON
# SCRIPT INTEGRADOR
# ==========================================

URL = (
    "https://services6.arcgis.com/Ex2fmFOuTOHRZtML/"
    "ArcGIS/rest/services/Veredas_Boyaca_2024/"
    "FeatureServer/0/query"
)

SALIDA = Path("nivelacion/salidas")
SALIDA.mkdir(parents=True, exist_ok=True)

def consultar_paginado(bloque):

    registros = []
    offset = 0
    iteraciones = 0

    base = {
        "where": "COD_DPTO=15",
        "outFields": "NOMB_MPIO,NOMBRE_VER",
        "outSR": "4326",
        "f": "geojson"
    }

    while True:

        parametros = {
            **base,
            "resultOffset": offset,
            "resultRecordCount": bloque
        }

        respuesta = requests.get(
            URL,
            params=parametros,
            timeout=60
        )

        respuesta.raise_for_status()
        datos = respuesta.json()

        if "error" in datos:
            raise RuntimeError(datos["error"])

        nuevos = datos.get("features", [])

        registros.extend(nuevos)
        iteraciones += 1

        print(
            f"Bloque {bloque} | Offset {offset} | "
            f"Registros: {len(nuevos)} | "
            f"Acumulado: {len(registros)}"
        )

        if len(nuevos) < bloque:
            break

        offset += bloque

    municipios = {
        f["properties"].get("NOMB_MPIO")
        for f in registros
        if f.get("properties", {}).get("NOMB_MPIO")
    }

    return len(registros), len(municipios), iteraciones


print("\nB2 - COMPARACION DE PAGINACION")
print("--------------------------------")

resultados = []

for bloque in [1000, 500]:

    total, municipios, iteraciones = consultar_paginado(bloque)

    resultados.append({
        "TAMANO_BLOQUE": bloque,
        "TOTAL_VEREDAS": total,
        "MUNICIPIOS_DISTINTOS": municipios,
        "ITERACIONES": iteraciones
    })

    print("\nRESULTADO DEL BLOQUE:", bloque)
    print("TOTAL DE VEREDAS:", total)
    print("MUNICIPIOS DISTINTOS:", municipios)
    print("ITERACIONES:", iteraciones)

df = pd.DataFrame(resultados)

archivo = SALIDA / "comparacion_paginacion_b2.csv"

df.to_csv(
    archivo,
    index=False,
    encoding="utf-8-sig"
)

print("\nTABLA COMPARATIVA")
print(df.to_string(index=False))

print("\nARCHIVO GENERADO:", archivo)
print("\nACTIVIDAD B2 FINALIZADA")
