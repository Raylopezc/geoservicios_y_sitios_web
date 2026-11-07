import pandas as pd
from pathlib import Path

datos = [
    {
        "TAMANO_BLOQUE": 1000,
        "TOTAL_VEREDAS": 1712,
        "MUNICIPIOS_DISTINTOS": 123,
        "ITERACIONES": 2
    },
    {
        "TAMANO_BLOQUE": 500,
        "TOTAL_VEREDAS": 1712,
        "MUNICIPIOS_DISTINTOS": 123,
        "ITERACIONES": 4
    }
]

df = pd.DataFrame(datos)

salida = Path(
    r"C:\Users\Ray Lopez\servicios-sig\Entrega_Ruta_B\02_APIs_JSON\02_Resultados\comparacion_paginacion.csv"
)

df.to_csv(salida, index=False, encoding="utf-8-sig")

print("TABLA COMPARATIVA GENERADA")
print(df.to_string(index=False))
print("ARCHIVO:", salida)
