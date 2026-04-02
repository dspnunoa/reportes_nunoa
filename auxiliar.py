import pandas as pd
import numpy as np

## Aquí va el nombre del archivo a añadir. Se recomienda un nombre breve tipo: infoMESAÑO. Aqui va el nombre sin la extensión (que debe ser siempre csv) ##
new_file = 'info'

## Con la librería pandas creo un dataframe del archivo leído ##
df = pd.read_csv(new_file+'.csv',sep=';',engine='python')

## Elimino las filas y columnas vacías ##
# df = df.dropna(axis=0,how='all')
# df = df.dropna(axis=1,how='all')


## Creo funciones que corrigen los errores ##
def fcalle(valor):
    if valor == 'Seguridad':
        return ''
    return str(valor).title()
def fcuadrante(valor):
    if valor == '118':
        return 'Nro. 118'
    elif valor == '119':
        return 'Nro. 119'
    elif valor == '120':
        return 'Nro. 120'
    elif valor == '121':
        return 'Nro. 121'
    elif valor == '129':
        return 'Nro. 129'
    elif valor == '130':
        return 'Nro. 130'
    elif valor == '131':
        return 'Nro. 131'
    elif valor == '132':
        return 'Nro. 132'
    elif valor == '133':
        return 'Nro. 133'
    elif valor == 'NO APLICA':
        return 'No aplica'
    elif valor == 'NO APLICA ':
        return 'No aplica'
    return valor
def fcanalingreso(valor):
    if valor == 'VECINO':
        return 'VECINO/A'
    elif valor == 'Cámaras':
        return 'OPERADOR CÁMARAS'
    elif valor == 'Iniciativa Propia':
        return 'INTERNO'
    elif valor == 'Interno':
        return 'INTERNO'
    elif valor == 'Jefatura':
        return 'JEFATURA'
    elif valor == 'RADIO':
        return 'INTERNO'
    elif valor == 'Whatsapp':
        return 'INTERNO'
    elif valor == 'WHATSAPP':
        return 'INTERNO'
    elif valor == 'INSPECTOR EN TERRENO':
        return 'INTERNO'
    elif valor == 'Otros':
        return 'OTROS'
    return valor
## Para verificar que todo el archivo tenga la misma estructua, comparo los campos del nuevo archivo con los del actual ##
# campos = list(df.columns)
# campos_final = ['NRO','ID ASIGNADO /TICKET','FECHA Y HORA','OPERADOR','CANAL DE INGRESO','TIPO DE RECURRENTE','AREA O SECCIÓN DEL RECURRENTE','NOMBRE DE RECURRENTE','TELEFONO RECURRENTE','DESCRIPCION DEL PROCEDIMIENTO (DETALLES RELEVANTES)','CATEGORIA','TIPO DE PROCEDIMIENTO','CALLE','NUMERACIÓN','CALLE QUE INTERSECTA','LUGAR PÚBLICO /  PRIVADO','ACLARATORIA DE LA UBICACIÓN','CUADRANTE','RADIOPERADOR DE TURNO','NRO DE MOVIL','INSPECTOR ASIGNADO AL PROCEDIMIENTO','ESTADO DEL PROCEDIMIENTO','HORA DE ASIGNACION A INSPECTOR','HORA DE ARRIBO','HORA DE TERMINO','INFORME','FINALIZACIÓN','APOYO/ASISTENCIA','COMISARIA','SEREMI','DERIVACIÓN A OTRA COMUNA',"OBSERVACIONES , DATOS GENERALES , ADICIONALES",'CONNOTACIÓN','COORDENADAS']
# for element in campos_final:
#     if element not in campos:
#         df[element] = np.nan

## Le doy el orden correcto ##
df = df[['NRO','ID ASIGNADO /TICKET','FECHA Y HORA','OPERADOR','CANAL DE INGRESO','TIPO DE RECURRENTE','AREA O SECCIÓN DEL RECURRENTE','NOMBRE DE RECURRENTE','TELEFONO RECURRENTE','DESCRIPCION DEL PROCEDIMIENTO (DETALLES RELEVANTES)','CATEGORIA','TIPO DE PROCEDIMIENTO','CALLE','NUMERACIÓN','CALLE QUE INTERSECTA','LUGAR PÚBLICO /  PRIVADO','ACLARATORIA DE LA UBICACIÓN','CUADRANTE','RADIOPERADOR DE TURNO','NRO DE MOVIL','INSPECTOR ASIGNADO AL PROCEDIMIENTO','ESTADO DEL PROCEDIMIENTO','HORA DE ASIGNACION A INSPECTOR','HORA DE ARRIBO','HORA DE TERMINO','INFORME','FINALIZACIÓN','APOYO/ASISTENCIA','COMISARIA','SEREMI','DERIVACIÓN A OTRA COMUNA',"OBSERVACIONES , DATOS GENERALES , ADICIONALES",'CONNOTACIÓN','COORDENADAS']]

## Aplico las funciones al nuevo archivo ##
# df['CUADRANTE'] = df['CUADRANTE'].apply(fcuadrante)
# df['CANAL DE INGRESO'] = df['CANAL DE INGRESO'].apply(fcanalingreso)
df['CALLE'] = df['CALLE'].apply(fcalle)

## Imprimo los elementos diferentes que hay en un campo en especifico (para corregir errores) ##
lfinal = ['7X3 delitos violentos', 'Accidente de tránsito (choque/colisión/atropello)', 'Acera en mal estado', 'Actividad sospechosa', 'Agresión', 'Alarma activada', 'Alcantarilla colapsada', 'Amenazas', 'Anegamiento de calle y paso bajo nivel', 'Anegamiento domicilios', 'Apoyo a Bomberos', 'Apoyo a Carabineros', 'Apoyo a SAMU', 'Artefacto explosivo o paquete sospechoso', 'Botar chicle, colillas o desechos en la vía pública', 'Cables a baja altura / Cables cortados', 'Caida de arbol', 'Carpa o Ruco en BNUP', 'Circuito y luminarias dañadas', 'Comercio ambulante Ilegal', 'Consumo de alcohol en vía pública', 'Consumo de drogas', 'Control de Transito', 'Corte energía eléctrica', 'Corte suministro de agua potable', 'Daños propiedad privada', 'Daños propiedad pública', 'Delito sexual', 'Desganche arbolado', 'Detención ciudadana', 'Detenidos', 'Disparos', 'Disturbios', 'Ebriedad', 'Emanación de gas/ Derrame o Materiales peligrosos', 
'Emergencia de salud', 'Filtración agua potable', 'Fiscalizacion Retiro de circulación de vehiculo motorizado', 'Fiscalizacion Ruidos Molestos', 'Fiscalizaciones (BNUP, comercio, etc)', 'Fiscalización alcoholes', 'Fiscalización aparcadores ilegales', 'Fiscalización de tránsito', 'Fiscalización ingesta de alcohol en vía pública', 'Fuegos artificiales', 'Homicidio', 'Homicidio Frustrado', 'Hurto', 
'Incendio o amago', 'Incumplimiento medida cautelar', 'Labores administrativas', 'Maltrato animal', 'Marchas/manifestaciones', 'Mascota atrapada/perdida', 'Microbasural', 'Motochorros ', 'Novedades Central', 'Operativo Conjunto Carabineros', 'Operativo Conjunto a otras Municipalidades', 'Operativo MTT', 'Operativo Seremi Salud', 'Operativo conjunto Delegación Presidencial', 'Operativo conjunto Dirección de Inspección', 'Operativo otras direcciones Municilapales', 'Operativos Conjunto PDI', 'Otra contingencia BNUP', 'Otros', 'P.V.P', 'Patrulla Mixta', 'Patrullaje focalizado Carabineros', 'Patrullaje focalizado Preventivo', 'Patrullaje preventivo general', 'Pavimento en mal estado', 'Persona extraviada / desorientada', 'Persona situación de calle', 'Posible Fallecido/Emergencia de Salud', 
'Posible sospechoso al interior', 'Postes dañados', 'Punto fijo', 'Riña', 'Robo con intimidación', 'Robo con violencia', 'Robo de especies de o desde vehículo', 'Robo de vehículo en BNUP', 'Robo en BNUP', 'Robo en lugar habitado', 'Robo en lugar no habitado', 'Robo frustrado', 'Robo por sorpresa', 'Ruta calle', 'Semáforo defectuoso', 'Servicio Estadio', 'Servicio FEI', 'Servicio especial Colegios', 'Servicio turístico Plaza Ñuñoa-Barrio Italia', 'Señalética o elemento caida', 'Suicidio/Intento', 'Tapa de servicios', 'Toma establecimiento educacional', 'Trabajos fuera de horario', 'Trafico Drogas', 'Traslado de documentos o funcionarios/limpieza de móvil', 'VIF', 'Vehiculo MAL Estacionado', 'Vehiculo sospechoso', 'Vehículo abandonado', 'Vehículo con encargo', 'Vehículo sospechoso', 'Vigilancia especial', 'Vulneración NNA', 'Vulneración derechos adultos mayores', 'Realizacion de Graffitis / Pintar sin autorización', 'Servicio DRONE', 'nan']
# lprod = list(df['TIPO DE PROCEDIMIENTO'].unique())
# for element in lprod:
#     if element not in lfinal:
#         print(str(element))

## Imprime las entradas con un valor específico en un campo a especificar ##
# for index, row in df.iterrows():
#     if str(row['TIPO DE PROCEDIMIENTO']) == 'ESCOMBROS EN DOMICILIO':
#         print(row['FECHA Y HORA']) 

## Lo guardo en un nuevo archivo que tendrá el mismo nombre que el original pero + 'P' al final, para poder diferenciarlo ##
#df.to_csv(new_file+'P.csv', index=False,sep=';')

