import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from shapely.geometry import Point, Polygon
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
op_ingreso = ['1445', 'EXTERNO','INTERNO','JEFATURA','OPERADOR CÁMARAS','PROALERT','SOSAFE','OTROS', 'VECINO/A']
op_cuadrantes = ['Nro. 118','Nro. 119','Nro. 120','Nro. 121','Nro. 129','Nro. 130','Nro. 131','Nro. 132','Nro. 133','No aplica']
dop_categoria ={'Seguridad':['Servicio DRONE','Apoyo a Carabineros','Actividad sospechosa','Agresión','Alarma activada','Amenazas','Artefacto explosivo o paquete sospechoso','Daños propiedad privada','Daños propiedad pública','Delito sexual','Detención ciudadana','Detenidos','Disparos','Disturbios','Fuegos artificiales','Homicidio','Homicidio Frustrado','Hurto','Maltrato animal','Marchas/manifestaciones','Persona extraviada / desorientada','Posible sospechoso al interior','Riña','Robo con intimidación','Robo con violencia','Robo de especies de o desde vehículo','Robo de vehículo en BNUP','Robo en BNUP','Robo en lugar habitado','Robo en lugar no habitado','Robo frustrado','Robo por sorpresa','Toma establecimiento educacional','Trafico Drogas','Vehículo con encargo','Vehiculo sospechoso','Incumplimiento medida cautelar','VIF','Vulneración derechos adultos mayores','Vulneración NNA','Otros','Motochorros '],
                 'Planes Operativos':['7X3 delitos violentos','Control de Transito','Operativo Conjunto a otras Municipalidades','Operativo Conjunto Carabineros','Operativo conjunto Delegación Presidencial','Operativo conjunto Dirección de Inspección','Operativo MTT','Operativo otras direcciones Municilapales','Operativo Seremi Salud','Operativos Conjunto PDI','P.V.P','Patrulla Mixta','Patrullaje focalizado Carabineros','Patrullaje focalizado Preventivo','Patrullaje preventivo general','Punto fijo','Ruta calle','Servicio especial Colegios','Servicio Estadio','Servicio FEI','Servicio turístico Plaza Ñuñoa-Barrio Italia','Vigilancia especial','Otros'],
                 'Emergencia/Espacio Públicos':['Apoyo a Bomberos','Apoyo a SAMU','Accidente de tránsito (choque/colisión/atropello)','Acera en mal estado','Alcantarilla colapsada','Anegamiento de calle y paso bajo nivel','Anegamiento domicilios','Suicidio/Intento','Cables a baja altura / Cables cortados','Caida de arbol','Circuito y luminarias dañadas','Corte energía eléctrica','Corte suministro de agua potable','Desganche arbolado','Emanación de gas/ Derrame o Materiales peligrosos','Emergencia de salud','Filtración agua potable','Incendio o amago','Mascota atrapada/perdida','Pavimento en mal estado','Posible Fallecido/Emergencia de Salud','Postes dañados','Semáforo defectuoso','Señalética o elemento caida','Tapa de servicios','Otra contingencia BNUP','Otros'],
                 'Fiscalización':['Realizacion de Graffitis / Pintar sin autorización','Comercio ambulante Ilegal','Fiscalización alcoholes','Fiscalización aparcadores ilegales','Fiscalización de tránsito','Vehiculo MAL Estacionado','Vehículo sospechoso','Fiscalización ingesta de alcohol en vía pública','Fiscalizacion Retiro de circulación de vehiculo motorizado','Fiscalizacion Ruidos Molestos','Fiscalizaciones (BNUP, comercio, etc)','Trabajos fuera de horario','Vehículo abandonado','Otros'],
                 'Incivilidades':['Botar chicle, colillas o desechos en la vía pública','Carpa o Ruco en BNUP','Consumo de alcohol en vía pública','Consumo de drogas','Ebriedad','Microbasural','Persona situación de calle','Otros'],
                 'Otros':['Novedades Central','Labores administrativas','Traslado de documentos o funcionarios/limpieza de móvil','Otros']}
op_categoria = list(dop_categoria.keys())
op_tipo =['Servicio DRONE','Apoyo a Carabineros','Actividad sospechosa','Agresión','Alarma activada','Amenazas','Artefacto explosivo o paquete sospechoso','Daños propiedad privada','Daños propiedad pública','Delito sexual','Detención ciudadana','Detenidos','Disparos','Disturbios','Fuegos artificiales','Homicidio','Homicidio Frustrado','Hurto','Maltrato animal','Marchas/manifestaciones','Persona extraviada / desorientada','Posible sospechoso al interior','Riña','Robo con intimidación','Robo con violencia','Robo de especies de o desde vehículo','Robo de vehículo en BNUP','Robo en BNUP','Robo en lugar habitado','Robo en lugar no habitado','Robo frustrado','Robo por sorpresa','Toma establecimiento educacional','Trafico Drogas','Vehículo con encargo','Vehiculo sospechoso','Incumplimiento medida cautelar','VIF','Vulneración derechos adultos mayores','Vulneración NNA','Otros','Motochorros ','7X3 delitos violentos','Control de Transito','Operativo Conjunto a otras Municipalidades','Operativo Conjunto Carabineros','Operativo conjunto Delegación Presidencial','Operativo conjunto Dirección de Inspección','Operativo MTT','Operativo otras direcciones Municilapales','Operativo Seremi Salud','Operativos Conjunto PDI','P.V.P','Patrulla Mixta','Patrullaje focalizado Carabineros','Patrullaje focalizado Preventivo','Patrullaje preventivo general','Punto fijo','Ruta calle','Servicio especial Colegios','Servicio Estadio','Servicio FEI','Servicio turístico Plaza Ñuñoa-Barrio Italia','Vigilancia especial','Otros','Apoyo a Bomberos','Apoyo a SAMU','Accidente de tránsito (choque/colisión/atropello)','Acera en mal estado','Alcantarilla colapsada','Anegamiento de calle y paso bajo nivel','Anegamiento domicilios','Suicidio/Intento','Cables a baja altura / Cables cortados','Caida de arbol','Circuito y luminarias dañadas','Corte energía eléctrica','Corte suministro de agua potable','Desganche arbolado','Emanación de gas/ Derrame o Materiales peligrosos','Emergencia de salud','Filtración agua potable','Incendio o amago','Mascota atrapada/perdida','Pavimento en mal estado','Posible Fallecido/Emergencia de Salud','Postes dañados','Semáforo defectuoso','Señalética o elemento caida','Tapa de servicios','Otra contingencia BNUP','Otros','Realizacion de Graffitis / Pintar sin autorización','Comercio ambulante Ilegal','Fiscalización alcoholes','Fiscalización aparcadores ilegales','Fiscalización de tránsito','Vehiculo MAL Estacionado','Vehículo sospechoso','Fiscalización ingesta de alcohol en vía pública','Fiscalizacion Retiro de circulación de vehiculo motorizado','Fiscalizacion Ruidos Molestos','Fiscalizaciones (BNUP, comercio, etc)','Trabajos fuera de horario','Vehículo abandonado','Otros','Botar chicle, colillas o desechos en la vía pública','Carpa o Ruco en BNUP','Consumo de alcohol en vía pública','Consumo de drogas','Ebriedad','Microbasural','Persona situación de calle','Otros','Novedades Central','Labores administrativas','Traslado de documentos o funcionarios/limpieza de móvil','Otros','Patrullaje preventivo', 'Focalizado municipal', 'Fiscalización conjunta (Carabineros, PDI)', 'Operativos conjuntos: colaboración con Carabineros, PDI', 'Fiscalización', 'Ruidos Molestos', 'Retiro de enseres de la via publica', 'Seguridad (prevención)', 'Seguridad', 'Robo tapa alcantarilla ']
op_hinicio = {0:'00:00',1:'01:00',2:'02:00',3:'03:00',4:'04:00',5:'05:00',6:'06:00',7:'07:00',8:'08:00',9:'09:00',10:'10:00',11:'11:00',12:'12:00',13:'13:00',14:'14:00',15:'15:00',16:'16:00',17:'17:00',18:'18:00',19:'19:00',20:'20:00',21:'21:00',22:'22:00',23:'23:00',24:'24:00'}
op_hfinal = {0:'00:00',1:'01:00',2:'02:00',3:'03:00',4:'04:00',5:'05:00',6:'06:00',7:'07:00',8:'08:00',9:'09:00',10:'10:00',11:'11:00',12:'12:00',13:'13:00',14:'14:00',15:'15:00',16:'16:00',17:'17:00',18:'18:00',19:'19:00',20:'20:00',21:'21:00',22:'22:00',23:'23:00', 24:'24:00'}
op_mes = {1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'}
op_ano = [2020,2021,2022,2023,2024,2025,2026]
##
opi_hinicio = list(op_hinicio.items())
opi_hfinal = list(op_hfinal.items())
opi_mes = list(op_mes.items())
col1, col2, col3, col4, col5 = st.columns(5)
col6, col7, col8, col9, col10 = st.columns(5)
##
with col1:
    ingreso = st.selectbox("Vía de Ingreso", op_ingreso, index=None,placeholder='Elige')
with col2:
    cuadrante = st.selectbox("Cuadrante", op_cuadrantes, index=None,placeholder='Elige')
with col3:
    categoria = st.selectbox("Categoría", op_categoria, index=None,placeholder='Elige')
with col4:
    if categoria:
        ltipo = dop_categoria[categoria]
        tipo = st.multiselect("Tipo", ltipo,placeholder='Elige')
    else:
        tipo = st.multiselect("Tipo", op_tipo,placeholder='Elige')
with col5:
    shinicio = st.selectbox("Hora Inicio",options=opi_hinicio,format_func=lambda o: o[1], index=None, placeholder='Elige')
    if shinicio:
        hinicio = shinicio[0]
    else:
        hinicio = None
with col6:
    shfinal = st.selectbox("Hora Final",options=opi_hfinal,format_func=lambda o: o[1], index=None, placeholder='Elige')
    if shfinal:
        hfinal = shfinal[0]
    else:
        hfinal = None
with col7:
    smes = st.selectbox("Mes",options=opi_mes,format_func=lambda o: o[1], index=None, placeholder='Elige')
    if smes:
        mes = smes[0]
    else:
        mes = None
with col8:
    ano = st.selectbox("Año", op_ano, index=None,placeholder='Elige')
with col9:
    finicio = st.date_input("Desde", value=None)
with col10:
    ffinal = st.date_input("Hasta", value=None)
######
col11, col12, col13, col14, col15 = st.columns(5)
with col11:
    calle = st.text_input("Calle",'',placeholder="Elige")
with col12:
    palabra = st.text_input("Palabra Clave",'',placeholder="Elige")
######

if st.button("Visualizar Mapa"):

    # Verificar si al menos un filtro está seleccionado
    if not any([ingreso, cuadrante, categoria, tipo, hinicio, hfinal, mes, ano, finicio, ffinal, calle, palabra]):
        st.error("Por favor selecciona al menos un filtro")
    else:
        st.session_state.mostrar_mapa = True
        # Procesar datos
        c = []
        try:
            df = pd.read_csv('info.csv',sep=';',engine='python')
            df_filtrado = df.copy()
            df_filtrado['FECHA Y HORA'] = pd.to_datetime(df_filtrado['FECHA Y HORA'])
            if ingreso:
                df_filtrado = df_filtrado[df_filtrado['CANAL DE INGRESO'] == ingreso]
            if cuadrante:
                df_filtrado = df_filtrado[df_filtrado['CUADRANTE'] == cuadrante]
            if categoria:
                df_filtrado = df_filtrado[df_filtrado['CATEGORIA'] == categoria]
            if tipo:
                df_filtrado = df_filtrado[df_filtrado['TIPO DE PROCEDIMIENTO'].isin(tipo)]
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
            if calle:
                df_filtrado = df_filtrado[df_filtrado['CALLE'].str.contains(calle, case=False, na=False) | df_filtrado['CALLE QUE INTERSECTA'].str.contains(calle, case=False, na=False)]
            if palabra:
                df_filtrado = df_filtrado[df_filtrado['INFORME'].str.contains(palabra, case=False, na=False) | df_filtrado['DESCRIPCION DEL PROCEDIMIENTO (DETALLES RELEVANTES)'].str.contains(palabra, case=False, na=False)]

            for index, row in df_filtrado.iterrows():
                if len(str(row['COORDENADAS'])) > 3:
                    cords = str(row['COORDENADAS']).split(',')
                    c.append([cords[0],cords[1],row['FECHA Y HORA'],row['CATEGORIA'],row['TIPO DE PROCEDIMIENTO'],row['CUADRANTE']])
            st.session_state.mapa_data = c
            
        except FileNotFoundError:
            st.error("No se encontró el archivo con la información")

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
    ## Defino los cuadrantes como polígonos y los agrego al mapa ##
    c118 = [[-33.449669,-70.600419], [-33.448523,-70.593123], [-33.44795,-70.571537], [-33.453465,-70.570679], [-33.458979,-70.572309], [-33.454503,-70.580034], [-33.454718,-70.582824], [-33.455541,-70.586472], [-33.454646,-70.59999], [-33.449669,-70.600419]]
    c119 = [[-33.454682,-70.599775], [-33.455613,-70.587158], [-33.454897,-70.583038], [-33.454467,-70.580034], [-33.457904,-70.574799], [-33.458979,-70.572267], [-33.46954,-70.576601], [-33.473406,-70.58454], [-33.474086,-70.588918], [-33.473728,-70.592093], [-33.472261,-70.592051], [-33.470578,-70.589561], [-33.459551,-70.586772], [-33.459014,-70.599904], [-33.454682,-70.599775]]
    c120 = [[-33.459086,-70.59999], [-33.459551,-70.586901], [-33.47065,-70.589561], [-33.472153,-70.592008], [-33.473764,-70.592051], [-33.473478,-70.59587], [-33.473836,-70.601149], [-33.471043,-70.601277], [-33.470793,-70.600591], [-33.459086,-70.59999]]
    c121 = [[-33.444835,-70.601106], [-33.444584,-70.598295], [-33.447753,-70.592823], [-33.439249,-70.587158], [-33.433984,-70.582523], [-33.436312,-70.578361], [-33.438031,-70.573382], [-33.447986,-70.571623], [-33.448559,-70.59351], [-33.449633,-70.600462], [-33.444835,-70.601106]]
    c129 = [[-33.449848,-70.63149], [-33.447941,-70.622263], [-33.453483,-70.620589], [-33.460626,-70.621051], [-33.461118,-70.62193], [-33.460948,-70.624226], [-33.461628,-70.625085], [-33.46118,-70.625739], [-33.455559,-70.627434], [-33.455309,-70.627702], [-33.455291,-70.628282], [-33.455564,-70.629827], [-33.449848,-70.63149]]
    c130 = [[-33.446831,-70.613852], [-33.446429,-70.611298], [-33.445659,-70.608702], [-33.444763,-70.600934], [-33.449741,-70.600548], [-33.454306,-70.600054], [-33.455291,-70.599625], [-33.464564,-70.600247], [-33.464313,-70.601621], [-33.46238,-70.606127], [-33.461771,-70.61501], [-33.461377,-70.614967], [-33.460787,-70.615332], [-33.460845,-70.614726], [-33.453187,-70.613616], [-33.453304,-70.612446], [-33.446831,-70.613852]]
    c131 = [[-33.461682,-70.615], [-33.462263,-70.606202], [-33.462523,-70.604872], [-33.464313,-70.601481], [-33.464582,-70.600312], [-33.470829,-70.600634], [-33.470918,-70.600934], [-33.471079,-70.601192], [-33.473782,-70.601234], [-33.474462,-70.613594], [-33.467643,-70.61398], [-33.465656,-70.614946], [-33.462604,-70.61516], [-33.461682,-70.615]]
    c132 = [[-33.455501,-70.629838], [-33.455201,-70.62847], [-33.455161,-70.627949], [-33.455273,-70.627445], [-33.461091,-70.625814], [-33.461673,-70.625106], [-33.460912,-70.624269], [-33.4611,-70.62193], [-33.460849,-70.621415], [-33.461234,-70.620975], [-33.461655,-70.615042], [-33.462639,-70.615096], [-33.465575,-70.614914], [-33.46766,-70.61398], [-33.474453,-70.613605], [-33.474928,-70.623014], [-33.470077,-70.624323], [-33.468931,-70.625954], [-33.455501,-70.629838]]
    c133 = [[-33.447941,-70.622252], [-33.447243,-70.618776], [-33.448362,-70.618411], [-33.447548,-70.613744], [-33.453277,-70.612457], [-33.453196,-70.613594], [-33.46084,-70.614731], [-33.460778,-70.615289], [-33.461324,-70.61501], [-33.461691,-70.61501], [-33.46127,-70.620965], [-33.460876,-70.621383], [-33.460626,-70.621051], [-33.453483,-70.620632], [-33.447941,-70.622252]]
    lcuad = [c118,c119,c120,c121,c129,c130,c131,c132,c133]
    for element in lcuad:
        folium.Polygon(
            locations=element,
            color="blue",
            fill=False,
            opacity = 0.5,
            fill_color="blue"
            ).add_to(m)
    
    ## Agregar herramienta de dibujo ##
    from folium.plugins import Draw
    Draw(export=False).add_to(m)
    
    ## Renderizar mapa y capturar interacciones ##
    map_key = f"map_{len(st.session_state.mapa_data)}_{st.session_state.cuadrante_filtro}"
    map_data = st_folium(m, width=800, height=600, key=map_key)
    
    st.success(f"✅ Total de puntos: {len(st.session_state.mapa_data)}")
    
    
    ## PROCESAR TODAS LAS FORMAS DIBUJADAS
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