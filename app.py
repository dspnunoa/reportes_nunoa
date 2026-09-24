import pandas as pd
import streamlit as st

## Configuración inicial aplicación ##
## El logo es el archivo logo.png ubicado en la misma carpeta que este archivo ##
## En caso de querer cambiar el logo, ubicar en esta carpeta un archivo png con el mismo nombre y borrar el antiguo ##
st.set_page_config(
    page_title="Inicio",
    page_icon="./logo.png",
    initial_sidebar_state="collapsed",
    layout="wide"
)
st.logo("./logo.png",size='large',icon_image="./logo.png")
st.title("ℹ️ Reportes Procedimientos Central Ñuñoa 2026")

## Validación por seguridad ##
from auth import check_auth
if not check_auth():
    st.stop()

## Título y botones en una fila ##
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("Inicio", key="nav_home", width='stretch', type="primary"):
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
    if st.button("Comparador Períodos", key='nav_comp', width='stretch'):
        st.switch_page("pages/5_Graficas_Comparativas.py")

## Descripción general de la aplicación ##
st.markdown("---")
## Información sobre la data comprendida en la aplicación ##
dfr = pd.read_csv('info.csv', sep=';', engine='python')
dfr['FECHA Y HORA'] = pd.to_datetime(dfr['FECHA Y HORA'])
first_hist = dfr.iloc[0]['FECHA Y HORA']
last_hist = dfr.iloc[-1]['FECHA Y HORA']
st.markdown(f"Información integrada desde **{first_hist}** a **{last_hist}**")
## CALLES PELIGROSAS ##
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
with st.expander("🚨 Análisis de Calles Peligrosas", expanded=False):
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
#######################

st.header("Bienvenido a la plataforma de análisis de reportes ingresados por Central de Dirección de Seguridad Pública. En esta aplicación podrás:")
st.write("""
- 🗺️ Visualizar reportes georeferenciados en un mapa de calor
- 📈 Analizar datos a través de gráficas y métricas
- 🗃️ Búsquedas personalizadas por filtros en tabla de datos
- 📝 Generar informes estandarizados y automatizados
- ⚖️ Comparar tipos de procedimientos por período de tiempo

Selecciona una opción en el menú para comenzar.
""")

st.markdown("---")
st.header("🗺️ Mapa Interactivo")
st.write("""
        Visualización georeferenciada de los reportes. Seleccione al menos uno de los doce filtros disponibles (Vía de Ingreso, Cuadrante, Categoría, Tipo, Hora Inicio, Hora Final, Mes, Año, Desde, Hasta, Calle, Palabra Clave) y haga click en "Visualizar Mapa" para que este se despliegue (El filtro Calle buscará coincidencias en los campos "CALLE" y "CALLE QUE INTERSECTA", mientras que el filtro Palabra Clave en los campos "DESCRIPCION DEL PROCEDIMIENTO" e "INFORME"). Se mostrará el número de resultados encontrados junto a los puntos ubicados en el mapa, además de un mapa de calor asociado. El mapa muestra la delimitación de cada cuadrante junto a una leyenda incluyendo el número de este.
         
        Es posible además elegir cualquiera de las figuras en la parte izquierda del mapa (círculo, cuadrado o polígono), para poder seleccionar una parte específica de interés. De ser así el caso, se desplegarán dos tablas: la primera mostrando un desglose de todos los puntos dentro de la figura, y la segunda un resumen por el tipo de procedimiento. Cada una de estas tablas se puede exportar de la siguiente manera: pasando el mouse por encima de la tabla, se despliega un menú en la parte superior derecha, ahí hay que hacer click en el botón 'Download as CSV'.

        Para una mejor disposición del archivo descargado hacer lo siguiente: con el archivo .csv abierto, hacer click en la columna A y asegurar que se hayan seleccionado todas las filas de esa columna. Luego ir a la parte 'Datos' del menú superior y hacer click en 'Texto en columnas'. En el paso 1 seleccionar 'Delimitados', en el paso 2 seleccionar 'Coma' y en el paso 3 hacer click en 'Finalizar'.
""")

st.markdown("---")
st.header("📈 Dashboard")
st.write("""
        Gráficas, métricas e indicadores relevantes de los reportes. Por defecto se muestra la información de todo el rango de fechas disponibles en la base de datos pero incluye la opción de seleccionar un rango personalizado. Incluye una sección de métricas principales, de análisis general, de análisis temporal, un desglose del total de procedimientos y un análisis detallado 

        Todos los gráficos son exportables. Para hacerlo, debe hacer click en el ícono de cámara 'Download plot as a PNG'. Los gráficos son interactivos y tienen funcionalidades útiles para un análisis exhaustivo.
""")

st.markdown("---")
st.header("🗃️ Tablas")
st.write("""
        Búsqueda detallada de reportes. Seleccione al menos uno de los doce filtros disponibles (Vía de Ingreso, Cuadrante, Categoría, Tipo, Hora Inicio, Hora Final, Mes, Año, Desde, Hasta, Calle, Palabra Clave) y la tabla y el número total de registros cambiará automáticamente. Al igual que en la sección del Mapa Interactivo, la tabla filtrada es exportable.
""")

st.markdown("---")
st.header("📝 Generación de Informe")
st.write("""
        Generación automática de informes personalizados. Seleccione un rango de fechas, en caso contrario se elegirá el total del archivo. Seleccione variables del reporte (Canal de Ingreso, Cuadrante, Categoría, Tipo de Procedimiento, Palabra Clave, Calle). Seleccione variables de diseño (Título, Autor, Formato Registros).
         
        Todas las variables son opcionales. Se incluye un título y autor pre-definido por defecto (Reporte de Análisis de Procedimientos y Dirección de Seguridad Pública de Ñuñoa, respectivamente). 
""")

st.markdown("---")
st.header("⚖️ Comparador Períodos")
st.write("""
        Gráfica comparativa del comportamiento de los tipos de procedimientos. Seleccione una categoría o un conjunto de tipos de procedimientos y un rango de fechas (verificar que este rango de fechas tenga información en más de un año diferente, para que lo que se muestre tenga sentido). Se desplegará un gráfico de barras con todos los procedimientos seleccionados por año, una tabla con lo anterior, y además por cada tipo de procedimiento un gráfico de barras con el comportamiento semanal en cada año disponible.
""")