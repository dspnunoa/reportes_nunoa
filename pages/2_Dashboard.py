from datetime import datetime
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📈 Dashboard Reportes Central Ñuñoa 2026")
## Cargo el excel ##
dfr = pd.read_csv('infofinal.csv',skiprows=1)
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
## FIN FUNCIONES ##

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
st.markdown("### 📊 Análisis General")
## GRÁFICO I ##
df_pie = df.groupby('CUADRANTE').size().reset_index(name='Reportes')
fig_pie = px.pie(
    df_pie,
    names='CUADRANTE',
    values='Reportes',
    title='Reportes por Cuadrante'
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

## GRÁFICO II ##
df_pie = df.groupby('CANAL DE INGRESO').size().reset_index(name='cantidad')
fig_pie = px.pie(
    df_pie,
    names='CANAL DE INGRESO',
    values='cantidad',
    title='Reportes por Vía de Ingreso'
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

## GRÁFICO III ##
counts = df["FECHA Y HORA"].dt.weekday.value_counts()
fig_barras = px.bar(
    counts,
    title='Reportes por Día de la Semana'
)
fig_barras.update_layout(
    xaxis_title='Día de la Semana',
    yaxis_title='Reportes'
)
st.plotly_chart(fig_barras,width='stretch')

## GRÁFICO IV ##
counts = df["FECHA Y HORA"].dt.hour.value_counts()
fig_barras = px.bar(
    counts,
    title='Reportes por Hora'
)
fig_barras.update_layout(
    xaxis_title='Hora',
    yaxis_title='Reportes'
)
st.plotly_chart(fig_barras,width='stretch')

## GRÁFICO V ##
counts = df["CATEGORIA"].value_counts()
fig_barras = px.bar(
    counts,
    title='Reportes por Categoría'
)
fig_barras.update_layout(
    xaxis_title='Categoría',
    yaxis_title='Reportes'
)
st.plotly_chart(fig_barras,width='stretch')

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

## GRÁFICO X ##
df['fecha_completa'] = pd.to_datetime(df['FECHA Y HORA'])
df['hora'] = df['fecha_completa'].dt.hour
df = df.dropna(subset=['hora'])
df['hora'] = df['hora'].astype(int)
df['rango_horario'] = df['hora'].apply(get_rango_horario)
matriz = pd.crosstab(df['rango_horario'], df['CUADRANTE'])
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
    labels=dict(x="Cuadrante", y="Rango Horario", color="Reportes"),
    title="Matriz de Calor: Registros por Cuadrante y Rango Horario",
    color_continuous_scale='RdYlGn_r',
    aspect='auto'
)
fig_heatmap.update_traces(text=matriz.values, texttemplate='%{text}')
fig_heatmap.update_layout(
    height=400,
    xaxis_title='Cuadrante',
    yaxis_title='Rango Horario'
)
st.plotly_chart(fig_heatmap, width='stretch')

## GRÁFICO XI ##
df['fecha_completa'] = pd.to_datetime(df['FECHA Y HORA'])
df['hora'] = df['fecha_completa'].dt.hour
df = df.dropna(subset=['hora'])
df['hora'] = df['hora'].astype(int)
df['rango_horario'] = df['hora'].apply(get_rango_horario)
matriz = pd.crosstab(df['rango_horario'], df['CATEGORIA'])
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
    labels=dict(x="Categoría", y="Rango Horario", color="Reportes"),
    title="Matriz de Calor: Registros por Categoría y Rango Horario",
    color_continuous_scale='RdYlGn_r',
    aspect='auto'
)
fig_heatmap.update_traces(text=matriz.values, texttemplate='%{text}')
fig_heatmap.update_layout(
    height=400,
    xaxis_title='Categoría',
    yaxis_title='Rango Horario'
)
st.plotly_chart(fig_heatmap, width='stretch')

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
pie_tipo('Incivilidades')
pie_tipo('Otros')