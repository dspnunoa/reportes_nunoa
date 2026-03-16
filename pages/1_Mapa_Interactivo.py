import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from shapely.geometry import Point, Polygon, box
from folium.plugins import HeatMap
from datetime import datetime

st.set_page_config(page_title="Mapa Interactivo", layout="wide")

st.title("📍 Mapa Interactivo Reportes Central Ñuñoa 2026")
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

# Inicializar session_state
if 'mostrar_mapa' not in st.session_state:
    st.session_state.mostrar_mapa = False
if 'cuadrante_filtro' not in st.session_state:
    st.session_state.cuadrante_filtro = None
if 'mapa_data' not in st.session_state:
    st.session_state.mapa_data = []

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


if st.button("Visualizar Mapa"):
    # Verificar si al menos un filtro está seleccionado
    if not any([ingreso, cuadrante, categoria, tipo, hinicio, hfinal, mes, ano, finicio, ffinal]):
        st.error("Por favor selecciona al menos un filtro")
    else:
        st.session_state.mostrar_mapa = True
        # Procesar datos
        c = []
        try:
            with open('datos_combinados.txt','r', encoding='utf-8') as file:
                for row in file:
                    lrow = row.split(',')
                    format_pattern = '%Y-%m-%d %H:%M' 
                    date_object = datetime.strptime(lrow[0], format_pattern)
                
                    # Verificar cada filtro (solo si está seleccionado)
                    cumple_filtros = True
                    
                    if ingreso and ingreso != lrow[1]:
                        cumple_filtros = False
                    
                    if cuadrante and cuadrante != lrow[4]:
                        cumple_filtros = False
                    
                    if categoria and categoria != lrow[2]:
                        cumple_filtros = False
                    
                    if tipo and tipo != lrow[3]:
                        cumple_filtros = False
                    
                    if ano and ano != date_object.year:
                        cumple_filtros = False
                    
                    if mes and mes != date_object.month:
                        cumple_filtros = False

                    if hinicio and not hfinal and hinicio > date_object.hour:
                        cumple_filtros = False

                    if hfinal and not hinicio and hfinal <= date_object.hour:
                        cumple_filtros = False

                    if hinicio and hfinal and hfinal > hinicio and (hinicio > date_object.hour or hfinal <= date_object.hour):
                        cumple_filtros = False

                    if hinicio and hfinal and hfinal < hinicio and (hinicio > date_object.hour and hfinal <= date_object.hour):
                        cumple_filtros = False

                    if finicio and finicio > date_object.date():
                        cumple_filtros = False

                    if ffinal and ffinal < date_object.date():
                        cumple_filtros = False                    
                    # Si cumple todos los filtros seleccionados, agregar el punto
                    if cumple_filtros:
                        if lrow[5] != 'None\n':
                            c.append([float(lrow[5]),float(lrow[6].strip('\n')),lrow[0],lrow[2],lrow[3],lrow[4]])
            
            file.close()
            st.session_state.mapa_data = c
            
        except FileNotFoundError:
            st.error("No se encontró el archivo sample.txt")
##
# Mostrar mapa si se aplicó el filtro
if st.session_state.mostrar_mapa:
    st.subheader("Instrucciones")
    st.info("💡 Dibuja un círculo o rectángulo en el mapa para contar los puntos dentro.")
    
    
    # Opción para mostrar/ocultar heatmap
    st.subheader("Opciones")
    mostrar_heatmap = st.checkbox("Mostrar Heatmap", value=True)
    
    # Crear mapa
    m = folium.Map(
        location=[-33.45588734763029, -70.5937367619373],
        zoom_start=13
    )
    
    # Preparar datos para heatmap
    heat_data = [[element[0], element[1]] for element in st.session_state.mapa_data]
    
    # Agregar heatmap si está activado
    if mostrar_heatmap and len(heat_data) > 0:
        custom_gradient = {
            0.4: 'green',
            0.6: 'yellow',
            0.8: 'red'
        }
        HeatMap(heat_data, gradient=custom_gradient,radius=20, blur=15, max_zoom=1).add_to(m)
    
    # Agregar marcadores con CircleMarker
    for element in st.session_state.mapa_data:
        folium.CircleMarker(
            location=[element[0], element[1]],
            radius=5,
            popup=folium.Popup(element[2], max_width=1000),
            color="#000000",
            fill=True,
            fillColor="#000000",
            fillOpacity=0.7,
            weight=1
        ).add_to(m)
    
    # Agregar herramienta de dibujo
    from folium.plugins import Draw
    Draw(export=False).add_to(m)
    
    # Renderizar mapa y capturar interacciones
    map_key = f"map_{len(st.session_state.mapa_data)}_{st.session_state.cuadrante_filtro}"
    map_data = st_folium(m, width=700, height=500, key=map_key)
    
    st.success(f"✅ Total de puntos: {len(st.session_state.mapa_data)}")
    
    
    # PROCESAR TODAS LAS FORMAS DIBUJADAS
    if map_data and map_data.get('all_drawings'):
        for idx, drawing in enumerate(map_data['all_drawings']):
            geom_type = drawing['geometry']['type']
            
            # CÍRCULO
            if geom_type == 'Point' and 'radius' in drawing['properties']:
                st.markdown("---")
                st.subheader(f"📊 Análisis de Círculo #{idx + 1}")
                
                polygon_coords = map_data['last_circle_polygon']['coordinates'][0]
                poligono = Polygon(polygon_coords)
                
                puntos_dentro = []
                for element in st.session_state.mapa_data:
                    punto = Point(element[1], element[0])
                    if poligono.contains(punto):
                        puntos_dentro.append([element[2],element[3],element[4],element[5]])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Puntos dentro del círculo", len(puntos_dentro))
                with col2:
                    st.metric("Puntos fuera", len(st.session_state.mapa_data) - len(puntos_dentro))
                
                if puntos_dentro:
                    st.subheader("Puntos dentro del círculo")
                    df_puntos = pd.DataFrame(puntos_dentro)
                    df_puntos.columns = ['Fecha','Categoría','Tipo de Procedimiento','Cuadrante']
                    st.dataframe(df_puntos, width='stretch', hide_index=True)

                    st.subheader("Resumen por Tipo")
                    conteo_tipos = df_puntos['Tipo de Procedimiento'].value_counts().reset_index()
                    conteo_tipos.columns = ['Tipo de procedimiento', 'Frecuencia']
                    st.dataframe(conteo_tipos, width='stretch', hide_index=True)
            
            # RECTÁNGULO O POLÍGONO
            elif geom_type == 'Polygon':
                st.markdown("---")
                st.subheader(f"📊 Análisis de Rectángulo #{idx + 1}")
                
                coords = drawing['geometry']['coordinates'][0]
                poligono = Polygon(coords)
                
                puntos_dentro = []
                for element in st.session_state.mapa_data:
                    punto = Point(element[1], element[0])
                    if poligono.contains(punto):
                        puntos_dentro.append([element[2],element[3],element[4],element[5]])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Puntos dentro del rectángulo", len(puntos_dentro))
                with col2:
                    st.metric("Puntos fuera", len(st.session_state.mapa_data) - len(puntos_dentro))
                
                if puntos_dentro:
                    st.subheader("Puntos dentro del rectángulo")
                    df_puntos = pd.DataFrame(puntos_dentro)
                    df_puntos.columns = ['Fecha','Categoría','Tipo de Procedimiento','Cuadrante']
                    st.dataframe(df_puntos, width='stretch', hide_index=True)
                    
                    st.subheader("Resumen por Tipo")
                    conteo_tipos = df_puntos['Tipo de Procedimiento'].value_counts().reset_index()
                    conteo_tipos.columns = ['Tipo de procedimiento', 'Frecuencia']
                    st.dataframe(conteo_tipos, width='stretch', hide_index=True)