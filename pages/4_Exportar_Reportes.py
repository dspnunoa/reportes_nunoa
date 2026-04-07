import io
import pandas as pd
import plotly.express as px
import pytz
import streamlit as st
import time
from datetime import datetime
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

st.set_page_config(page_title="Generación de Informe", layout="wide")

st.title("📝 Generación de Informe Reportes Central Ñuñoa 2026")

# Título y botones en una fila
col1, col2, col3, col4, col5 = st.columns(5)

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
with col5:
    if st.button("Exportar Reportes", key="nav_report", width='stretch'):
        st.switch_page("pages/4_Exportar_Reportes.py")
st.markdown("---")

st.subheader("Instrucciones de Uso")
st.markdown(f" 1. Elegir rango de fechas. Por defecto, se elegirá el total del archivo.\n 2. Seleccionar aspectos a analizar.\n 3. COMPLETAR OTROS.")
##
fec1, fec2 = st.columns(2)
dfr = pd.read_csv('info.csv',sep=';',engine='python',encoding='utf-8')
dfr['FECHA Y HORA'] = pd.to_datetime(dfr['FECHA Y HORA'])
with fec1:
    finicio = st.date_input("Fecha inicial:", value=None)
with fec2:
    ffinal = st.date_input("Fecha final:", value=None)

if finicio and ffinal:
    df = dfr[(dfr['FECHA Y HORA'].dt.date >= finicio) & (dfr['FECHA Y HORA'].dt.date <= ffinal)].copy()
else:
    df = dfr.copy()
    finicio = str(df['FECHA Y HORA'].min()).split(' ')[0]
    ffinal = str(df['FECHA Y HORA'].max()).split(' ')[0]
##
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
    titulo = st.text_input("Título",'',placeholder="Elige")

##### GRAN FUNCION #####
def crear_pdf_con_graficos_y_tablas(titulo, metricas, graficos_dict, tablas_dict):
    """
    Crea un PDF con gráficos y tablas
    
    Args:
        titulo: Título del reporte
        metricas: Dict con {nombre: valor}
        graficos_dict: Dict con {nombre: figura_plotly}
        tablas_dict: Dict con {nombre: dataframe}
    """
    
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, title='Reporte Ñuñoa',pagesize=landscape(letter), topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=20,
    )
    
    # Título
    elements.append(Paragraph(titulo, title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # SECCIÓN: MÉTRICAS
    if metricas:
        elements.append(Paragraph("Métricas Principales", styles['Heading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        # Crear tabla de métricas
        data = [['Métrica', 'Valor']]
        for nombre, valor in metricas.items():
            data.append([nombre, str(valor)])
        
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f2f6')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f2f6')])
        ]))
        elements.append(table)
        elements.append(PageBreak())
    
    # SECCIÓN: GRÁFICOS
    if graficos_dict:
        elements.append(Paragraph("Gráficos", styles['Heading2']))
        elements.append(Spacer(1, 0.2*inch))
        
        for nombre_grafico, fig in graficos_dict.items():
            try:
                # Convertir gráfico a imagen PNG
                img_bytes = fig.to_image(format="png", width=700, height=400)
                img_buffer = io.BytesIO(img_bytes)
                
                # Agregar título del gráfico
                elements.append(Paragraph(nombre_grafico, styles['Heading3']))
                elements.append(Spacer(1, 0.1*inch))
                
                # Agregar imagen
                img = Image(img_buffer, width=6*inch, height=3.5*inch)
                elements.append(img)
                elements.append(Spacer(1, 0.3*inch))
                
            except Exception as e:
                elements.append(Paragraph(f"Error al generar gráfico: {nombre_grafico}", styles['Normal']))
                st.warning(f"Error con gráfico {nombre_grafico}: {e}")
        
        elements.append(PageBreak())
    
    # SECCIÓN: TABLAS
    if tablas_dict:
        elements.append(Paragraph("Datos Detallados", styles['Heading2']))
        elements.append(Spacer(1, 0.2*inch))
        
        for nombre_tabla, df in tablas_dict.items():
            # Título de la tabla
            elements.append(Paragraph(f"{nombre_tabla} ({len(df)} registros)", styles['Heading3']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Convertir DataFrame a lista (máximo 15 filas por tabla)
            df_truncado = df.head(15)
            data = [df_truncado.columns.tolist()] + df_truncado.values.tolist()
            
            # Crear tabla
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
            ]))
            elements.append(table)
            elements.append(Spacer(1, 0.2*inch))
            
            if len(df) > 15:
                elements.append(Paragraph(f"Mostrando 15 de {len(df)} registros", styles['Italic']))
            
            elements.append(PageBreak())
    
    # Construir PDF
    doc.build(elements)
    pdf_buffer.seek(0)
    
    return pdf_buffer
########################

# GRÁFICOS
fig_barras = px.bar(
    df.groupby('CUADRANTE').size().reset_index(name='cantidad'),
    x='CUADRANTE',
    y='cantidad',
    title='Registros por Cuadrante',
    color_discrete_sequence=['#1f77b4']
)

fig_pie = px.pie(
    df.groupby('CATEGORIA').size().reset_index(name='cantidad'),
    names='CATEGORIA',
    values='cantidad',
    title='Distribución por Categoría',
    color_discrete_sequence=px.colors.sequential.Rainbow
)

df['fecha'] = df['FECHA Y HORA'].dt.date
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

# ==================== EXPORTAR A PDF ====================
local_tz = pytz.timezone("America/Santiago") 
now_local = datetime.now(local_tz)
st.markdown("---")
st.subheader("📥 Descargar Reporte")

if st.button("📄 Generar PDF"):
    with st.spinner("Generando PDF..."):
        try:
            # Preparar métricas
            metricas = {
                'Total de procedimientos': len(df),
                'Cuadrante con más reportes': df['CUADRANTE'].value_counts().index[0],
                'Procedimiento más común': df['TIPO DE PROCEDIMIENTO'].value_counts().index[0],
                'Hora punta': f"{df['FECHA Y HORA'].dt.hour.value_counts().index[0]}:00" ,
                'Día con más reportes':df['FECHA Y HORA'].dt.date.value_counts().index[0],
                'Calle con más reportes': df['CALLE'].value_counts().index[0] if df['CALLE'].value_counts().index[0] != "Nan" else df['CALLE'].value_counts().index[1]
            }
            
            # Preparar gráficos
            graficos = {
                'Registros por Cuadrante': fig_barras,
                'Distribución por Categoría': fig_pie,
                'Evolución Temporal': fig_linea,
            }
            
            # Preparar tablas
            tablas = {
                'Top Cuadrantes': df['CUADRANTE'].value_counts().reset_index(name='Cantidad').head(10),
                'Top Tipos': df['TIPO DE PROCEDIMIENTO'].value_counts().reset_index(name='Cantidad').head(10),
                'Últimos Registros': df[['FECHA Y HORA', 'CUADRANTE', 'TIPO DE PROCEDIMIENTO', 'CATEGORIA']].tail(15),
            }
            
            # Crear PDF
            if titulo:
                pdf = crear_pdf_con_graficos_y_tablas(
                    f"{titulo}: {finicio} a {ffinal}",
                    metricas,
                    graficos,
                    tablas
                )
            else:
                pdf = crear_pdf_con_graficos_y_tablas(
                    f"Reporte de Análisis de Procedimientos: {finicio} a {ffinal}",
                    metricas,
                    graficos,
                    tablas
                )
            
            # Descargar
            st.download_button(
                label="📥 Descargar PDF",
                data=pdf,
                file_name=f"reporte_analisis{str(now_local.strftime('%Y%m%d%H%M%S'))}.pdf",
                mime="application/pdf",
                width='stretch'
            )
            
            st.success("✅ PDF generado exitosamente")
            
        except Exception as e:
            st.error(f"❌ Error al generar PDF: {e}")