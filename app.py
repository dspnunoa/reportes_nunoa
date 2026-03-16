import streamlit as st
st.set_page_config(layout="wide")

## Configuración inicial aplicación ##

st.set_page_config(
    page_title="Inicio",
    page_icon="./logo.png",
    layout="wide"
)

st.title("ℹ️ Reportes Procedimientos Central Ñuñoa 2026")


# Título y botones en una fila
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

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

st.markdown("---")

st.header("Bienvenido")
st.write("""
Esta herramienta permite:
- 📍 Visualizar datos en un mapa interactivo
- 📊 Analizar datos a través de gráficas
- 📋 Explorar y filtrar datos en una tabla interactiva

Selecciona una opción en el menú para comenzar.
""")