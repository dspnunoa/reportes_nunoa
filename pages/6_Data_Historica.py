from datetime import date
import time
import pandas as pd
import streamlit as st
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


st.set_page_config(page_title="Data Histórica", layout="wide")
st.logo("./logo.png",size='large',icon_image="./logo.png")

st.title("🗃️ Data Histórica Reportes Central Ñuñoa 2023-2024")

# Validación por seguridad
from auth import check_auth
if not check_auth():
    st.stop()

# Conexión
conn = st.connection("neon", type="sql")

# Función que controla errores
def consultar_df(consulta, parametros=None, intentos=2):
    """
    Ejecuta una consulta SQL y devuelve un DataFrame.
    Si falla la conexión, reintenta una vez.
    """
    conexion_db = st.connection("neon", type="sql")
    ultimo_error = None

    for intento in range(intentos):
        try:
            with conexion_db.engine.connect() as conexion:
                return pd.read_sql_query(
                    consulta,
                    conexion,
                    params=parametros or {}
                )

        except (SQLAlchemyError, pd.errors.DatabaseError) as error:
            ultimo_error = error

            if intento < intentos - 1:
                try:
                    conexion_db.reset()
                except Exception:
                    pass

                time.sleep(2)

    st.error(
        "No pudimos conectar con la base de datos. "
        "Es posible que esté iniciándose después de un período "
        "de inactividad. Espera unos segundos e inténtalo nuevamente."
    )

    with st.expander("Detalles técnicos"):
        st.code(str(ultimo_error))

    if st.button("Reintentar conexión", key="reintentar_neon"):
        st.rerun()

    st.stop()

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

    resultado = consultar_df(consulta)

    return resultado[columna].tolist()

@st.cache_data(ttl=3600)
def obtener_rango_fechas(_conn):
    consulta = text("""
        SELECT MIN(fecha) AS fecha_min,
               MAX(fecha) AS fecha_max
        FROM public.historico
    """)
    resultado = consultar_df(consulta)

    return resultado.iloc[0]["fecha_min"], resultado.iloc[0]["fecha_max"]

# Filtros
st.caption("Filtros")


fecha_desde = None
fecha_hasta = None

fecha_min, fecha_max = obtener_rango_fechas(conn)

if pd.notna(fecha_min) and pd.notna(fecha_max):
    fecha_min = pd.Timestamp(fecha_min).date()
    fecha_max = pd.Timestamp(fecha_max).date()

    c1, c2 = st.columns(2)
    with c1:
        fecha_desde = st.date_input(
            "Fecha de inicio",
            value=fecha_min,
            min_value=fecha_min,
            max_value=fecha_max,
            key="fecha_inicio"
        )
    with c2:
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

c3, c4, c5, c6 = st.columns(4)
with c3:
    categoria = opciones_filtro("categoria", "Categoría")

with c4:
    tipo = opciones_filtro(
    "tipo_de_procedimiento", "Tipo de procedimiento"
)
with c5:
    cuadrante = opciones_filtro("cuadrante", "Cuadrante")
with c6:
    canal = opciones_filtro("canal_de_ingreso", "Canal de ingreso")

busqueda = st.text_input(
    "Buscar texto",
    placeholder="Dirección, calle, descripción..."
)

condiciones = []
parametros = {}

if fecha_desde and fecha_hasta:
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
            OR informe ILIKE :busqueda
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

resultado_conteo = consultar_df(
    sql_conteo,
    parametros
)
total = int(resultado_conteo.iloc[0, 0])

# --------------------------------------------------
# PAGINACIÓN
# --------------------------------------------------

st.subheader(f"Resultados: {total:,}")

# tamano_pagina = st.selectbox(
#     "Registros por página",
#     [50, 100, 250, 500],
#     index=1
# )
tamano_pagina = 250

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
        nro "Nro.",
        fecha AS "Fecha",
        hora AS "Hora",
        categoria AS "Categoría",
        tipo_de_procedimiento AS "Tipo de Procedimiento",
        descripcion_del_procedimiento AS "Descripción",
        cuadrante AS "Cuadrante",
        canal_de_ingreso AS "Canal de Ingreso",
        estado_del_procedimiento AS "Estado del Procedimiento",
        informe AS "Informe"
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

df = consultar_df(
    sql_datos,
    parametros_pagina
)

st.dataframe(
    df,
    width='stretch',
    hide_index=True,
    height=600
)