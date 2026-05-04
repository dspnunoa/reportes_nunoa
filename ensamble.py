import pandas as pd

## CONCATENAR DOS CSV EN UNO ##
## Aquí crea las variables de los archivos que quieras unir ##
file1 = 'info.csv'
file2 = 'abrilp2.csv'

## Aquí crea el dataframe asociado a cada archivo ##
df1 = pd.read_csv(file1, encoding='utf-8',sep=';')
df2 = pd.read_csv(file2, encoding='utf-8',sep=';')

## Unes aquí todos los dataframes en una lista ##
frames = [df1,df2]

## Concatenas todo ##
result = pd.concat(frames)

## Imprimes el resultado ##
print(result)

## Guardas el .csv con la información unificada ##
result.to_csv('infop.csv', index=False,sep=';')

## AGREGAR COORDENADAS A ARCHIVO SIN COORDENADAS ##
# file1 = "infoadd"
# file2 = "CALLESP"

# df1 = pd.read_csv(file1+'.csv', encoding='utf-8',sep=';')
# df2 = pd.read_csv(file2+'.csv', encoding='utf-8',sep=';')

# df1["COORDENADAS"] = df2["COORDENADAS"]

# df1.to_csv("infoaddP.csv", index=False,sep=';')