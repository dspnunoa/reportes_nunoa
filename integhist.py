import pandas as pd

# Cargo archivo base
file = "2024p1.csv"
df = pd.read_csv(file,sep=";",engine="python")

# Imprimo el número de filas y columnas
print(f"Filas: {len(df):,}")
print(f"Columnas: {len(df.columns)}")

# Para cada columna imprime la cantidad de valores distintos encontrados
for columna in df.columns:
    cantidad = df[columna].nunique(dropna=False)
    print(f"{columna:50} -> {cantidad:,} valores distintos")

# Lista los valores distintos y su frencuencia para una columna en específico
print("*****************************")
print(df["VÍA DE INGRESO"].value_counts(dropna=False))

# Normalizo la columna para un mejor análisis
# df["TIPO NORM"] = (df["TIPO PROCED."].astype("string").str.strip().str.lower())
# print(df["TIPO NORM"].value_counts(dropna=False))