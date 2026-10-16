from datetime import datetime
import pandas as pd

# Cargo archivo base
file = "2023_2024.csv"
df = pd.read_csv(file,sep=";",engine="python")
df = df.dropna(axis=1, how='all')

# Funciones
def fcanal(valor):
    if valor == 'Whatsapp':
        return 'WHATSAPP'
    elif valor == 'Radio':
        return 'RADIAL'
    elif valor == 'Cámaras':
        return 'CAMARAS'
    elif valor == 'Otros' or valor == 'DPTO INNOVACIÓN' or valor == 'CENCO':
        return 'OTROS'
    elif pd.isna(valor) == False:
         valor = valor.upper()
    return valor
def ftiporec(valor):
    if valor == 'INTERNO' or valor == 'interno' or valor == 'ÍNTERNO':
        return 'Interno'
    elif valor == 'VECINO/A':
        return 'Vecino/a'
    return valor
def fcat(valor):
    if valor == 'SEGURIDAD':
        return 'Seguridad'
    elif valor == 'SEGURIDAD (prevención)' or valor == 'SEGURIDAD (PREVENCION)' or valor == 'SEGURIDAD Y PREVENCION':
        return 'Seguridad (prevención)'
    elif valor == 'FISCALIZACION' or valor == 'FISCALIZACIÓN':
        return 'Fiscalización'
    elif valor == 'OTROS':
        return 'Otros'
    elif valor == 'constancia' or valor == 'R.DONOSO' or valor == 'SOSPECHOSO' or valor == 'CONSTANCIA' or valor == 'CONTINGENCIA BNUP':
        return 'Otros'
    elif pd.isna(valor):
        return 'XXXX'
    return valor
def fplanb(valor):
    if valor == 'NO' or valor == 'no':
        return 'No'
    elif valor == 'SI':
        return 'Sí'
    return valor
def fop(valor):
    if valor == 'JOSE LUIS MOLINA':
        return 'JOSÉ LUIS MOLINA'
    elif valor == '-+' or valor == '65' or valor == 'XXXX' or valor == 'xxx' or valor == '27-07-2024' or valor == '06-05-2024':
        return 'OTROS'
    elif valor == 'ROXAN DIAZ' or valor == 'ROXANA DAZ' or valor == 'ROXANA DIAz' or valor == 'ROXAA DIAZ' or valor == 'ROXANA DIZ' or valor == 'ROZXANA DIAZ' or valor == 'ROXANADIAZ' or valor == 'ROXANA DIAX':
        return 'ROXANA DÍAZ'
    return valor
def  farec(valor):
    if pd.isna(valor) == False and '.' in valor:
        if valor.split('.')[1] == '0':
            return valor.split('.')[0]
    if  pd.isna(valor) == False and valor.isnumeric() == False:
        return 'OTROS'
    return valor
def ftipo(valor):
    if valor == 'ACCIDENTE DE TRANSITO' or valor == 'ACCIDENTE DE TRÁNSITO (CHOQUE/COLISIÓN)':
        return 'ACCIDENTE DE TRÁNSITO (CHOQUE / COLISIÓN)'
    elif valor == 'CABLES':
        return 'CABLES A BAJA ALTURA / CABLES CORTADOS'
    elif valor == 'VEHICULO MAL ESTACIONADO' or valor == 'VEHICULOS MAL ESTACIONADOS' or valor == 'VEHÍCHULO MAL ESTACIONADO':
        return 'VEHÍCHULO MAL ESTACIONADO'
    elif valor == 'CONSUMO DE ALCOHOL EN LA VÍA PÚBLICA':
        return 'CONSUMO DE ALCOHOL EN VÍA PÚBLICA'
    elif valor == 'DELIVERY':
        return 'OTROS'
    elif valor == 'DETENCIÓN CIUDADANA ':
        return 'DETENCIÓN CIUDADANA'
    elif valor == 'FISCALIZACIONES (BNUP, COMERCIO, ETC)':
        return 'FISCALIZACIONES (BPNU, COMERCIO, ETC.)'
    elif valor == 'MARCHAS/MANIFESTACIONES':
        return 'MARCHAS / MANIFESTACIONES'
    elif valor == 'PLA' or valor == 'PLAN':
        return 'PLAN BARRIAL'
    elif valor == 'PUN':
        return 'PUNTO FIJO'
    elif valor == 'PERSONAS SITUACION CALLE' or valor == 'PERSONAS SITUACIÓN DE CALLE':
        return 'PERSONA SITUACIÓN DE CALLE'
    elif valor == 'ROBO ESPECIES DE VEHICULO':
        return 'ROBO DE ESPECIES DE O DESDE VEHÍCULO'
    elif valor == 'RUIDOS':
        return 'RUIDOS MOLESTOS'
    elif valor == 'SOSPECHOSOS':
        return 'SOSPECHOSO'
    elif valor == 'TRASLADO DE DOCUMENTOS O FUNCIONARIOS/LIMPIEZA DE MÓVIL':
        return 'TRASLADO DE DOCUMENTOS O FUNCIONARIOS / LIMPIEZA DE MÓVIL'
    elif valor == 'VEHICULO CON ENCARGO':
        return 'VEHÍCULO CON ENCARGO'
    elif valor == 'VIGILANCIA ESPECIA':
        return 'VIGILANCIA ESPECIAL'
    return valor
def fcuad(valor):
    if pd.isna(valor) == False and '.' in valor:
        if valor.split('.')[1] == '0':
            return valor.split('.')[0]
    if pd.isna(valor) == True:
       return 'XXXX'
    if ':' in valor:
        return 'XXXX'
    if valor.isnumeric() == False:
        return 'XXXX'
    if valor.isnumeric():
        nval = int(valor)
        if nval > 133 or nval < 118 or nval == 123 or nval == 126:
            return 'XXXX'
    return valor
def fuv(valor):
    if pd.isna(valor) == False and '.' in valor:
        if valor.split('.')[1] == '0':
            return valor.split('.')[0]
    if pd.isna(valor) == False and valor.isnumeric() == False:
        return 'XXXX'
    if pd.isna(valor):
        return 'XXXX'
    if pd.isna(valor) == False and valor.isnumeric() and (int(valor) > 37 or int(valor) < 1):
        return 'XXXX'
    return valor
def fpb(valor):
    if valor == 'No':
        return 'NO'
    elif valor == 'Sí' or valor == 'SÍ':
        return 'SI'
    return valor
def fradiop(valor):
    if valor == 'ALfredo perez' or valor == 'alfredo perez':
        return 'ALFREDO PEREZ'
    elif valor == 'HECTOR GODOY':
        return 'HÉCTOR GODOY'
    elif valor == 'JOSE LUIS MOLINA':
        return 'JOSÉ LUIS MOLINA'
    elif valor == 'PAMELA MOLINA ':
        return 'PAMELA MOLINA'
    elif valor == 'ROBERTO MARTINEZ':
        return 'ROBERTO MARTÍNEZ'
    elif valor == 'ROXANA DIAZ':
        return 'ROXANA DÍAZ'
    elif valor == 'SEBASTIAN POBLETE':
        return 'SEBASTIÁN POBLETE'
    elif valor == 'TACURY RODRIGUEZ':
        return 'TAKURI RODRIGUEZ'
    return valor

# Aplico funciones
# df['CANAL DE INGRESO'] = df['CANAL DE INGRESO'].apply(fcanal)
# df['TIPO DE RECURRENTE'] = df['TIPO DE RECURRENTE'].apply(ftiporec)
# df['CATEGORIA'] = df['CATEGORIA'].apply(fcat)
# df['OPERADOR'] = df['OPERADOR'].apply(fop)
# df['NRO'] = range(1,len(df)+1)
# df['PLAN BARRIAL'] = df['PLAN BARRIAL'].apply(fplanb)
# df['AREA O SECCIÓN DEL RECURRENTE'] = df['AREA O SECCIÓN DEL RECURRENTE'].apply(farec)
# df['TIPO DE PROCEDIMIENTO'] = df['TIPO DE PROCEDIMIENTO'].apply(ftipo)
# df['CUADRANTE'] = df['CUADRANTE'].apply(fcuad)
# df['UNIDAD VECINAL'] = df['UNIDAD VECINAL'].apply(fuv)
# df['PLAN BARRIAL'] = df['PLAN BARRIAL'].apply(fpb)
# df['RADIOPERADOR DE TURNO'] = df['RADIOPERADOR DE TURNO'].apply(fradiop)

# Junto columnas
# df['CATEGORIA'] = df['CATEGORIA'].fillna(df['Unnamed: 27'])
# df['TIPO DE PROCEDIMIENTO'] = df['TIPO DE PROCEDIMIENTO'].fillna(df['Unnamed: 28'])

# Remuevo columna del Dataframe
# df = df.drop('Unnamed: 25', axis=1)

# Imprimo el número de filas y columnas
print(f"Filas: {len(df):,}")
print(f"Columnas: {len(df.columns)}")

# # Regex para manejo de errores de ingreso en horas
# # df["HORA"] = df["HORA"].astype("string").str.replace(".", ":", regex=False)


# # Para cada columna imprime la cantidad de valores distintos encontrados
for columna in df.columns:
    cantidad = df[columna].nunique(dropna=False)
    print(f"{columna:50} -> {cantidad:,} valores distintos")

# print("*****************************")
# Lista los valores distintos y su frencuencia para una columna en específico
# print(df["HORA DE TERMINO"].value_counts(dropna=False))

# Lo mismo que lo anterior pero imprime TODOS los resultados (en trabajos de gran volumen se recomienda exportar el resultado en un archivo .txt para poder verlo completo)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df["ESTADO DEL PROCEDIMIENTO"].value_counts(dropna=False))


# Paso los strings de fechas a su formato real y las ordeno
# lifechas = df["FECHA"].unique()
# lfechas = lifechas.tolist()
# fechas_ordenadas = sorted(
#     lfechas, key=lambda x: datetime.strptime(x, "%d-%m-%Y")
# )
# print(fechas_ordenadas)

# Hago una búsqueda y luego imprimo el Dataframe completo filtrado
# resultado = df[df["Unnamed: 29"].notnull()]
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(resultado)

# Filtro por columna todas las entradas con valores diferentes a los que están dentro del isin()
# df_filtrado = df[~df['ESTADO DEL PROCEDIMIENTO'].isin(['PENDIENTE', 'PROCESO', 'FINALIZADO'])]
# print(df_filtrado[df['ESTADO DEL PROCEDIMIENTO'].notnull()])

# Normalizo la columna para un mejor análisis
# df["TIPO NORM"] = (df["TIPO PROCED."].astype("string").str.strip().str.lower())
# print(df["TIPO NORM"].value_counts(dropna=False))

# Guardo los cambios hechos en un nuevo .csv
# df.to_csv('newv.csv', sep=';', encoding='utf-8',index=False)