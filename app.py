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
    if st.button("Gráficas Comparativas", key='nav_comp', width='stretch'):
        st.switch_page("pages/5_Graficas_Comparativas.py")

## Descripción general de la aplicación ##
st.markdown("---")
## Información sobre la data comprendida en la aplicación ##
dfr = pd.read_csv('info.csv', sep=';', engine='python')
dfr['FECHA Y HORA'] = pd.to_datetime(dfr['FECHA Y HORA'])
first_hist = dfr.iloc[0]['FECHA Y HORA']
last_hist = dfr.iloc[-1]['FECHA Y HORA']
st.markdown(f"Información integrada desde **{first_hist}** a **{last_hist}**")

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
st.header("⚖️ Gráficas Comparativas")
st.write("""
        Gráfica comparativa del comportamiento de los tipos de procedimientos. Seleccione una categoría o un conjunto de tipos de procedimientos y un rango de fechas (verificar que este rango de fechas tenga información en más de un año diferente, para que lo que se muestre tenga sentido). Se desplegará un gráfico de barras con todos los procedimientos seleccionados por año, una tabla con lo anterior, y además por cada tipo de procedimiento un gráfico de barras con el comportamiento semanal en cada año disponible.
""")