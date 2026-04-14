import streamlit as st
## Configuración inicial aplicación ##
st.set_page_config(
    page_title="Inicio",
    page_icon="./logo.png",
    initial_sidebar_state="collapsed",
    layout="wide"
)
st.logo("./logo.png",size='large',icon_image="./logo.png")
##
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
##

st.title("ℹ️ Reportes Procedimientos Central Ñuñoa 2026")


# Título y botones en una fila
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
    if st.button("Gráficas Comparativas", key='nav_comp', width='stretch'):
        st.switch_page("pages/5_Graficas_Comparativas.py")
st.markdown("---")

st.header("Bienvenido")
st.write("""
Esta herramienta permite:
- 🗺️ Visualizar datos en un mapa interactivo
- 📈 Analizar datos a través de gráficas
- 🗃️ Explorar y filtrar datos en una tabla interactiva
- 📝 Generar informes personalizados y estandarizados
- ⚖️ Comparar información por período de tiempo

Selecciona una opción en el menú para comenzar.
""")