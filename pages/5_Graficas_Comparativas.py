from datetime import datetime
import pandas as pd
import plotly.express as px
import streamlit as st

## Configuración inicial aplicación ##
st.set_page_config(page_title="Comparador Períodos", layout="wide")
st.logo("./logo.png",size='large',icon_image="./logo.png")
st.title("⚖️ Comparador Períodos Reportes Central Ñuñoa 2026")

## Validación por seguridad ##
from auth import check_auth
if not check_auth():
    st.stop()

## Título y botones en una fila ##
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("Inicio", key="nav_home", width='stretch'):
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

with col5:
    if st.button("Exportar Reportes", key="nav_report", width='stretch'):
        st.switch_page("pages/4_Exportar_Reportes.py")

with col6:
    if st.button("Comparador Períodos", key='nav_comp', width='stretch', type="primary"):
        st.switch_page("pages/5_Graficas_Comparativas.py")
st.markdown("---")
## Información sobre la data comprendida en la aplicación ##
dfr = pd.read_csv('info.csv', sep=';', engine='python')
dfr['FECHA Y HORA'] = pd.to_datetime(dfr['FECHA Y HORA'])
first_hist = dfr.iloc[0]['FECHA Y HORA']
last_hist = dfr.iloc[-1]['FECHA Y HORA']
st.markdown(f"Información integrada desde **{first_hist}** a **{last_hist}**")


## Cargo el excel ##
dfr = pd.read_csv('info.csv', sep=';', engine='python')
dfr['FECHA Y HORA'] = pd.to_datetime(dfr['FECHA Y HORA'])
df = dfr.copy()

## COMPARADOR DE PERIODOS ##
st.subheader(f"⇄ Comparador de Períodos")
c1,c2,c3,c4,c5 = st.columns(5)
with c1:
    tipo_periodo = st.selectbox("Periodo:",["Semana","Mes"])
if tipo_periodo == "Semana":
    with c2:
        periodo1 = st.selectbox("Semana 1:", range(1, 54), key="sem1")
    with c3:
        periodo2 = st.selectbox("Semana 2:", range(1, 54), key="sem2", index=1)
else:
    with c2:
        periodo1 = st.selectbox("Mes 1:", range(1, 13), key="mes1")
    with c3:
        periodo2 = st.selectbox("Mes 2:", range(1, 13), key="mes2", index=1)
with c4:
    ano1 = st.selectbox("Año 1:",sorted(df['FECHA Y HORA'].dt.year.unique()), key="ano1")
with c5:
    ano2 = st.selectbox("Año 2:",sorted(df['FECHA Y HORA'].dt.year.unique()), key="ano2")

if tipo_periodo == "Semana":
    df['periodo'] = df['FECHA Y HORA'].dt.isocalendar().week
    label1 = f"Semana {periodo1} - {ano1}"
    label2 = f"Semana {periodo2} - {ano2}"
else:
    df['periodo'] = df['FECHA Y HORA'].dt.month
    label1 = f"Mes {periodo1} - {ano1}"
    label2 = f"Mes {periodo2} - {ano2}"
df['ano'] = df['FECHA Y HORA'].dt.year

df_periodo1 = df[(df['periodo']==periodo1)&(df['ano']==ano1)]
df_periodo2 = df[(df['periodo']==periodo2)&(df['ano']==ano2)]

m1,m2,m3,m4,m5,m6 = st.columns(6)
def calcular_dif(x,y):
    if y==0:
        return 0
    return ((x-y)/y)*100
t1 = len(df_periodo1)
t2 = len(df_periodo2)
diff = calcular_dif(t1,t2)

with m1:
    st.metric(label1,t1,delta=f"{diff:+.1f}&")

with m2:
    st.metric(label2,t2)
# 2. Cuadrante top
cuad1 = df_periodo1['CUADRANTE'].value_counts().index[0] if len(df_periodo1) > 0 else "N/A"
cuad2 = df_periodo2['CUADRANTE'].value_counts().index[0] if len(df_periodo2) > 0 else "N/A"
count1 = df_periodo1['CUADRANTE'].value_counts().iloc[0] if len(df_periodo1) > 0 else 0
count2 = df_periodo2['CUADRANTE'].value_counts().iloc[0] if len(df_periodo2) > 0 else 0
diff_cuad = calcular_dif(count1, count2)

with m3:
    st.metric(
        f"Cuadrante Top {ano1}",
        cuad1,
        delta=f"{count1} reportes"
    )

with m4:
    st.metric(
        f"Cuadrante Top {ano2}",
        cuad2,
        delta=f"{diff_cuad:+.1f}%"
    )

# 3. Tipo de procedimiento top
tipo1 = df_periodo1['TIPO DE PROCEDIMIENTO'].value_counts().index[0] if len(df_periodo1) > 0 else "N/A"
tipo2 = df_periodo2['TIPO DE PROCEDIMIENTO'].value_counts().index[0] if len(df_periodo2) > 0 else "N/A"
count_tipo1 = df_periodo1['TIPO DE PROCEDIMIENTO'].value_counts().iloc[0] if len(df_periodo1) > 0 else 0
count_tipo2 = df_periodo2['TIPO DE PROCEDIMIENTO'].value_counts().iloc[0] if len(df_periodo2) > 0 else 0
diff_tipo = calcular_dif(count_tipo1, count_tipo2)

with m5:
    st.metric(
        f"Tipo Top {ano1}",
        tipo1,
        delta=f"{count_tipo1} reportes"
    )

with m6:
    st.metric(
        f"Tipo Top {ano2}",
        tipo2,
        delta=f"{diff_tipo:+.1f}%"
    )

# GRÁFICOS COMPARATIVOS
st.markdown("---")

# Preparar datos para gráficos
datos_cuadrante1 = df_periodo1['CUADRANTE'].value_counts().reset_index(name='cantidad').head(10)
datos_cuadrante1['Período'] = label1

datos_cuadrante2 = df_periodo2['CUADRANTE'].value_counts().reset_index(name='cantidad').head(10)
datos_cuadrante2['Período'] = label2

datos_cuadrante = pd.concat([datos_cuadrante1, datos_cuadrante2], ignore_index=True)

# Gráfico 1: Cuadrantes
fig_cuadrantes = px.bar(
    datos_cuadrante,
    x='CUADRANTE',
    y='cantidad',
    color='Período',
    barmode='group',
    title='Top 10 Cuadrantes',
    labels={'cantidad': 'Total de Procedimientos'}
)

st.plotly_chart(fig_cuadrantes, width='stretch')

# Gráfico 2: Tipos
datos_tipo1 = df_periodo1['TIPO DE PROCEDIMIENTO'].value_counts().reset_index(name='cantidad').head(10)
datos_tipo1['Período'] = label1

datos_tipo2 = df_periodo2['TIPO DE PROCEDIMIENTO'].value_counts().reset_index(name='cantidad').head(10)
datos_tipo2['Período'] = label2

datos_tipo = pd.concat([datos_tipo1, datos_tipo2], ignore_index=True)

fig_tipos = px.bar(
    datos_tipo,
    x='TIPO DE PROCEDIMIENTO',
    y='cantidad',
    color='Período',
    barmode='group',
    title='Top 10 Tipos de Procedimiento',
    labels={'cantidad': 'Total'}
)

st.plotly_chart(fig_tipos, width='stretch')

# Tabla comparativa
st.markdown("---")
st.subheader("📋 Tabla Comparativa Detallada")

tabla_comp = pd.DataFrame({
    'Métrica': ['Total Procedimientos', 'Cuadrantes Únicos', 'Tipos Únicos', 'Canales Únicos', 'Categorías Únicas'],
    label1: [
        len(df_periodo1),
        df_periodo1['CUADRANTE'].nunique(),
        df_periodo1['TIPO DE PROCEDIMIENTO'].nunique(),
        df_periodo1['CANAL DE INGRESO'].nunique(),
        df_periodo1['CATEGORIA'].nunique()
    ],
    label2: [
        len(df_periodo2),
        df_periodo2['CUADRANTE'].nunique(),
        df_periodo2['TIPO DE PROCEDIMIENTO'].nunique(),
        df_periodo2['CANAL DE INGRESO'].nunique(),
        df_periodo2['CATEGORIA'].nunique()
    ]
})

tabla_comp['Diferencia %'] = tabla_comp.apply(
    lambda row: f"{calcular_dif(row[label1], row[label2]):+.1f}%",
    axis=1
)

st.dataframe(tabla_comp, width='stretch', hide_index=True)
st.markdown("---")
############################

## Defino la lista de categirias y tipos de procedimientos ##
st.subheader(f"📉 Gráficas Comparativas")
dop_categoria ={'Seguridad':['Servicio DRONE','Apoyo a Carabineros','Actividad sospechosa','Agresión','Alarma activada','Amenazas','Artefacto explosivo o paquete sospechoso','Daños propiedad privada','Daños propiedad pública','Delito sexual','Detención ciudadana','Detenidos','Disparos','Disturbios','Fuegos artificiales','Homicidio','Homicidio Frustrado','Hurto','Maltrato animal','Marchas/manifestaciones','Persona extraviada / desorientada','Posible sospechoso al interior','Riña','Robo con intimidación','Robo con violencia','Robo de especies de o desde vehículo','Robo de vehículo en BNUP','Robo en BNUP','Robo en lugar habitado','Robo en lugar no habitado','Robo frustrado','Robo por sorpresa','Toma establecimiento educacional','Trafico Drogas','Vehículo con encargo','Vehiculo sospechoso','Incumplimiento medida cautelar','VIF','Vulneración derechos adultos mayores','Vulneración NNA','Otros','Motochorros '],
                 'Planes Operativos':['7X3 delitos violentos','Control de Transito','Operativo Conjunto a otras Municipalidades','Operativo Conjunto Carabineros','Operativo conjunto Delegación Presidencial','Operativo conjunto Dirección de Inspección','Operativo MTT','Operativo otras direcciones Municilapales','Operativo Seremi Salud','Operativos Conjunto PDI','P.V.P','Patrulla Mixta','Patrullaje focalizado Carabineros','Patrullaje focalizado Preventivo','Patrullaje preventivo general','Punto fijo','Ruta calle','Servicio especial Colegios','Servicio Estadio','Servicio FEI','Servicio turístico Plaza Ñuñoa-Barrio Italia','Vigilancia especial','Otros'],
                 'Emergencia/Espacio Públicos':['Apoyo a Bomberos','Apoyo a SAMU','Accidente de tránsito (choque/colisión/atropello)','Acera en mal estado','Alcantarilla colapsada','Anegamiento de calle y paso bajo nivel','Anegamiento domicilios','Suicidio/Intento','Cables a baja altura / Cables cortados','Caida de arbol','Circuito y luminarias dañadas','Corte energía eléctrica','Corte suministro de agua potable','Desganche arbolado','Emanación de gas/ Derrame o Materiales peligrosos','Emergencia de salud','Filtración agua potable','Incendio o amago','Mascota atrapada/perdida','Pavimento en mal estado','Posible Fallecido/Emergencia de Salud','Postes dañados','Semáforo defectuoso','Señalética o elemento caida','Tapa de servicios','Otra contingencia BNUP','Otros'],
                 'Fiscalización':['Realizacion de Graffitis / Pintar sin autorización','Comercio ambulante Ilegal','Fiscalización alcoholes','Fiscalización aparcadores ilegales','Fiscalización de tránsito','Vehiculo MAL Estacionado','Vehículo sospechoso','Fiscalización ingesta de alcohol en vía pública','Fiscalizacion Retiro de circulación de vehiculo motorizado','Fiscalizacion Ruidos Molestos','Fiscalizaciones (BNUP, comercio, etc)','Trabajos fuera de horario','Vehículo abandonado','Otros'],
                 'Incivilidades':['Botar chicle, colillas o desechos en la vía pública','Carpa o Ruco en BNUP','Consumo de alcohol en vía pública','Consumo de drogas','Ebriedad','Microbasural','Persona situación de calle','Otros'],
                 'Otros':['Novedades Central','Labores administrativas','Traslado de documentos o funcionarios/limpieza de móvil','Otros']}
op_categoria = list(dop_categoria.keys())
op_tipo =['Servicio DRONE','Apoyo a Carabineros','Actividad sospechosa','Agresión','Alarma activada','Amenazas','Artefacto explosivo o paquete sospechoso','Daños propiedad privada','Daños propiedad pública','Delito sexual','Detención ciudadana','Detenidos','Disparos','Disturbios','Fuegos artificiales','Homicidio','Homicidio Frustrado','Hurto','Maltrato animal','Marchas/manifestaciones','Persona extraviada / desorientada','Posible sospechoso al interior','Riña','Robo con intimidación','Robo con violencia','Robo de especies de o desde vehículo','Robo de vehículo en BNUP','Robo en BNUP','Robo en lugar habitado','Robo en lugar no habitado','Robo frustrado','Robo por sorpresa','Toma establecimiento educacional','Trafico Drogas','Vehículo con encargo','Vehiculo sospechoso','Incumplimiento medida cautelar','VIF','Vulneración derechos adultos mayores','Vulneración NNA','Otros','Motochorros ','7X3 delitos violentos','Control de Transito','Operativo Conjunto a otras Municipalidades','Operativo Conjunto Carabineros','Operativo conjunto Delegación Presidencial','Operativo conjunto Dirección de Inspección','Operativo MTT','Operativo otras direcciones Municilapales','Operativo Seremi Salud','Operativos Conjunto PDI','P.V.P','Patrulla Mixta','Patrullaje focalizado Carabineros','Patrullaje focalizado Preventivo','Patrullaje preventivo general','Punto fijo','Ruta calle','Servicio especial Colegios','Servicio Estadio','Servicio FEI','Servicio turístico Plaza Ñuñoa-Barrio Italia','Vigilancia especial','Otros','Apoyo a Bomberos','Apoyo a SAMU','Accidente de tránsito (choque/colisión/atropello)','Acera en mal estado','Alcantarilla colapsada','Anegamiento de calle y paso bajo nivel','Anegamiento domicilios','Suicidio/Intento','Cables a baja altura / Cables cortados','Caida de arbol','Circuito y luminarias dañadas','Corte energía eléctrica','Corte suministro de agua potable','Desganche arbolado','Emanación de gas/ Derrame o Materiales peligrosos','Emergencia de salud','Filtración agua potable','Incendio o amago','Mascota atrapada/perdida','Pavimento en mal estado','Posible Fallecido/Emergencia de Salud','Postes dañados','Semáforo defectuoso','Señalética o elemento caida','Tapa de servicios','Otra contingencia BNUP','Otros','Realizacion de Graffitis / Pintar sin autorización','Comercio ambulante Ilegal','Fiscalización alcoholes','Fiscalización aparcadores ilegales','Fiscalización de tránsito','Vehiculo MAL Estacionado','Vehículo sospechoso','Fiscalización ingesta de alcohol en vía pública','Fiscalizacion Retiro de circulación de vehiculo motorizado','Fiscalizacion Ruidos Molestos','Fiscalizaciones (BNUP, comercio, etc)','Trabajos fuera de horario','Vehículo abandonado','Otros','Botar chicle, colillas o desechos en la vía pública','Carpa o Ruco en BNUP','Consumo de alcohol en vía pública','Consumo de drogas','Ebriedad','Microbasural','Persona situación de calle','Otros','Novedades Central','Labores administrativas','Traslado de documentos o funcionarios/limpieza de móvil','Otros','Patrullaje preventivo', 'Focalizado municipal', 'Fiscalización conjunta (Carabineros, PDI)', 'Operativos conjuntos: colaboración con Carabineros, PDI', 'Fiscalización', 'Ruidos Molestos', 'Retiro de enseres de la via publica', 'Seguridad (prevención)', 'Seguridad']

## Agrego la opción de elegir un período ##
col1, col2 = st.columns([1,4])
with col1:
    categoria = st.selectbox("Categoría", op_categoria, index=None,placeholder='Elige')
with col2:
    if categoria:
        ltipo = dop_categoria[categoria]
        tipos = st.multiselect("Tipo", ltipo,placeholder='Elige')
    else:
        tipos = st.multiselect("Tipo", op_tipo,placeholder='Elige')
anos = [2025,2026]

col3, col4 = st.columns(2)
with col3:
    finicio = st.date_input("Fecha inicial:", value=None)
with col4:
    ffinal = st.date_input("Fecha final:", value=None)
if finicio and ffinal:
    fcinicio = finicio.strftime("%m-%d")
    fcfinal = ffinal.strftime("%m-%d")

if st.button("Ver Gráfica Comparativa"):
    if not any([tipos]):
        st.error("Por favor selecciona al menos un tipo de procedimiento.")
    if not any([finicio, ffinal]):
        st.error("Por favor ingrese un rango de fechas.")
    if finicio and ffinal and (finicio > ffinal):
        st.error("Por favor ingrese un rango de fechas válido.")
    else:
        lista = []
        for ano in anos:
            listanual = []
            for tipo in tipos:
                rinicio = str(ano)+'-'+str(fcinicio)
                rfinal = str(ano)+'-'+str(fcfinal)
                rinicio = datetime.strptime(rinicio, "%Y-%m-%d")
                rfinal = datetime.strptime(rfinal, "%Y-%m-%d")
                rinicio = rinicio.date()
                rfinal = rfinal.date()
                if categoria:
                    count = len(df[(df['CATEGORIA'] == categoria) & (df['TIPO DE PROCEDIMIENTO']== tipo) & (df['FECHA Y HORA'].dt.year == ano) & (df['FECHA Y HORA'].dt.date >= rinicio) & (df['FECHA Y HORA'].dt.date <= rfinal)])            
                else:
                    count = len(df[(df['TIPO DE PROCEDIMIENTO']== tipo) & (df['FECHA Y HORA'].dt.year == ano) & (df['FECHA Y HORA'].dt.date >= rinicio) & (df['FECHA Y HORA'].dt.date <= rfinal)])
                listanual.append(count)
            lista.append(listanual)
        ## Genero la información ##
        lform = [tipos,lista[0],lista[1]]
        df2 = pd.DataFrame({
            "Tipo de Procedimiento":lform[0],
            "2025":lform[1],
            "2026":lform[2]
        })

        df_melt = df2.melt(id_vars="Tipo de Procedimiento", 
                        var_name="Año", 
                        value_name="Valor")

        fig = px.bar(df_melt, 
                    x="Tipo de Procedimiento", 
                    y="Valor", 
                    color="Año",
                    barmode="group")
        
        ## Gráfico de barra doble ##
        st.plotly_chart(fig,width='stretch')

        ## Tabla que muestra lo mismo que el gráfico de barra ##
        st.dataframe(df2, width='stretch', hide_index=True)

        ## Recorro todos los procedimientos ##
        df = dfr.copy()
        filt = (df['FECHA Y HORA'].dt.strftime('%m-%d') >= fcinicio) & (df['FECHA Y HORA'].dt.strftime('%m-%d') <= fcfinal)
        dff = df[filt]
        df = dff
        df["AÑO"] = df["FECHA Y HORA"].dt.year
        df["DIA DEL ANO"] = df["FECHA Y HORA"].dt.dayofyear
        df["SEMANA"] = df["FECHA Y HORA"].dt.isocalendar().week
        for tipo in tipos:
            st.subheader(f"{tipo}")
            df_tipo = df[df["TIPO DE PROCEDIMIENTO"] == tipo]
            ## Este funciona para las semanas ##
            df_grouped = (
                df_tipo.groupby(["AÑO", "SEMANA"])
                    .size()
                    .unstack(fill_value=0)
                    .stack()
                    .reset_index()
                    .rename(columns={0: "CANTIDAD"})
            )
            fig = px.line(
                df_grouped,
                x="SEMANA",
                y="CANTIDAD",
                color="AÑO"
            )
            ## Este funciona para los días (comentar/descomentar uno u otro según corresponda) ## 
            # df_grouped = (
            #     df_tipo.groupby(["AÑO", "DIA DEL ANO"])
            #         .size()
            #         .unstack(fill_value=0)
            #         .stack()
            #         .reset_index()
            #         .rename(columns={0: "CANTIDAD"})
            # )
            # fig = px.line(
            #     df_grouped,
            #     x="DIA DEL ANO",
            #     y="CANTIDAD",
            #     color="AÑO"
            # )
            st.plotly_chart(fig, width='stretch')