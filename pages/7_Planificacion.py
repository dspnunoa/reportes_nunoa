import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from shapely.geometry import MultiPoint
from scipy import stats
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from sklearn.cluster import DBSCAN
from shapely import contains_xy
from shapely.geometry import MultiPoint
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(page_title="Planificación", layout="wide")
st.logo("./logo.png",size='large',icon_image="./logo.png")
st.title("🧭 Predicción y Planificación de Operativos")
# Validación por seguridad
from auth import check_auth
if not check_auth():
    st.stop()


## Información sobre la data comprendida en la aplicación ##
dfr = pd.read_csv('info.csv', sep=';', engine='python')
dfr['FECHA Y HORA'] = pd.to_datetime(dfr['FECHA Y HORA'])
first_hist = dfr.iloc[0]['FECHA Y HORA']
last_hist = dfr.iloc[-1]['FECHA Y HORA']
st.markdown(f"Información integrada desde **{first_hist}** a **{last_hist}**")

## CALLES PELIGROSAS ##
with st.expander("🚨 Análisis por Calle", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        finicio = st.date_input("Fecha inicial:", value=None)
    with col2:
        ffinal = st.date_input("Fecha final:", value=None)

    if finicio and ffinal:
        df = dfr[(dfr['FECHA Y HORA'].dt.date >= finicio) & (dfr['FECHA Y HORA'].dt.date <= ffinal)].copy()
    else:
        df = dfr.copy()
    # ==================== SECCIÓN 1: RANKING TOP 20 ====================

    st.subheader("🏆 Top 20 Calles con Mayor Actividad")

    # Contar procedimientos por calle
    top_calles = (
        df.loc[df['CALLE'].ne('Nan'), 'CALLE']
        .value_counts()
        .head(20)
        .reset_index(name='Total Procedimientos')
    )

    # Agregar información adicional
    datos_enriquecidos = []
    for idx, row in top_calles.iterrows():
        calle = row['CALLE']
        total = row['Total Procedimientos']
        
        # Obtener tipo más frecuente
        tipo_top = df[df['CALLE'] == calle]['TIPO DE PROCEDIMIENTO'].value_counts().index[0]
        
        # Obtener categoría más frecuente
        cat_top = df[df['CALLE'] == calle]['CATEGORIA'].value_counts().index[0]
        
        # Calcular tendencia (últimas 2 semanas vs antes)
        df['semana'] = df['FECHA Y HORA'].dt.isocalendar().week
        semana_actual = df['semana'].max()
        
        recientes = len(df[(df['CALLE'] == calle) & (df['semana'] >= semana_actual - 1)])
        antiguos = len(df[(df['CALLE'] == calle) & (df['semana'] < semana_actual - 1)])
        
        tendencia = ((recientes - antiguos) / max(antiguos, 1)) * 100 if antiguos > 0 else 0
        
        # Hora pico
        hora_pico = df[df['CALLE'] == calle]['FECHA Y HORA'].dt.hour.value_counts().index[0]
        
        datos_enriquecidos.append({
            'Ranking': idx + 1,
            'Calle': calle,
            'Total': total,
            'Tipo Top': tipo_top,
            'Categoría Top': cat_top,
            'Hora Pico': f"{hora_pico:02d}:00",
            'Tendencia %': f"{tendencia:+.1f}%",
            'Riesgo': '🔴 Crítico' if total > top_calles['Total Procedimientos'].mean() + top_calles['Total Procedimientos'].std() else '🟡 Elevado'
        })

    df_ranking = pd.DataFrame(datos_enriquecidos)

    # Mostrar tabla colorida
    col1, col2 = st.columns([3, 1])

    with col1:
        st.dataframe(
            df_ranking[['Ranking', 'Calle', 'Total', 'Tipo Top', 'Categoría Top', 'Hora Pico', 'Riesgo']],
            width='stretch',
            hide_index=True,
            height=600
        )

    with col2:
        # Métricas de impacto
        st.markdown("### 📊 Impacto General")
        
        total_top20 = df_ranking['Total'].sum()
        porcentaje_impacto = (total_top20 / len(df)) * 100
        
        st.metric(
            "Procedimientos Top 20",
            total_top20,
            f"{porcentaje_impacto:.1f}% del total"
        )
        
        st.metric(
            "Promedio por Calle",
            f"{df_ranking['Total'].mean():.0f}",
            "procedimientos"
        )
        
        st.metric(
            "Calles Críticas",
            len(df_ranking[df_ranking['Riesgo'] == '🔴 Crítico']),
            "requieren intervención"
        )

    # ==================== SECCIÓN 2: ANÁLISIS DETALLADO ====================

    st.markdown("---")
    st.subheader("🔍 Análisis Detallado por Calle")

    # Seleccionar calle
    calle_seleccionada = st.selectbox(
        "Selecciona una calle:",
        df_ranking['Calle'].tolist()
    )

    # Filtrar datos de la calle
    df_calle = df[df['CALLE'] == calle_seleccionada].copy()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Procedimientos", len(df_calle))

    with col2:
        st.metric("Tipos Únicos", df_calle['TIPO DE PROCEDIMIENTO'].nunique())

    with col3:
        st.metric("Categoría Top", df_calle['CATEGORIA'].value_counts().index[0])

    with col4:
        st.metric("Cuadrante", df_calle['CUADRANTE'].value_counts().index[0])

    with col5:
        # Calcular score de riesgo
        score = (len(df_calle) / len(df)) * 100
        st.metric("Score de Riesgo", f"{score:.1f}%")

    # Gráficos de la calle seleccionada
    col1, col2 = st.columns(2)

    with col1:
        # Distribución por tipo
        tipos_calle = df_calle['TIPO DE PROCEDIMIENTO'].value_counts().head(10)
        
        fig_tipos = px.bar(
            x=tipos_calle.index,
            y=tipos_calle.values,
            title=f"Tipos de Procedimientos en {calle_seleccionada}",
            labels={'x': 'Tipo', 'y': 'Cantidad'},
            color=tipos_calle.values,
            color_continuous_scale='Reds'
        )
        
        st.plotly_chart(fig_tipos, width='stretch')

    with col2:
        # Distribución por hora
        horas_calle = df_calle['FECHA Y HORA'].dt.hour.value_counts().sort_index()
        
        fig_horas = px.bar(
            x=horas_calle.index,
            y=horas_calle.values,
            title=f"Distribución Horaria en {calle_seleccionada}",
            labels={'x': 'Hora', 'y': 'Cantidad'},
            color=horas_calle.values,
            color_continuous_scale='Oranges'
        )
        
        fig_horas.update_xaxes(type='category')
        st.plotly_chart(fig_horas, width='stretch')

    # Tendencia temporal
    st.markdown("---")
    st.subheader("📈 Tendencia Temporal")

    df_calle['fecha'] = df_calle['FECHA Y HORA'].dt.date
    tendencia_calle = df_calle.groupby('fecha').size().reset_index(name='cantidad')

    fig_tendencia = px.line(
        tendencia_calle,
        x='fecha',
        y='cantidad',
        title=f"Evolución de Procedimientos en {calle_seleccionada}",
        markers=True,
        labels={'fecha': 'Fecha', 'cantidad': 'Procedimientos'}
    )

    st.plotly_chart(fig_tendencia, width='stretch')

    # ==================== SECCIÓN 4: RECOMENDACIONES ====================

    st.markdown("---")
    st.subheader("💡 Recomendaciones de Intervención")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔴 Calles Críticas (Intervención Inmediata)")
        
        criticas = df_ranking[df_ranking['Riesgo'] == '🔴 Crítico']
        
        for idx, row in criticas.iterrows():
            st.markdown(f"""
            **{row['Ranking']}. {row['Calle']}**
            - Total: {row['Total']} procedimientos
            - Tipo predominante: {row['Tipo Top']}
            - Hora crítica: {row['Hora Pico']}
            - Acción: Aumentar patrullaje en {row['Hora Pico']}
            """)
    with col2:
        st.markdown("### 🟡 Calles con Tendencia Creciente")
        
        # Convertir tendencia a numérica
        df_ranking['Tendencia_Num'] = df_ranking['Tendencia %'].str.rstrip('%').astype(float)
        
        crecientes = df_ranking[df_ranking['Tendencia_Num'] > 0]
        
        if len(crecientes) > 0:
            for idx, row in crecientes.head(5).iterrows():
                st.markdown(f"""
                **{row['Ranking']}. {row['Calle']}**
                - Cambio: {row['Tendencia %']}
                - Total: {row['Total']} procedimientos
                - Tipo: {row['Tipo Top']}
                - Acción: Monitoreo intensivo
                """)
        else:
            st.info("ℹ️ No hay calles con tendencia creciente")



@st.cache_data
def cargar_datos():
    df = pd.read_csv('info.csv', sep=';', engine='python')
    df['FECHA Y HORA'] = pd.to_datetime(df['FECHA Y HORA'], format='%Y-%m-%d %H:%M', errors='coerce')
    df[['LATITUD', 'LONGITUD']] = df['COORDENADAS'].str.split(',', expand=True).apply(lambda x: x.str.strip())
    df['LATITUD'] = pd.to_numeric(df['LATITUD'], errors='coerce')
    df['LONGITUD'] = pd.to_numeric(df['LONGITUD'], errors='coerce')
    df = df.dropna(subset=['FECHA Y HORA', 'LATITUD', 'LONGITUD']).copy()
    df['fecha'] = df['FECHA Y HORA'].dt.normalize()
    return df

df = cargar_datos()

# ==================== PARÁMETROS ====================
VENTANA_DIAS = 14
EPS_METROS = 150          # distancia máxima entre reportes del mismo foco (~2 cuadras)
MIN_REPORTES = 10         # reportes mínimos en la ventana actual para formar un foco
CAMBIO_MIN = 0.20  

# ==================== COORDENADAS EN METROS ====================
LAT_REF = df['LATITUD'].mean()
LON_REF = df['LONGITUD'].mean()
M_POR_GRADO_LAT = 110_574
M_POR_GRADO_LON = 111_320 * np.cos(np.radians(LAT_REF))

def a_metros(datos):
    """Convierte lat/lon a metros (aproximación plana local)."""
    x = datos['LONGITUD'].values * M_POR_GRADO_LON
    y = datos['LATITUD'].values * M_POR_GRADO_LAT
    return np.column_stack([x, y])

def geometria_a_latlon(geom):
    """Convierte el polígono (en metros) a listas de [lat, lon] para folium."""
    partes = [geom] if geom.geom_type == 'Polygon' else list(geom.geoms)
    anillos = []
    for p in partes:
        anillos.append([[y / M_POR_GRADO_LAT, x / M_POR_GRADO_LON] for x, y in p.exterior.coords])
    return anillos

# ==================== FOCOS ====================
def construir_focos(df, fecha_corte):
    fin_act = fecha_corte
    ini_act = fin_act - pd.Timedelta(days=VENTANA_DIAS - 1)
    fin_ant = ini_act - pd.Timedelta(days=1)
    ini_ant = fin_ant - pd.Timedelta(days=VENTANA_DIAS - 1)

    df_act = df[(df['fecha'] >= ini_act) & (df['fecha'] <= fin_act)]
    df_ant = df[(df['fecha'] >= ini_ant) & (df['fecha'] <= fin_ant)]
    df_ambas = df[(df['fecha'] >= ini_ant) & (df['fecha'] <= fin_act)].copy()

    if df_ambas.empty:
        return pd.DataFrame()

    # 1. Agrupar reportes de AMBAS ventanas (aquí está el cambio clave)
    df_ambas['foco'] = DBSCAN(eps=EPS_METROS, min_samples=MIN_REPORTES).fit_predict(a_metros(df_ambas))
    df_ambas = df_ambas[df_ambas['foco'] != -1]

    xy_act = a_metros(df_act)
    xy_ant = a_metros(df_ant)

    def contar(geom, xy):
        return int(contains_xy(geom, xy[:, 0], xy[:, 1]).sum()) if len(xy) else 0

    resultados = []
    for foco_id, grupo in df_ambas.groupby('foco'):
        # 2. Polígono sobre los reportes de ambas ventanas
        geom = MultiPoint(a_metros(grupo)).buffer(EPS_METROS / 2, quad_segs=4).simplify(5)

        # 3. Contar dentro del mismo polígono en cada ventana
        n_act = contar(geom, xy_act)
        n_ant = contar(geom, xy_ant)
        cambio = (n_act - n_ant) / max(n_ant, 1)

        resultados.append({
            'Foco': int(foco_id),
            'Actual': n_act,
            'Anterior': n_ant,
            'Cambio %': round(cambio * 100, 1),
            'Calles principales': ', '.join(grupo['CALLE'].value_counts().head(3).index),
            'Polígono': geometria_a_latlon(geom),
        })

    return pd.DataFrame(resultados)

# ==================== INTERFAZ ====================

fecha_corte = pd.Timestamp(
    st.date_input("Fecha de corte (fin de la ventana actual):", value=df['fecha'].max().date())
)

df_focos = construir_focos(df, fecha_corte)

if df_focos.empty:
    st.info("No hay reportes suficientes en los últimos 28 días para formar focos.")
    st.stop()

def estado(cambio):
    if cambio >= CAMBIO_MIN * 100:
        return 'Aumento'
    if cambio <= -CAMBIO_MIN * 100:
        return 'Mejora'
    return 'Estable'

df_focos['Estado'] = df_focos['Cambio %'].apply(estado)
COLORES = {'Aumento': '#d62728', 'Mejora': '#2ca02c', 'Estable': '#7f7f7f'}

col1, col2, col3 = st.columns(3)
col1.metric("🔴 Focos en aumento", int((df_focos['Estado'] == 'Aumento').sum()))
col2.metric("🟢 Focos en mejora", int((df_focos['Estado'] == 'Mejora').sum()))
col3.metric("⚪ Focos estables", int((df_focos['Estado'] == 'Estable').sum()))

st.caption(f"Rojo: aumento ≥ +{CAMBIO_MIN:.0%} · Verde: mejora ≤ −{CAMBIO_MIN:.0%} · Gris: estable")

m = folium.Map(location=[LAT_REF, LON_REF], zoom_start=14)
c118 = [[-33.449669,-70.600419], [-33.448523,-70.593123], [-33.44795,-70.571537], [-33.453465,-70.570679], [-33.458979,-70.572309], [-33.454503,-70.580034], [-33.454718,-70.582824], [-33.455541,-70.586472], [-33.454646,-70.59999], [-33.449669,-70.600419]]
c119 = [[-33.454682,-70.599775], [-33.455613,-70.587158], [-33.454897,-70.583038], [-33.454467,-70.580034], [-33.457904,-70.574799], [-33.458979,-70.572267], [-33.46954,-70.576601], [-33.473406,-70.58454], [-33.474086,-70.588918], [-33.473728,-70.592093], [-33.472261,-70.592051], [-33.470578,-70.589561], [-33.459551,-70.586772], [-33.459014,-70.599904], [-33.454682,-70.599775]]
c120 = [[-33.459086,-70.59999], [-33.459551,-70.586901], [-33.47065,-70.589561], [-33.472153,-70.592008], [-33.473764,-70.592051], [-33.473478,-70.59587], [-33.473836,-70.601149], [-33.471043,-70.601277], [-33.470793,-70.600591], [-33.459086,-70.59999]]
c121 = [[-33.444835,-70.601106], [-33.444584,-70.598295], [-33.447753,-70.592823], [-33.439249,-70.587158], [-33.433984,-70.582523], [-33.436312,-70.578361], [-33.438031,-70.573382], [-33.447986,-70.571623], [-33.448559,-70.59351], [-33.449633,-70.600462], [-33.444835,-70.601106]]
c129 = [[-33.449848,-70.63149], [-33.447941,-70.622263], [-33.453483,-70.620589], [-33.460626,-70.621051], [-33.461118,-70.62193], [-33.460948,-70.624226], [-33.461628,-70.625085], [-33.46118,-70.625739], [-33.455559,-70.627434], [-33.455309,-70.627702], [-33.455291,-70.628282], [-33.455564,-70.629827], [-33.449848,-70.63149]]
c130 = [[-33.446831,-70.613852], [-33.446429,-70.611298], [-33.445659,-70.608702], [-33.444763,-70.600934], [-33.449741,-70.600548], [-33.454306,-70.600054], [-33.455291,-70.599625], [-33.464564,-70.600247], [-33.464313,-70.601621], [-33.46238,-70.606127], [-33.461771,-70.61501], [-33.461377,-70.614967], [-33.460787,-70.615332], [-33.460845,-70.614726], [-33.453187,-70.613616], [-33.453304,-70.612446], [-33.446831,-70.613852]]
c131 = [[-33.461682,-70.615], [-33.462263,-70.606202], [-33.462523,-70.604872], [-33.464313,-70.601481], [-33.464582,-70.600312], [-33.470829,-70.600634], [-33.470918,-70.600934], [-33.471079,-70.601192], [-33.473782,-70.601234], [-33.474462,-70.613594], [-33.467643,-70.61398], [-33.465656,-70.614946], [-33.462604,-70.61516], [-33.461682,-70.615]]
c132 = [[-33.455501,-70.629838], [-33.455201,-70.62847], [-33.455161,-70.627949], [-33.455273,-70.627445], [-33.461091,-70.625814], [-33.461673,-70.625106], [-33.460912,-70.624269], [-33.4611,-70.62193], [-33.460849,-70.621415], [-33.461234,-70.620975], [-33.461655,-70.615042], [-33.462639,-70.615096], [-33.465575,-70.614914], [-33.46766,-70.61398], [-33.474453,-70.613605], [-33.474928,-70.623014], [-33.470077,-70.624323], [-33.468931,-70.625954], [-33.455501,-70.629838]]
c133 = [[-33.447941,-70.622252], [-33.447243,-70.618776], [-33.448362,-70.618411], [-33.447548,-70.613744], [-33.453277,-70.612457], [-33.453196,-70.613594], [-33.46084,-70.614731], [-33.460778,-70.615289], [-33.461324,-70.61501], [-33.461691,-70.61501], [-33.46127,-70.620965], [-33.460876,-70.621383], [-33.460626,-70.621051], [-33.453483,-70.620632], [-33.447941,-70.622252]]
ldcuad = {"118":c118,"119":c119,"120":c120,"121":c121,"129":c129,"130":c130,"131":c131,"132":c132,"133":c133}
for element in ldcuad:
    folium.Polygon(
        locations=ldcuad[element],
        color="black",
        fill=False,
        opacity = 0.5,
        ).add_to(m)
for _, f in df_focos.iterrows():
    color = COLORES[f['Estado']]
    for anillo in f['Polígono']:
        folium.Polygon(
            locations=anillo,
            color=color, fill=True, fill_opacity=0.3, weight=2,
            tooltip=f"Foco {f['Foco']}: {f['Actual']} reportes ({f['Cambio %']:+.0f}%)",
            popup=(f"<b>Actual:</b> {f['Actual']} | <b>Anterior:</b> {f['Anterior']}<br>"
                   f"<b>Calles:</b> {f['Calles principales']}")
        ).add_to(m)

st.subheader("Tendencias y focos en los últimos 14 días")
st_folium(m, width=1000, height=800)

columnas = ['Foco', 'Actual', 'Anterior', 'Cambio %', 'Calles principales']

st.subheader("🔴 Focos en aumento")
aumentos = df_focos[df_focos['Estado'] == 'Aumento'].sort_values('Cambio %', ascending=False)
if aumentos.empty:
    st.info("No hay focos en aumento.")
else:
    st.dataframe(aumentos[columnas], width='stretch', hide_index=True)

st.subheader("🟢 Focos en mejora")
mejoras = df_focos[df_focos['Estado'] == 'Mejora'].sort_values('Cambio %')
if mejoras.empty:
    st.info("No hay focos en mejora.")
else:
    st.dataframe(mejoras[columnas], width='stretch', hide_index=True)