from datetime import datetime
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tabla Interactiva", layout="wide")

st.title("📋 Tablas Reportes Central Ñuñoa 2026")

# Título y botones en una fila
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    if st.button("Inicio", key="nav_home",width='stretch'):
        st.switch_page("app.py")
        
with col2:
    if st.button("Mapa Interactivo", key="nav_mapa", width='stretch'):
        st.switch_page("pages/1_Mapa_Interactivo.py")

with col3:
    if st.button("Dashboard", key="nav_dash", width='stretch'):
        st.switch_page("pages/2_Dashboard.py")

with col4:
    if st.button("Tabla Interactiva", key="nav_tabla", width='stretch'):
        st.switch_page("pages/3_Tabla_Interactiva.py")

st.markdown("---")

st.subheader("Filtros")
##
op_ingreso = ['1445', 'EXTERNO','INSPECTOR EN TERRENO','INTERNO','JEFATURA','OPERADOR CÁMARAS','PROALERT','SOSAFE','WHATSAPP','OTROS']
op_cuadrantes = ['Nro. 118','Nro. 119','Nro. 120','Nro. 121','Nro. 129','Nro. 130','Nro. 131','Nro. 132','Nro. 133','No aplica']
op_categoria = ['Seguridad','Planes Operativos','Emergencia/Espacio Públicos','Fiscalización','Incivilidades','Otros']
op_tipo = ['7X3 delitos violentos', 'Accidente de tránsito (choque/colisión)', 'Acera en mal estado', 'Actividad sospechosa', 'Agresión', 'Alarma activada', 'Alcantarilla colapsada', 'Amenazas', 'Anegamiento de calle y paso bajo nivel', 'Anegamiento domicilios', 'Artefacto explosivo o paquete sospechoso', 'Atropello', 'Botar chicle, colillas o desechos en la vía pública', 'CAIDA DE ARBOL', 'Cables a baja altura / Cables cortados', 'Carpa o Ruco en BNUP', 'Circuito y luminarias dañadas', 'Comercio ambulante ILEGAL', 'Consumo de alcohol en vía pública', 'Consumo de drogas', 'Control de Transito', 'Corte energía eléctrica', 'Corte suministro de agua potable', 'DESGANCHE DE ARBOLADO', 'Daños propiedad privada', 'Daños propiedad pública', 'Delito sexual', 'Detención ciudadana', 'Detenidos', 'Disparos', 'Disturbios', 'Ebriedad', 'Emanación de gas', 'Emergencia de salud', 'Filtración agua potable', 'Fiscalizacion Retiro de circulación de vehiculo motorizado', 'Fiscalizacion Ruidos Molestos', 'Fiscalizaciones (BNUP, comercio, etc)', 'Fiscalización alcoholes', 'Fiscalización aparcadores ilegales', 'Fiscalización de tránsito', 'Fiscalización ingesta de alcohol en vía pública', 'Fuegos artificiales', 'Homicidio', 'Hurto', 'Incendio o amago', 'Labores administrativas', 'Maltrato animal', 'Marchas/manifestaciones', 'Mascota atrapada', 'Microbasural', 'Novedades Central', 'Operativo Conjunto Carabineros', 'Operativo Conjunto a otras Municipalidades', 'Operativo MTT', 'Operativo Seremi Salud', 'Operativo conjunto Delegación Presidencial', 'Operativo conjunto Dirección de Inspección', 'Operativo otras direcciones Municilapales', 'Operativos Conjunto PDI', 'Otra contingencia BNUP', 'Emergencia/Otros', 'Fiscalización/Otros', 'Incivilidades/Otros', 'Planes Operativos/Otros', 'Seguridad/Otros', 'Otros/Otros', 'P.V.P', 'Patrulla Mixta', 'Patrullaje focalizado Carabineros', 'Patrullaje focalizado Preventivo', 'Patrullaje preventivo general', 'Pavimento en mal estado', 'Persona extraviada', 'Persona situación de calle', 'Posible Fallecido/Emergencia de Salud', 'Posible sospechoso al interior', 'Postes dañados', 'Punto fijo', 'Riña', 'Robo con intimidación', 'Robo con violencia', 'Robo de especies de o desde vehículo', 'Robo de vehículo en BNUP', 'Robo en BNUP', 'Robo en lugar habitado', 'Robo en lugar no habitado', 'Robo frustrado', 'Robo por sorpresa', 'Ruta calle', 'Semáforo defectuoso', 'Servicio Estadio', 'Servicio FEI', 'Servicio especial Colegios', 'Servicio turístico Plaza Ñuñoa-Barrio Italia', 'Señalética o elemento caida', 'Tapa de servicios', 'Toma establecimiento educacional', 'Trabajos fuera de horario', 'Trafico Drogas', 'Traslado de documentos o funcionarios/limpieza de móvil', 'VIF', 'Vehiculo sospechoso', 'Vehículo abandonado', 'Vehículo con encargo', 'Vigilancia especial', 'Vulneración NNA', 'Vulneración derechos adultos mayores']
op_hinicio = {0:'00:00',1:'01:00',2:'02:00',3:'03:00',4:'04:00',5:'05:00',6:'06:00',7:'07:00',8:'08:00',9:'09:00',10:'10:00',11:'11:00',12:'12:00',13:'13:00',14:'14:00',15:'15:00',16:'16:00',17:'17:00',18:'18:00',19:'19:00',20:'20:00',21:'21:00',22:'22:00',23:'23:00',24:'24:00'}
op_hfinal = {0:'00:00',1:'01:00',2:'02:00',3:'03:00',4:'04:00',5:'05:00',6:'06:00',7:'07:00',8:'08:00',9:'09:00',10:'10:00',11:'11:00',12:'12:00',13:'13:00',14:'14:00',15:'15:00',16:'16:00',17:'17:00',18:'18:00',19:'19:00',20:'20:00',21:'21:00',22:'22:00',23:'23:00', 24:'24:00'}
op_mes = {1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'}
op_ano = [2020,2021,2022,2023,2024,2025,2026]
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)

with col1:
    ingreso = st.selectbox("Vía de Ingreso", op_ingreso, index=None,placeholder='Elige')
with col2:
    cuadrante = st.selectbox("Cuadrante", op_cuadrantes, index=None,placeholder='Elige')
with col3:
    categoria = st.selectbox("Categoría", op_categoria, index=None,placeholder='Elige')
with col4:
    tipo = st.selectbox("Tipo", op_tipo, index=None,placeholder='Elige')
with col5:
    hinicio = st.selectbox("Inicio", op_hinicio, index=None,placeholder='Elige')
with col6:
    hfinal = st.selectbox("Final", op_hfinal, index=None,placeholder='Elige')
with col7:
    mes = st.selectbox("Mes", op_mes, index=None,placeholder='Elige')
with col8:
    ano = st.selectbox("Año", op_ano, index=None,placeholder='Elige')
with col9:
    finicio = st.date_input("Desde", value=None)
with col10:
    ffinal = st.date_input("Hasta", value=None)

## Cargo el archivo .csv ##
# df1 = pd.read_csv('infoenero.csv')
# df2 = pd.read_csv('infofebrero.csv')

# df = pd.concat([df1, df2], ignore_index=True)

# df.to_csv('infofinal.csv', index=False)
df = pd.read_csv('infofinaltest.csv')
###########################
df = df.dropna(subset=['ID ASIGNADO /TICKET'])
df_filtrado = df.copy()
df_filtrado['FECHA Y HORA'] = pd.to_datetime(df_filtrado['FECHA Y HORA'])

if ingreso:
    df_filtrado = df_filtrado[df_filtrado['CANAL DE INGRESO'] == ingreso]
if cuadrante:
     df_filtrado = df_filtrado[df_filtrado['CUADRANTE'] == cuadrante]
if categoria:
    df_filtrado = df_filtrado[df_filtrado['CATEGORIA'] == categoria]
if tipo:
    df_filtrado = df_filtrado[df_filtrado['TIPO DE PROCEDIMIENTO'] == tipo]
if mes:
    df_filtrado = df_filtrado[df_filtrado['FECHA Y HORA'].dt.month == mes]
if ano:
    df_filtrado = df_filtrado[df_filtrado['FECHA Y HORA'].dt.year == ano]
if hinicio and hfinal and hinicio > hfinal:
    df_filtrado = df_filtrado[(df_filtrado['FECHA Y HORA'].dt.hour >= hinicio) | (df_filtrado['FECHA Y HORA'].dt.hour < hfinal)]
if hinicio and hfinal and hinicio < hfinal:
    df_filtrado = df_filtrado[(df_filtrado['FECHA Y HORA'].dt.hour >= hinicio) & (df_filtrado['FECHA Y HORA'].dt.hour < hfinal)]
if hinicio and not hfinal:
    df_filtrado = df_filtrado[df_filtrado['FECHA Y HORA'].dt.hour >= hinicio]
if hfinal and not hinicio:
    df_filtrado = df_filtrado[df_filtrado['FECHA Y HORA'].dt.hour < hfinal]
if finicio:
    df_filtrado = df_filtrado[df_filtrado['FECHA Y HORA'].dt.date >= finicio]
if ffinal:
    df_filtrado = df_filtrado[df_filtrado['FECHA Y HORA'].dt.date <= ffinal]
    
st.subheader("Resultados")
st.write(f"Total de registros: {len(df_filtrado)}")
st.dataframe(df_filtrado[df_filtrado.columns[2:25]], width='stretch')