from datetime import date
from sqlalchemy import text
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Data Histórica", layout="wide")
st.logo("./logo.png",size='large',icon_image="./logo.png")

st.title("🗃️ Data Histórica Reportes Central Ñuñoa 2023-2024")

# Validación por seguridad
from auth import check_auth
if not check_auth():
    st.stop()

# Conexión
conn = st.connection("neon", type="sql")

# Funciones
@st.cache_data(ttl=3600)
def obtener_opciones(_conn,columna):
    columnas = {
        "categoria",
        "tipo_de_procedimiento",
        "cuadrante",
        "canal_de_ingreso",
    }
    if columna not in columnas:
        raise ValueError("Columna no permitida")
    consulta = text(f"""
        SELECT DISTINCT {columna}
        FROM public.historico
        WHERE {columna} IS NOT NULL
            AND TRIM({columna}) <> ''
        ORDER BY {columna}
    """)

    with _conn.engine.connect() as conexion:
        resultado = pd.read_sql_query(consulta,conexion)
    return resultado[columna].tolist()

@st.cache_data(ttl=3600)
def obtener_rango_fechas(_conn):
    consulta = text("""
        SELECT MIN(fecha) AS fecha_min,
               MAX(fecha) AS fecha_max
        FROM public.historico
    """)
    with _conn.engine.connect() as conexion:
        resultado = pd.read_sql_query(consulta, conexion)
    return resultado.iloc[0]["fecha_min"], resultado.iloc[0]["fecha_max"]

# Filtros
st.caption("Filtros")

filtrar_fecha = st.checkbox("Filtrar por fecha")

fecha_desde = None
fecha_hasta = None


if filtrar_fecha:
    fecha_min, fecha_max = obtener_rango_fechas(conn)

    if pd.notna(fecha_min) and pd.notna(fecha_max):
        fecha_min = pd.Timestamp(fecha_min).date()
        fecha_max = pd.Timestamp(fecha_max).date()

        fecha_desde = st.date_input(
            "Fecha de inicio",
            value=fecha_min,
            min_value=fecha_min,
            max_value=fecha_max,
            key="fecha_inicio"
        )

        fecha_hasta = st.date_input(
            "Fecha de término",
            value=fecha_max,
            min_value=fecha_min,
            max_value=fecha_max,
            key="fecha_termino"
        )

        if fecha_desde > fecha_hasta:
            st.warning(
                "La fecha de inicio debe ser anterior "
                "o igual a la fecha de término."
            )
            st.stop()

# Filtros categóricos
def opciones_filtro(columna, etiqueta):
    opciones = obtener_opciones(conn, columna)

    return st.selectbox(
        etiqueta,
        ["Todas"] + opciones,
        key=f"filtro_{columna}"
    )


categoria = opciones_filtro("categoria", "Categoría")
tipo = opciones_filtro(
    "tipo_de_procedimiento", "Tipo de procedimiento"
)
cuadrante = opciones_filtro("cuadrante", "Cuadrante")
canal = opciones_filtro("canal_de_ingreso", "Canal de ingreso")

busqueda = st.text_input(
    "Buscar texto",
    placeholder="Dirección, calle, descripción..."
)

condiciones = []
parametros = {}

if filtrar_fecha and fecha_desde and fecha_hasta:
    condiciones.append("fecha >= :fecha_desde")
    condiciones.append("fecha <= :fecha_hasta")
    parametros["fecha_desde"] = fecha_desde
    parametros["fecha_hasta"] = fecha_hasta

for columna, valor in [
    ("categoria", categoria),
    ("tipo_de_procedimiento", tipo),
    ("cuadrante", cuadrante),
    ("canal_de_ingreso", canal),
]:
    if valor != "Todas":
        condiciones.append(f"{columna} = :{columna}")
        parametros[columna] = valor

if busqueda.strip():
    condiciones.append("""
        (
            nro ILIKE :busqueda
            OR calle ILIKE :busqueda
            OR direccion_procedimiento ILIKE :busqueda
            OR descripcion_del_procedimiento ILIKE :busqueda
            OR nombre_de_recurrente ILIKE :busqueda
        )
    """)
    parametros["busqueda"] = f"%{busqueda.strip()}%"

where_sql = (
    "WHERE " + " AND ".join(condiciones)
    if condiciones else ""
)

# --------------------------------------------------
# CONTAR RESULTADOS
# --------------------------------------------------

sql_conteo = text(f"""
    SELECT COUNT(*)
    FROM public.historico
    {where_sql}
""")

with conn.engine.connect() as conexion:
    total = conexion.execute(
        sql_conteo, parametros
    ).scalar_one()

# --------------------------------------------------
# PAGINACIÓN
# --------------------------------------------------

st.subheader(f"Resultados: {total:,}")

tamano_pagina = st.selectbox(
    "Registros por página",
    [50, 100, 250, 500],
    index=1
)

total_paginas = max(
    1, (total + tamano_pagina - 1) // tamano_pagina
)

if "pagina" not in st.session_state:
    st.session_state.pagina = 0

if st.session_state.pagina >= total_paginas:
    st.session_state.pagina = 0

col_anterior, col_info, col_siguiente = st.columns([1, 3, 1])

with col_anterior:
    if st.button(
        "← Anterior",
        disabled=st.session_state.pagina == 0
    ):
        st.session_state.pagina -= 1
        st.rerun()

with col_info:
    st.write(
        f"Página {st.session_state.pagina + 1} "
        f"de {total_paginas}"
    )

with col_siguiente:
    if st.button(
        "Siguiente →",
        disabled=st.session_state.pagina >= total_paginas - 1
    ):
        st.session_state.pagina += 1
        st.rerun()

# --------------------------------------------------
# CONSULTAR SOLO LA PÁGINA ACTUAL
# --------------------------------------------------

offset = st.session_state.pagina * tamano_pagina

sql_datos = text(f"""
    SELECT
        nro,
        fecha,
        hora,
        categoria,
        tipo_de_procedimiento,
        calle,
        direccion_procedimiento,
        cuadrante,
        canal_de_ingreso,
        estado_del_procedimiento
    FROM public.historico
    {where_sql}
    ORDER BY fecha ASC NULLS LAST, nro ASC
    LIMIT :limite OFFSET :offset
""")

parametros_pagina = {
    **parametros,
    "limite": tamano_pagina,
    "offset": offset,
}

with conn.engine.connect() as conexion:
    df = pd.read_sql_query(
        sql_datos,
        conexion,
        params=parametros_pagina
    )

st.dataframe(
    df,
    width='stretch',
    hide_index=True,
    height=600
)