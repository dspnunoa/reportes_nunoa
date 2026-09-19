from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np
from scipy import stats

## Configuración inicial aplicación ##
st.set_page_config(page_title="Dashboard", layout="wide")
st.logo("./logo.png",size='large',icon_image="./logo.png")
st.title("📈 Dashboard Reportes Central Ñuñoa 2026")

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
    if st.button("Dashboard", key="nav_dash", width='stretch', type="primary"):
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
st.markdown("---")

## Cargo el excel ##
dfr = pd.read_csv('info.csv', sep=';', engine='python')
dfr['FECHA Y HORA'] = pd.to_datetime(dfr['FECHA Y HORA'])
dias_hist = ((dfr['FECHA Y HORA'].max() - dfr['FECHA Y HORA'].min()).days)+1
prom_hist = round(len(dfr) / max(dias_hist, 1), 1)
first_hist = dfr.iloc[0]['FECHA Y HORA']
last_hist = dfr.iloc[-1]['FECHA Y HORA']
st.markdown(f"Información integrada desde **{first_hist}** a **{last_hist}**")

## Función auxiliar para evitar errores de formato ##
def is_time(time_str):
    try:
        datetime.strptime(str(time_str), '%H:%M')
        return True
    except ValueError:
        return False


## Agrego la opción de elegir un período ##
col1, col2 = st.columns(2)
with col1:
    finicio = st.date_input("Fecha inicial:", value=None)
with col2:
    ffinal = st.date_input("Fecha final:", value=None)

if finicio and ffinal:
    df = dfr[(dfr['FECHA Y HORA'].dt.date >= finicio) & (dfr['FECHA Y HORA'].dt.date <= ffinal)].copy()
else:
    df = dfr.copy()

st.subheader(f"ℹ️ Métricas Principales")
dias_cubiertos = ((df['FECHA Y HORA'].max() - df['FECHA Y HORA'].min()).days)+1
met1, met2, met3, met4 = st.columns(4, border=True)
with met1:
    st.metric("Número de Reportes",f"{df.shape[0]}")
with met2:
    cuad_metric = df['CUADRANTE'].value_counts().index[0]
    st.metric("Cuadrante con más Reportes",cuad_metric,delta=f"{df['CUADRANTE'].value_counts().iloc[0]}",delta_arrow="off")
with met3:
    tipo_metric = df['TIPO DE PROCEDIMIENTO'].value_counts().index[0]
    st.metric("Procedimiento más común",tipo_metric,delta=f"{df['TIPO DE PROCEDIMIENTO'].value_counts().iloc[0]}",width="content",delta_arrow="off")
with met4:
    hora_metric = df['FECHA Y HORA'].dt.hour.value_counts().index[0]
    st.metric("Horario Punta",f"{int(hora_metric):02d}:00-{int(hora_metric+1):02d}:00",delta=df['FECHA Y HORA'].dt.hour.value_counts().iloc[0],width="content",delta_arrow="off")

met5, met6, met7, met8 = st.columns(4, border=True)
with met5:
    fecha_metric = df['FECHA Y HORA'].dt.date.value_counts().index[0]
    st.metric("Día con más reportes",f"{fecha_metric}",delta=df['FECHA Y HORA'].dt.date.value_counts().iloc[0], delta_arrow="off")
with met6:
    st.metric("Días Cubiertos",dias_cubiertos)
with met7:
    dia_metric = df['FECHA Y HORA'].dt.day_name().value_counts().index[0]
    dict_dias = {'Monday':'Lunes','Tuesday':'Martes','Wednesday':'Miércoles','Thursday':'Jueves','Friday':'Viernes','Saturday':'Sábado','Sunday':'Domingo'}
    dies = dict_dias[dia_metric]
    st.metric("Día de la semana con más Reportes",dies,delta=f"{df['FECHA Y HORA'].dt.day_name().value_counts().iloc[0]}",delta_arrow="off")

with met8:
    promedio_diario = round(len(df) / max(dias_cubiertos, 1), 1)
    st.metric("Promedio Diario",f"{promedio_diario} reportes/día",delta=round((promedio_diario-prom_hist),1),delta_color="inverse")

met9, met10, met11, met12 = st.columns(4, border=True)
with met9:
    calle_metric = df['CALLE'].value_counts().index[0]
    if calle_metric == 'Nan':
        calle_metric = df['CALLE'].value_counts().index[1]
    st.metric("Calle con más Reportes",calle_metric,delta=f"{df['CALLE'].value_counts().iloc[0]}",delta_arrow="off")
with met10:
    if df['LUGAR PÚBLICO /  PRIVADO'].isnull().all():
        st.metric("Tipo de lugar más común",'NO Aplica')
    else:
        lugar_metric = df['LUGAR PÚBLICO /  PRIVADO'].value_counts().index[0]
        st.metric("Tipo de lugar más común",lugar_metric,delta=f"{df['LUGAR PÚBLICO /  PRIVADO'].value_counts().iloc[0]}",delta_arrow="off")
## M11 ##
d11 = dfr[dfr['HORA DE ASIGNACION A INSPECTOR'].apply(is_time) & dfr['HORA DE ARRIBO'].apply(is_time)]
d11 = d11[d11['HORA DE ARRIBO'] > d11['HORA DE ASIGNACION A INSPECTOR']]
d11['HORA DE ASIGNACION A INSPECTOR'] = pd.to_timedelta(d11['HORA DE ASIGNACION A INSPECTOR'] + ':00')
d11['HORA DE ARRIBO'] = pd.to_timedelta(d11['HORA DE ARRIBO'] + ':00')
d11['DIF'] = d11['HORA DE ARRIBO'] - d11['HORA DE ASIGNACION A INSPECTOR']
p11 = str(d11['DIF'].mean())
p11 = p11.split(' ')[2]
p11 = p11.split('.')[0]
with met11:
    dft = df[df['HORA DE ASIGNACION A INSPECTOR'].apply(is_time) & df['HORA DE ARRIBO'].apply(is_time)]
    dft = dft[dft['HORA DE ARRIBO'] > dft['HORA DE ASIGNACION A INSPECTOR']]
    dft['HORA DE ASIGNACION A INSPECTOR'] = pd.to_timedelta(dft['HORA DE ASIGNACION A INSPECTOR'] + ':00')
    dft['HORA DE ARRIBO'] = pd.to_timedelta(dft['HORA DE ARRIBO'] + ':00')
    dft['DIF'] = dft['HORA DE ARRIBO'] - dft['HORA DE ASIGNACION A INSPECTOR']
    prom = str(dft['DIF'].mean())
    promf = prom.split(' ')[2]
    promf = promf.split('.')[0]
    formato = "%H:%M:%S"
    promf_t = datetime.strptime(promf, formato)
    p11_t = datetime.strptime(p11, formato)
    if promf_t > p11_t:
        dif = promf_t-p11_t
        dc = "red"
        da = "up"
    else:
        dif = p11_t-promf_t
        dc = "green"
        da = "down"
    st.metric("Media Tiempo Asignación-Arribo",promf,delta=f"{str(dif)}", delta_color=dc, delta_arrow=da)
## M12 ##
d12 = dfr[dfr['HORA DE ARRIBO'].apply(is_time) & dfr['HORA DE TERMINO'].apply(is_time)]
d12 = d12[d12['HORA DE TERMINO'] > d12['HORA DE ARRIBO']]
d12['HORA DE ARRIBO'] = pd.to_timedelta(d12['HORA DE ARRIBO'] + ':00')
d12['HORA DE TERMINO'] = pd.to_timedelta(d12['HORA DE TERMINO'] + ':00')
d12['DIF'] = d12['HORA DE TERMINO'] - d12['HORA DE ARRIBO']
p12 = str(d12['DIF'].mean())
p12 = p12.split(' ')[2]
p12 = p12.split('.')[0]
with met12:
    dft = df[df['HORA DE ARRIBO'].apply(is_time) & df['HORA DE TERMINO'].apply(is_time)]
    dft = dft[dft['HORA DE TERMINO'] > dft['HORA DE ARRIBO']]
    dft['HORA DE ARRIBO'] = pd.to_timedelta(dft['HORA DE ARRIBO'] + ':00')
    dft['HORA DE TERMINO'] = pd.to_timedelta(dft['HORA DE TERMINO'] + ':00')
    dft['DIF'] = dft['HORA DE TERMINO'] - dft['HORA DE ARRIBO']
    prom = str(dft['DIF'].mean())
    promf = prom.split(' ')[2]
    promf = promf.split('.')[0]
    formato = "%H:%M:%S"
    promf_t = datetime.strptime(promf, formato)
    p12_t = datetime.strptime(p12, formato)
    if promf_t > p12_t:
        dif = promf_t-p12_t
        dc = "red"
        da = "up"
    else:
        dif = p12_t-promf_t
        dc = "green"
        da = "down"
    st.metric("Media Tiempo Arribo-Termino",promf,delta=f"{str(dif)}", delta_color=dc, delta_arrow=da)

## Funciones de gráficos y auxiliares para gráficos ##
def get_rango_horario(hora):
    """Convierte hora (0-23) en rango de 4 horas"""
    rango = int((hora // 4) * 4)
    return f"{rango:02d}:00 - {rango+3:02d}:59"

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

def barra(filtro):
    if filtro == 'Día de la Semana':
        l1 = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
        l2 = df["FECHA Y HORA"].dt.weekday.value_counts()
        l2 = list(l2.sort_index())
        fig_barras = px.bar(
            x=l1,
            y=l2,
            title='Reportes por '+filtro
        )
    elif filtro == 'Hora':
        l1 = ['00:00-01:00','01:00-02:00','02:00-03:00','03:00-04:00','04:00-05:00','05:00-06:00','06:00-07:00','07:00-08:00','08:00-09:00','09:00-10:00','10:00-11:00','11:00-12:00','12:00-13:00','13:00-14:00','14:00-15:00','15:00-16:00','16:00-17:00','17:00-18:00','18:00-19:00','19:00-20:00','20:00-21:00','21:00-22:00','22:00-23:00','23:00-24:00']
        l2 = df["FECHA Y HORA"].dt.hour.value_counts()
        l2 = list(l2.sort_index())
        fig_barras = px.bar(
            x=l1,
            y=l2,
            title='Reportes por '+filtro
        )
    elif filtro == 'CATEGORIA':
        counts = df["CATEGORIA"].value_counts()
        fig_barras = px.bar(
            counts,
            title='Reportes por Categoría'
        )
        filtro = filtro.title()
    fig_barras.update_layout(
        xaxis_title=filtro,
        yaxis_title='Reportes'
    )
    st.plotly_chart(fig_barras,width='stretch')

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
## TENDENCIA DIARIA ##
if finicio and ffinal:
    st.markdown("---")
    st.subheader("📉 Tendencia Diaria")
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
    x = np.arange(len(df_linea))
    coef = np.polyfit(x,df_linea['cantidad'],1)
    tendencia = np.polyval(coef,x)
    fig_linea.add_scatter(
        x=df_linea['fecha'],
        y=tendencia,
        mode='lines',
        name='Tendencia'
    )
    fig_linea.update_layout(
        template='plotly_white',
        height=400,
        hovermode='x unified',
        xaxis_title='Fecha',
        yaxis_title='Cantidad de Registros'
    )
    st.plotly_chart(fig_linea, width='stretch')
## ANOMALIAS ##
def detectar_anomalias(valores):
    """
    Detecta anomalías usando método de desviación estándar
    Anomalía = valor > (promedio + 2*desv_estándar)
    """
    promedio = valores.mean()
    desv_est = valores.std()
    limite = promedio + (2 * desv_est)
    
    anomalias = valores > limite
    return anomalias, limite, promedio, desv_est
with st.expander("⚠️ Alerta de Anomalías", expanded=False):
    # Agrupar por tipo y contar
    datos_por_tipo = df.groupby('TIPO DE PROCEDIMIENTO').size().reset_index(name='frecuencia')
    datos_por_cuadrante = df.groupby('CUADRANTE').size().reset_index(name='frecuencia')
    datos_por_categoria = df.groupby('CATEGORIA').size().reset_index(name='frecuencia')

    # Detectar anomalías en cada grupo
    anomalias_tipo, limite_tipo, prom_tipo, desv_tipo = detectar_anomalias(datos_por_tipo['frecuencia'])
    anomalias_cuad, limite_cuad, prom_cuad, desv_cuad = detectar_anomalias(datos_por_cuadrante['frecuencia'])
    anomalias_cat, limite_cat, prom_cat, desv_cat = detectar_anomalias(datos_por_categoria['frecuencia'])

    # RECOPILAR TODAS LAS ANOMALÍAS
    alertas_totales = []

    for idx, row in datos_por_tipo.iterrows():
        if anomalias_tipo[idx]:
            alertas_totales.append({
                'Tipo': 'Tipo de Procedimiento',
                'Valor': row['TIPO DE PROCEDIMIENTO'],
                'Frecuencia': row['frecuencia'],
                'Límite Normal': f"{limite_tipo:.0f}",
                'Severidad': 'Alta' if row['frecuencia'] > limite_tipo * 1.5 else 'Media'
            })

    for idx, row in datos_por_cuadrante.iterrows():
        if anomalias_cuad[idx]:
            alertas_totales.append({
                'Tipo': 'Cuadrante',
                'Valor': row['CUADRANTE'],
                'Frecuencia': row['frecuencia'],
                'Límite Normal': f"{limite_cuad:.0f}",
                'Severidad': 'Alta' if row['frecuencia'] > limite_cuad * 1.5 else 'Media'
            })

    for idx, row in datos_por_categoria.iterrows():
        if anomalias_cat[idx]:
            alertas_totales.append({
                'Tipo': 'Categoría',
                'Valor': row['CATEGORIA'],
                'Frecuencia': row['frecuencia'],
                'Límite Normal': f"{limite_cat:.0f}",
                'Severidad': 'Alta' if row['frecuencia'] > limite_cat * 1.5 else 'Media'
            })

    # MOSTRAR ALERTAS
    if alertas_totales:
        df_alertas = pd.DataFrame(alertas_totales)
        
        # Separar por severidad
        alertas_altas = df_alertas[df_alertas['Severidad'] == 'Alta']
        alertas_medias = df_alertas[df_alertas['Severidad'] == 'Media']
        
        # Métricas de resumen
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "🔴 Alertas Críticas",
                len(alertas_altas),
                "Valores muy por encima del promedio"
            )
        
        with col2:
            st.metric(
                "🟡 Alertas Medias",
                len(alertas_medias),
                "Valores ligeramente elevados"
            )
        
        with col3:
            st.metric(
                "ℹ️ Total Anomalías",
                len(df_alertas),
                "Registros inusuales detectados"
            )
        
        # MOSTRAR ALERTAS CRÍTICAS
        if len(alertas_altas) > 0:
            st.error("🔴 **ALERTAS CRÍTICAS** - Revisar inmediatamente")
            
            for idx, alerta in alertas_altas.iterrows():
                st.markdown(f"""
                **{alerta['Tipo']}: {alerta['Valor']}**
                - Frecuencia: {alerta['Frecuencia']} procedimientos
                - Límite normal: {alerta['Límite Normal']} procedimientos
                - Exceso: {alerta['Frecuencia'] - float(alerta['Límite Normal']):.0f} por encima
                """)
        
        # MOSTRAR ALERTAS MEDIAS
        if len(alertas_medias) > 0:
            st.warning("🟡 **ALERTAS MEDIAS** - Monitorear")
            
            for idx, alerta in alertas_medias.iterrows():
                st.markdown(f"""
                **{alerta['Tipo']}: {alerta['Valor']}**
                - Frecuencia: {alerta['Frecuencia']} procedimientos
                - Límite normal: {alerta['Límite Normal']} procedimientos
                """)
        
        # TABLA DE TODAS LAS ANOMALÍAS
        st.subheader("📋 Tabla de Anomalías Detectadas")
        st.dataframe(
            df_alertas.sort_values('Frecuencia', ascending=False),
            width='stretch',
            hide_index=True
        )

    else:
        st.success("✅ No hay anomalías detectadas - Todo normal")

    # ==================== INFORMACIÓN ESTADÍSTICA ====================

    st.markdown("---")
    st.subheader("📊 Parámetros de Detección")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Promedio (Tipo)",
            f"{prom_tipo:.1f}",
            "Procedimientos promedio por tipo"
        )

    with col2:
        st.metric(
            "Desv. Estándar (Tipo)",
            f"{desv_tipo:.1f}",
            "Variabilidad de los datos"
        )

    with col3:
        st.metric(
            "Límite de Anomalía",
            f"{limite_tipo:.0f}",
            "Valor que dispara alerta"
        )

    st.info("""
    **¿Cómo funciona?**
    - Se calcula el promedio de cada categoría
    - Se suma 2 × desviación estándar
    - Si un valor supera este límite → **ANOMALÍA**
    - Severidad Alta: valor > límite × 1.5
    - Severidad Media: valor entre límite y límite × 1.5
    """)

    # ==================== AGREGAR ALERTAS A LA TABLA INTERACTIVA ====================

    # Función para colorear filas con anomalías
    def aplicar_colores_anomalias(df_mostrar, tipo_alerta='TIPO DE PROCEDIMIENTO'):
        """Marca filas con anomalías para visualización"""
        
        def highlight_fila(row):
            # Contar frecuencia de este tipo
            frecuencia = len(df[df[tipo_alerta] == row[tipo_alerta]])
            
            anomalia, limite, prom, desv = detectar_anomalias(
                df.groupby(tipo_alerta).size().values
            )
            
            limite_val = prom + (2 * desv)
            
            if frecuencia > limite_val:
                return ['background-color: #ffcccc'] * len(row)  # Rojo claro
            else:
                return [''] * len(row)
        
        return df_mostrar.style.apply(highlight_fila, axis=1)

###############
## ESTADISTICAS DESCRIPTIVAS ##
with st.expander("📈 Estadísticas Avanzadas", expanded=False):
    
    # Seleccionar qué analizar
    col1, col2 = st.columns(2)
    
    with col1:
        tipo_analisis = st.selectbox(
            "Analizar por:",
            ["Tipo de Procedimiento", "Cuadrante", "Categoría"]
        )
    
    with col2:
        metrica = st.selectbox(
            "Métrica:",
            ["Frecuencia de Reportes", "Duración (si disponible)"]
        )
    
    # CALCULAR ESTADÍSTICAS
    if tipo_analisis == "Tipo de Procedimiento":
        columna = 'TIPO DE PROCEDIMIENTO'
    elif tipo_analisis == "Cuadrante":
        columna = 'CUADRANTE'
    else:
        columna = 'CATEGORIA'
    
    # Agrupar y contar
    datos_agrupados = df.groupby(columna).size().reset_index(name='frecuencia')
    
    # Crear tabla de estadísticas
    estadisticas = {
        'Categoría': datos_agrupados[columna],
        'Min': datos_agrupados['frecuencia'].min(),
        'Max': datos_agrupados['frecuencia'].max(),
        'Promedio': datos_agrupados['frecuencia'].mean(),
        'Mediana': datos_agrupados['frecuencia'].median(),
        'Desv. Estándar': datos_agrupados['frecuencia'].std(),
        'Q1 (25%)': datos_agrupados['frecuencia'].quantile(0.25),
        'Q3 (75%)': datos_agrupados['frecuencia'].quantile(0.75),
        'Total': datos_agrupados['frecuencia'].sum()
    }
    
    # TABLA GENERAL
    st.subheader(f"📊 Estadísticas Generales - {tipo_analisis}")
    
    tabla_general = pd.DataFrame({
        'Métrica': ['Mínimo', 'Máximo', 'Promedio', 'Mediana', 'Desv. Estándar', 'Q1 (25%)', 'Q3 (75%)', 'Total'],
        'Valor': [
            f"{datos_agrupados['frecuencia'].min():.0f}",
            f"{datos_agrupados['frecuencia'].max():.0f}",
            f"{datos_agrupados['frecuencia'].mean():.2f}",
            f"{datos_agrupados['frecuencia'].median():.0f}",
            f"{datos_agrupados['frecuencia'].std():.2f}",
            f"{datos_agrupados['frecuencia'].quantile(0.25):.0f}",
            f"{datos_agrupados['frecuencia'].quantile(0.75):.0f}",
            f"{datos_agrupados['frecuencia'].sum():.0f}"
        ]
    })
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(tabla_general, width='stretch', hide_index=True)
    
    with col2:
        # Indicador de variabilidad
        cv = (datos_agrupados['frecuencia'].std() / datos_agrupados['frecuencia'].mean()) * 100
        st.metric("Coef. de Variación", f"{cv:.1f}%", "Indica variabilidad")
    
    # TABLA DETALLADA POR CATEGORÍA
    st.subheader(f"📋 Detalles por {tipo_analisis}")
    
    tabla_detallada = datos_agrupados.copy()
    tabla_detallada.columns = [tipo_analisis, 'Frecuencia']
    tabla_detallada['% del Total'] = (tabla_detallada['Frecuencia'] / tabla_detallada['Frecuencia'].sum() * 100).round(2)
    tabla_detallada['Desviación del Promedio'] = (tabla_detallada['Frecuencia'] - datos_agrupados['frecuencia'].mean()).round(2)
    tabla_detallada = tabla_detallada.sort_values('Frecuencia', ascending=False)
    
    st.dataframe(tabla_detallada, width='stretch', hide_index=True)
    
    # VISUALIZACIONES
    st.markdown("---")
    st.subheader("📊 Visualizaciones")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Box plot
        fig_box = go.Figure()
        fig_box.add_trace(go.Box(
            y=datos_agrupados['frecuencia'],
            name='Distribución',
            marker_color='#1f77b4',
            boxmean='sd'  # Muestra promedio y desv. estándar
        ))
        
        fig_box.update_layout(
            title="Box Plot - Distribución de Frecuencias",
            yaxis_title="Frecuencia",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig_box, width='stretch')
    
    with col2:
        # Histograma
        fig_hist = px.histogram(
            datos_agrupados,
            x='frecuencia',
            nbins=15,
            title="Histograma - Distribución de Frecuencias",
            labels={'frecuencia': 'Frecuencia', 'count': 'Cantidad'}
        )
        
        fig_hist.update_traces(marker_color='#ff7f0e')
        fig_hist.update_layout(height=400)
        
        st.plotly_chart(fig_hist, width='stretch')
    
    # Gráfico de barras ordenado
    fig_barras = px.bar(
        tabla_detallada.head(15),
        x=tipo_analisis,
        y='Frecuencia',
        title=f"Top 15 {tipo_analisis} - Frecuencia",
        labels={'Frecuencia': 'Total de Reportes'},
        color='Frecuencia',
        color_continuous_scale='Blues'
    )
    
    fig_barras.update_layout(height=400)
    st.plotly_chart(fig_barras, width='stretch')
    
    # ANÁLISIS ESTADÍSTICO AVANZADO
    st.markdown("---")
    st.subheader("🔬 Análisis Estadístico Avanzado")
    
    # Normalidad (Shapiro-Wilk)
    if len(datos_agrupados) > 3:
        statistic, p_value = stats.shapiro(datos_agrupados['frecuencia'])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            normalidad = "✅ Normal" if p_value > 0.05 else "❌ No Normal"
            st.metric("Test Shapiro-Wilk", normalidad, f"p={p_value:.4f}")
        
        with col2:
            # Simetría (Skewness)
            skewness = stats.skew(datos_agrupados['frecuencia'])
            if abs(skewness) < 0.5:
                simetr = "Simétrica"
            elif skewness > 0:
                simetr = "Sesgada Derecha"
            else:
                simetr = "Sesgada Izquierda"
            
            st.metric("Simetría (Skewness)", simetr, f"{skewness:.2f}")
        
        with col3:
            # Curtosis
            kurtosis = stats.kurtosis(datos_agrupados['frecuencia'])
            if abs(kurtosis) < 0.5:
                kurt = "Normal"
            elif kurtosis > 0:
                kurt = "Leptocúrtica"
            else:
                kurt = "Platicúrtica"
            
            st.metric("Curtosis", kurt, f"{kurtosis:.2f}")
    
    # INTERPRETACIÓN
    st.markdown("---")
    st.info("""
    **Interpretación:**
    - **Min/Max**: Valores extremos
    - **Promedio/Mediana**: Centro de los datos
    - **Desv. Estándar**: Cuánto varían los datos
    - **Q1/Q3**: Rango del 50% central de datos
    - **Coef. Variación**: >30% indica alta variabilidad
    - **Normalidad**: ¿Siguen distribución normal?
    - **Simetría**: ¿Están balanceados los datos?
    """)
###############################
st.markdown("### 📊 Análisis General")
## Gráficos I, II ##
pie('CUADRANTE')
pie('CANAL DE INGRESO')

## Gráficos III, IV, V ##
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

## Gráfico VIII ##
# SE TRASLADÓ DE LUGAR

## Gráfico IX ##
df['semana'] = df['fecha_completa'].dt.isocalendar().week
df_semana = df.groupby('semana').size().reset_index(name='cantidad')

fig = px.line(df_semana, x='semana', y='cantidad', 
              title='Tendencia Semanal', markers=True)
st.plotly_chart(fig, width='stretch')

## Tabla de frecuencia del total de procedimientos ##
st.markdown("### 📁 Desglose del Total de Procedimientos")
a = df['TIPO DE PROCEDIMIENTO'].value_counts() .reset_index().rename(columns={'TIPO DE PROCEDIMIENTO': 'Tipo de Procedimiento', 'count': 'Frecuencia'})
st.dataframe(a,width='stretch')
##

st.markdown("### 📅 Análisis Detallado")

## Gráficos X, XI ##
matriz('Cuadrante')
matriz('Categoria')

## Gráfico XII ##
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

## Gráficos XIII, XIV, XV, XVI, XVII, XVIII ##
pie_tipo('Seguridad')
pie_tipo('Planes Operativos')
pie_tipo('Emergencia/Espacio Públicos')
pie_tipo('Fiscalización')
if df[df['CATEGORIA'] == 'Incivilidades'].shape[0] > 0:
    pie_tipo('Incivilidades')
pie_tipo('Otros')