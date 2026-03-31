from datetime import datetime
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📈 Dashboard Reportes Central Ñuñoa 2026")
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
## Cargo el excel ##
dfr = pd.read_csv('info.csv', sep=';', engine='python')
dfr['FECHA Y HORA'] = pd.to_datetime(dfr['FECHA Y HORA'])
## Agrego la opción de elegir un período ##
col1, col2 = st.columns(2)
with col1:
    finicio = st.date_input("Fecha inicial:", value=None)
with col2:
    ffinal = st.date_input("Fecha final:", value=None)
###########################################
if finicio and ffinal:
    df = dfr[(dfr['FECHA Y HORA'].dt.date >= finicio) & (dfr['FECHA Y HORA'].dt.date <= ffinal)].copy()
else:
    df = dfr.copy()

st.subheader("ℹ️ Métricas Principales")
met1, met2, met3, met4 = st.columns(4)
with met1:
    st.metric("Número de Reportes",f"{df.shape[0]}")
with met2:
    cuad_metric = df['CUADRANTE'].value_counts().index[0]
    st.metric("Cuadrante con más Reportes",cuad_metric,delta=f"{df['CUADRANTE'].value_counts().iloc[0]}")
with met3:
    tipo_metric = df['TIPO DE PROCEDIMIENTO'].value_counts().index[0]
    st.metric("Procedimiento más común",tipo_metric,delta=f"{df['TIPO DE PROCEDIMIENTO'].value_counts().iloc[0]}",width="content")
with met4:
    hora_metric = df['FECHA Y HORA'].dt.hour.value_counts().index[0]
    st.metric("Horario Punta",f"{int(hora_metric):02d}:00-{int(hora_metric+1):02d}:00",delta=df['FECHA Y HORA'].dt.hour.value_counts().iloc[0],width="content")

met5, met6, met7, met8 = st.columns(4)
with met5:
    fecha_metric = df['FECHA Y HORA'].dt.date.value_counts().index[0]
    st.metric("Día con más reportes",f"{fecha_metric}",delta=df['FECHA Y HORA'].dt.date.value_counts().iloc[0])
with met6:
    st.metric("Procedimientos",df['TIPO DE PROCEDIMIENTO'].nunique())
with met7:
    dias_cubiertos = ((df['FECHA Y HORA'].max() - df['FECHA Y HORA'].min()).days)+1
    st.metric("Días Cubiertos",dias_cubiertos)
with met8:
    promedio_diario = round(len(df) / max(dias_cubiertos, 1), 1)
    st.metric("Promedio Diario",f"{promedio_diario} reportes/día")

met9, met10, met11, met12 = st.columns(4)
with met9:
    calle_metric = df['CALLE'].value_counts().index[0]
    st.metric("Calle con más Reportes",calle_metric,delta=f"{df['CALLE'].value_counts().iloc[0]}")
with met10:
    if df['LUGAR PÚBLICO /  PRIVADO'].isnull().all():
        st.metric("Tipo de lugar más común",'NO APLICA')
    else:
        lugar_metric = df['LUGAR PÚBLICO /  PRIVADO'].value_counts().index[0]
        st.metric("Tipo de lugar más común",lugar_metric,delta=f"{df['LUGAR PÚBLICO /  PRIVADO'].value_counts().iloc[0]}")
with met11:
    dia_metric = df['FECHA Y HORA'].dt.day_name().value_counts().index[0]
    dict_dias = {'Monday':'Lunes','Tuesday':'Martes','Wednesday':'Miércoles','Thursday':'Jueves','Friday':'Viernes','Saturday':'Sábado','Sunday':'Domingo'}
    dies = dict_dias[dia_metric]
    st.metric("Día de la semana con más Reportes",dies,delta=f"{df['FECHA Y HORA'].dt.day_name().value_counts().iloc[0]}")
with met12:
    st.metric("Métrica por añadir",35,delta=-10)
## COM FUNCIONES ##
def get_rango_horario(hora):
    """Convierte hora (0-23) en rango de 4 horas"""
    rango = int((hora // 4) * 4)
    return f"{rango:02d}:00 - {rango+3:02d}:59"
##
def pie_tipo(cat):
    df_filtrado = df[df['CATEGORIA'] == cat]
    df_pie = df_filtrado.groupby('TIPO DE PROCEDIMIENTO').size().reset_index(name='cantidad')
    fig_pie = px.pie(
        df_pie,
        names='TIPO DE PROCEDIMIENTO',
        values='cantidad',
        title='Distribución por categoría: '+cat
    )
    fig_pie.update_traces(
        textposition='inside',
        textinfo='label',  # Nombre + Porcentaje + Valor
        hovertemplate='<b>%{label}</b><br>Cantidad: %{value}<br>Porcentaje: %{percent}<extra></extra>'
    )
    st.plotly_chart(fig_pie, width='stretch')
##
def pie(filtro):
    df_pie = df.groupby(filtro).size().reset_index(name='cantidad')
    titulo = filtro.title()
    fig_pie = px.pie(
        df_pie,
        names=filtro,
        values='cantidad',
        title='Reportes por '+titulo
    )
    fig_pie.update_traces(
        textposition='inside',
        textinfo='label',  # Nombre + Porcentaje + Valor
        hovertemplate='<b>%{label}</b><br>Cantidad: %{value}<br>Porcentaje: %{percent}<extra></extra>'
    )
    fig_pie.update_layout(
        legend=dict(
            orientation="h",  # Horizontal
            yanchor="bottom",
            y=-0.15,  # Debajo del gráfico
            xanchor="center",
            x=0.5
        )
    )
    st.plotly_chart(fig_pie, width='stretch')
##
def barra(filtro):
    if filtro == 'Día de la Semana':
        counts = df["FECHA Y HORA"].dt.weekday.value_counts()
    elif filtro == 'Hora':
        counts = df["FECHA Y HORA"].dt.hour.value_counts()
    elif filtro == 'CATEGORIA':
        counts = df["CATEGORIA"].value_counts()
        filtro = filtro.title()
    fig_barras = px.bar(
        counts,
        title='Reportes por '+filtro
    )
    fig_barras.update_layout(
        xaxis_title=filtro,
        yaxis_title='Reportes'
    )
    st.plotly_chart(fig_barras,width='stretch')
##
def matriz(filtro):
    dfm = df.copy()
    titulo = filtro.upper()
    dfm['fecha_completa'] = pd.to_datetime(dfm['FECHA Y HORA'])
    dfm['hora'] = dfm['fecha_completa'].dt.hour
    dfm = dfm.dropna(subset=['hora'])
    dfm['hora'] = dfm['hora'].astype(int)
    dfm['rango_horario'] = dfm['hora'].apply(get_rango_horario)
    matriz = pd.crosstab(dfm['rango_horario'], dfm[titulo])
    rangos_orden = [
        "00:00 - 03:59",
        "04:00 - 07:59",
        "08:00 - 11:59",
        "12:00 - 15:59",
        "16:00 - 19:59",
        "20:00 - 23:59"
    ]
    rangos_existentes = [r for r in rangos_orden if r in matriz.index]
    matriz = matriz.loc[rangos_existentes]
    fig_heatmap = px.imshow(
        matriz,
        labels=dict(x=filtro, y="Rango Horario", color="Reportes"),
        title="Matriz de Calor: Registros por "+filtro+" y Rango Horario",
        color_continuous_scale='RdYlGn_r',
        aspect='auto'
    )
    fig_heatmap.update_traces(text=matriz.values, texttemplate='%{text}')
    fig_heatmap.update_layout(
        height=400,
        xaxis_title=filtro,
        yaxis_title='Rango Horario'
    )
    st.plotly_chart(fig_heatmap, width='stretch')
## FIN FUNCIONES ##
st.markdown("### 📊 Análisis General")
## GRÁFICOS I, II ##
pie('CUADRANTE')
pie('CANAL DE INGRESO')

## GRÁFICO III, IV, V ##
barra('Día de la Semana')
barra('Hora')
barra('CATEGORIA')

## Gráfico VI ##
df['fecha_completa'] = pd.to_datetime(df['FECHA Y HORA'])
df['hora_numerica'] = df['fecha_completa'].dt.hour
fig = px.box(
    df,
    x='CATEGORIA',
    y='hora_numerica',
    title='Distribución de horas por Categoría'
)
st.plotly_chart(fig, width='stretch')

## Gráfico VII ##
fig = px.scatter(
    df.groupby(['CUADRANTE', 'CATEGORIA']).size().reset_index(name='cantidad'),
    x='CUADRANTE',
    y='CATEGORIA',
    size='cantidad',
    title='Relación Cuadrante vs Categoría'
)
st.plotly_chart(fig, width='stretch')
st.markdown("### 📈 Análisis Temporal")

## GRÁFICO VIII ##
df['fecha_completa'] = pd.to_datetime(df['FECHA Y HORA'])
df['fecha'] = df['fecha_completa'].dt.date
df_linea = df.groupby('fecha').size().reset_index(name='cantidad')
df_linea['fecha'] = pd.to_datetime(df_linea['fecha'])
df_linea = df_linea.sort_values('fecha')
fig_linea = px.line(
    df_linea,
    x='fecha',
    y='cantidad',
    title='Reportes Diarios',
    labels={'fecha': 'Fecha', 'cantidad': 'Cantidad'},
    markers=True
)
fig_linea.update_layout(
    template='plotly_white',
    height=400,
    hovermode='x unified',
    xaxis_title='Fecha',
    yaxis_title='Cantidad de Registros'
)
st.plotly_chart(fig_linea, width='stretch')

## Gráfico IX ##
df['semana'] = df['fecha_completa'].dt.isocalendar().week
df_semana = df.groupby('semana').size().reset_index(name='cantidad')

fig = px.line(df_semana, x='semana', y='cantidad', 
              title='Tendencia Semanal', markers=True)
st.plotly_chart(fig, width='stretch')
st.markdown("### 📅 Análisis Detallado")

## GRÁFICO X, XI ##
matriz('Cuadrante')
matriz('Categoria')

## GRÁFICO XII ##
df['fecha_completa'] = pd.to_datetime(df['FECHA Y HORA'])
df['hora'] = df['fecha_completa'].dt.hour
df = df.dropna(subset=['hora'])
df['hora'] = df['hora'].astype(int)
df['dia'] = df['fecha_completa'].dt.weekday
df = df.dropna(subset=['dia'])
df['dia'] = df['dia'].astype(int)
df['rango_horario'] = df['hora'].apply(get_rango_horario)
matriz = pd.crosstab(df['rango_horario'], df['dia'])
rangos_orden = [
    "00:00 - 03:59",
    "04:00 - 07:59",
    "08:00 - 11:59",
    "12:00 - 15:59",
    "16:00 - 19:59",
    "20:00 - 23:59"
]
rangos_existentes = [r for r in rangos_orden if r in matriz.index]
matriz = matriz.loc[rangos_existentes]
fig_heatmap = px.imshow(
    matriz,
    labels=dict(x="Día de la Semana", y="Rango Horario", color="Frecuencia"),
    title="Matriz de Calor: Registros por Día y Rango Horario",
    color_continuous_scale='RdYlGn_r',
    aspect='auto'
)
fig_heatmap.update_traces(text=matriz.values, texttemplate='%{text}')
fig_heatmap.update_layout(
    height=400,
    xaxis_title='Día de la Semana',
    yaxis_title='Rango Horario'
)
st.plotly_chart(fig_heatmap, width='stretch')

## GRÁFICOS XIII, XIV, XV, XVI, XVII, XVIII ##
pie_tipo('Seguridad')
pie_tipo('Planes Operativos')
pie_tipo('Emergencia/Espacio Públicos')
pie_tipo('Fiscalización')
if df[df['CATEGORIA'] == 'Incivilidades'].shape[0] > 0:
    pie_tipo('Incivilidades')
pie_tipo('Otros')