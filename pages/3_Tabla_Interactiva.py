## SIRAM ##
from __future__ import annotations
import unicodedata
from datetime import date, datetime
from io import BytesIO
from pathlib import Path
from typing import Callable, Union
import pandas as pd
import warnings
from openpyxl import load_workbook
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from openpyxl.worksheet.cell_range import CellRange
###########

from datetime import datetime
import streamlit as st
import pandas as pd



## Configuración inicial aplicación ##
st.set_page_config(page_title="Tabla Interactiva", layout="wide")
st.logo("./logo.png",size='large',icon_image="./logo.png")
st.title("🗃️ Tablas Reportes Central Ñuñoa 2026")

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
    if st.button("Dashboard", key="nav_dash", width='stretch'):
        st.switch_page("pages/2_Dashboard.py")

with col4:
    if st.button("Tabla Interactiva", key="nav_tabla", width='stretch', type="primary"):
        st.switch_page("pages/3_Tabla_Interactiva.py")

with col5:
    if st.button("Exportar Reportes", key="nav_report", width='stretch'):
        st.switch_page("pages/4_Exportar_Reportes.py")

with col6:
    if st.button("Comparador Períodos", key='nav_comp', width='stretch'):
        st.switch_page("pages/5_Graficas_Comparativas.py")
st.markdown("---")
## Información sobre la data comprendida en la aplicación ##
dfr = pd.read_csv('info.csv', sep=';', engine='python')
dfr['FECHA Y HORA'] = pd.to_datetime(dfr['FECHA Y HORA'])
first_hist = dfr.iloc[0]['FECHA Y HORA']
last_hist = dfr.iloc[-1]['FECHA Y HORA']
st.markdown(f"Información integrada desde **{first_hist}** a **{last_hist}**")


## Enlisto los filtros ##
st.subheader("Filtros")
op_ingreso = ['1445', 'EXTERNO','INTERNO','JEFATURA','OPERADOR CÁMARAS','PROALERT','SOSAFE','OTROS', 'VECINO/A']
op_cuadrantes = ['Nro. 118','Nro. 119','Nro. 120','Nro. 121','Nro. 129','Nro. 130','Nro. 131','Nro. 132','Nro. 133','No aplica']
dop_categoria ={'Seguridad':['Servicio DRONE','Apoyo a Carabineros','Actividad sospechosa','Agresión','Alarma activada','Amenazas','Artefacto explosivo o paquete sospechoso','Daños propiedad privada','Daños propiedad pública','Delito sexual','Detención ciudadana','Detenidos','Disparos','Disturbios','Fuegos artificiales','Homicidio','Homicidio Frustrado','Hurto','Maltrato animal','Marchas/manifestaciones','Persona extraviada / desorientada','Posible sospechoso al interior','Riña','Robo con intimidación','Robo con violencia','Robo de especies de o desde vehículo','Robo de vehículo en BNUP','Robo en BNUP','Robo en lugar habitado','Robo en lugar no habitado','Robo frustrado','Robo por sorpresa','Toma establecimiento educacional','Trafico Drogas','Vehículo con encargo','Vehiculo sospechoso','Incumplimiento medida cautelar','VIF','Vulneración derechos adultos mayores','Vulneración NNA','Otros','Motochorros '],
                 'Planes Operativos':['7X3 delitos violentos','Control de Transito','Operativo Conjunto a otras Municipalidades','Operativo Conjunto Carabineros','Operativo conjunto Delegación Presidencial','Operativo conjunto Dirección de Inspección','Operativo MTT','Operativo otras direcciones Municilapales','Operativo Seremi Salud','Operativos Conjunto PDI','P.V.P','Patrulla Mixta','Patrullaje focalizado Carabineros','Patrullaje focalizado Preventivo','Patrullaje preventivo general','Punto fijo','Ruta calle','Servicio especial Colegios','Servicio Estadio','Servicio FEI','Servicio turístico Plaza Ñuñoa-Barrio Italia','Vigilancia especial','Otros'],
                 'Emergencia/Espacio Públicos':['Apoyo a Bomberos','Apoyo a SAMU','Accidente de tránsito (choque/colisión/atropello)','Acera en mal estado','Alcantarilla colapsada','Anegamiento de calle y paso bajo nivel','Anegamiento domicilios','Suicidio/Intento','Cables a baja altura / Cables cortados','Caida de arbol','Circuito y luminarias dañadas','Corte energía eléctrica','Corte suministro de agua potable','Desganche arbolado','Emanación de gas/ Derrame o Materiales peligrosos','Emergencia de salud','Filtración agua potable','Incendio o amago','Mascota atrapada/perdida','Pavimento en mal estado','Posible Fallecido/Emergencia de Salud','Postes dañados','Semáforo defectuoso','Señalética o elemento caida','Tapa de servicios','Otra contingencia BNUP','Otros'],
                 'Fiscalización':['Realizacion de Graffitis / Pintar sin autorización','Comercio ambulante Ilegal','Fiscalización alcoholes','Fiscalización aparcadores ilegales','Fiscalización de tránsito','Vehiculo MAL Estacionado','Vehículo sospechoso','Fiscalización ingesta de alcohol en vía pública','Fiscalizacion Retiro de circulación de vehiculo motorizado','Fiscalizacion Ruidos Molestos','Fiscalizaciones (BNUP, comercio, etc)','Trabajos fuera de horario','Vehículo abandonado','Otros'],
                 'Incivilidades':['Botar chicle, colillas o desechos en la vía pública','Carpa o Ruco en BNUP','Consumo de alcohol en vía pública','Consumo de drogas','Ebriedad','Microbasural','Persona situación de calle','Otros'],
                 'Otros':['Novedades Central','Labores administrativas','Traslado de documentos o funcionarios/limpieza de móvil','Otros']}
op_categoria = list(dop_categoria.keys())
op_tipo =['Servicio DRONE','Apoyo a Carabineros','Actividad sospechosa','Agresión','Alarma activada','Amenazas','Artefacto explosivo o paquete sospechoso','Daños propiedad privada','Daños propiedad pública','Delito sexual','Detención ciudadana','Detenidos','Disparos','Disturbios','Fuegos artificiales','Homicidio','Homicidio Frustrado','Hurto','Maltrato animal','Marchas/manifestaciones','Persona extraviada / desorientada','Posible sospechoso al interior','Riña','Robo con intimidación','Robo con violencia','Robo de especies de o desde vehículo','Robo de vehículo en BNUP','Robo en BNUP','Robo en lugar habitado','Robo en lugar no habitado','Robo frustrado','Robo por sorpresa','Toma establecimiento educacional','Trafico Drogas','Vehículo con encargo','Vehiculo sospechoso','Incumplimiento medida cautelar','VIF','Vulneración derechos adultos mayores','Vulneración NNA','Otros','Motochorros ','7X3 delitos violentos','Control de Transito','Operativo Conjunto a otras Municipalidades','Operativo Conjunto Carabineros','Operativo conjunto Delegación Presidencial','Operativo conjunto Dirección de Inspección','Operativo MTT','Operativo otras direcciones Municilapales','Operativo Seremi Salud','Operativos Conjunto PDI','P.V.P','Patrulla Mixta','Patrullaje focalizado Carabineros','Patrullaje focalizado Preventivo','Patrullaje preventivo general','Punto fijo','Ruta calle','Servicio especial Colegios','Servicio Estadio','Servicio FEI','Servicio turístico Plaza Ñuñoa-Barrio Italia','Vigilancia especial','Otros','Apoyo a Bomberos','Apoyo a SAMU','Accidente de tránsito (choque/colisión/atropello)','Acera en mal estado','Alcantarilla colapsada','Anegamiento de calle y paso bajo nivel','Anegamiento domicilios','Suicidio/Intento','Cables a baja altura / Cables cortados','Caida de arbol','Circuito y luminarias dañadas','Corte energía eléctrica','Corte suministro de agua potable','Desganche arbolado','Emanación de gas/ Derrame o Materiales peligrosos','Emergencia de salud','Filtración agua potable','Incendio o amago','Mascota atrapada/perdida','Pavimento en mal estado','Posible Fallecido/Emergencia de Salud','Postes dañados','Semáforo defectuoso','Señalética o elemento caida','Tapa de servicios','Otra contingencia BNUP','Otros','Realizacion de Graffitis / Pintar sin autorización','Comercio ambulante Ilegal','Fiscalización alcoholes','Fiscalización aparcadores ilegales','Fiscalización de tránsito','Vehiculo MAL Estacionado','Vehículo sospechoso','Fiscalización ingesta de alcohol en vía pública','Fiscalizacion Retiro de circulación de vehiculo motorizado','Fiscalizacion Ruidos Molestos','Fiscalizaciones (BNUP, comercio, etc)','Trabajos fuera de horario','Vehículo abandonado','Otros','Botar chicle, colillas o desechos en la vía pública','Carpa o Ruco en BNUP','Consumo de alcohol en vía pública','Consumo de drogas','Ebriedad','Microbasural','Persona situación de calle','Otros','Novedades Central','Labores administrativas','Traslado de documentos o funcionarios/limpieza de móvil','Otros','Patrullaje preventivo', 'Focalizado municipal', 'Fiscalización conjunta (Carabineros, PDI)', 'Operativos conjuntos: colaboración con Carabineros, PDI', 'Fiscalización', 'Ruidos Molestos', 'Retiro de enseres de la via publica', 'Seguridad (prevención)', 'Seguridad']
op_hinicio = {0:'00:00',1:'01:00',2:'02:00',3:'03:00',4:'04:00',5:'05:00',6:'06:00',7:'07:00',8:'08:00',9:'09:00',10:'10:00',11:'11:00',12:'12:00',13:'13:00',14:'14:00',15:'15:00',16:'16:00',17:'17:00',18:'18:00',19:'19:00',20:'20:00',21:'21:00',22:'22:00',23:'23:00',24:'24:00'}
op_hfinal = {0:'00:00',1:'01:00',2:'02:00',3:'03:00',4:'04:00',5:'05:00',6:'06:00',7:'07:00',8:'08:00',9:'09:00',10:'10:00',11:'11:00',12:'12:00',13:'13:00',14:'14:00',15:'15:00',16:'16:00',17:'17:00',18:'18:00',19:'19:00',20:'20:00',21:'21:00',22:'22:00',23:'23:00', 24:'24:00'}
op_mes = {1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'}
op_ano = [2020,2021,2022,2023,2024,2025,2026]
op_comisaria = ['33° Comisaría','18° Comisaría','No hubo','NO APLICA']
opi_hinicio = list(op_hinicio.items())
opi_hfinal = list(op_hfinal.items())
opi_mes = list(op_mes.items())
col1, col2, col3, col4, col5 = st.columns(5)
col6, col7, col8, col9, col10 = st.columns(5)
with col1:
    ingreso = st.multiselect("Vía de Ingreso", op_ingreso,placeholder='Elige')
with col2:
    cuadrante = st.multiselect("Cuadrante", op_cuadrantes, placeholder='Elige')
with col3:
    categoria = st.selectbox("Categoría", op_categoria, index=None,placeholder='Elige')
with col4:
    if categoria:
        ltipo = dop_categoria[categoria]
        tipo = st.multiselect("Tipo", ltipo,placeholder='Elige')
    else:
        tipo = st.multiselect("Tipo", op_tipo,placeholder='Elige')
with col5:
    shinicio = st.selectbox("Hora Inicio",options=opi_hinicio,format_func=lambda o: o[1], index=None, placeholder='Elige')
    if shinicio:
        hinicio = shinicio[0]
    else:
        hinicio = None
with col6:
    shfinal = st.selectbox("Hora Final",options=opi_hfinal,format_func=lambda o: o[1], index=None, placeholder='Elige')
    if shfinal:
        hfinal = shfinal[0]
    else:
        hfinal = None
with col7:
    smes = st.selectbox("Mes",options=opi_mes,format_func=lambda o: o[1], index=None, placeholder='Elige')
    if smes:
        mes = smes[0]
    else:
        mes = None
with col8:
    ano = st.selectbox("Año", op_ano, index=None,placeholder='Elige')
with col9:
    finicio = st.date_input("Desde", value=None)
with col10:
    ffinal = st.date_input("Hasta", value=None)
col11, col12, col13, col14, col15 = st.columns(5)
with col11:
    calle = st.text_input("Calle",'',placeholder="Elige")
with col12:
    numeracion = st.text_input("Numeración",'',placeholder="Elige")
with col13:
    palabra = st.text_input("Palabra Clave",'',placeholder="Elige")
with col14:
    comisaria = st.selectbox("Comisaría", op_comisaria, index=None,placeholder='Elige')

## Cargo el archivo .csv ##
df = pd.read_csv('info.csv', sep=';', engine='python')
df_filtrado = df.copy()
df_filtrado['FECHA Y HORA'] = pd.to_datetime(df_filtrado['FECHA Y HORA'])

## Filtro la base de datos ##
if ingreso:
    df_filtrado = df_filtrado[df_filtrado['CANAL DE INGRESO'].isin(ingreso)]
if cuadrante:
     df_filtrado = df_filtrado[df_filtrado['CUADRANTE'].isin(cuadrante)]
if categoria:
    df_filtrado = df_filtrado[df_filtrado['CATEGORIA'] == categoria]
if tipo:
    df_filtrado = df_filtrado[df_filtrado['TIPO DE PROCEDIMIENTO'].isin(tipo)]
if mes:
    df_filtrado = df_filtrado[df_filtrado['FECHA Y HORA'].dt.month == mes]
if ano:
    df_filtrado = df_filtrado[df_filtrado['FECHA Y HORA'].dt.year == ano]
if hinicio and hfinal and hinicio > hfinal:
    df_filtrado = df_filtrado[(df_filtrado['FECHA Y HORA'].dt.hour >= hinicio) | (df_filtrado['FECHA Y HORA'].dt.hour < hfinal)]
if hinicio and hfinal and hinicio < hfinal:
    df_filtrado = df_filtrado[(df_filtrado['FECHA Y HORA'].dt.hour >= hinicio) & (df_filtrado['FECHA Y HORA'].dt.hour < hfinal)]
if hinicio and not hfinal:
    df_filtrado = df_filtrado[df_filtrado['FECHA Y HORA'].dt.hour >= hinicio]
if hfinal and not hinicio:
    df_filtrado = df_filtrado[df_filtrado['FECHA Y HORA'].dt.hour < hfinal]
if finicio:
    df_filtrado = df_filtrado[df_filtrado['FECHA Y HORA'].dt.date >= finicio]
if ffinal:
    df_filtrado = df_filtrado[df_filtrado['FECHA Y HORA'].dt.date <= ffinal]
if calle:
    df_filtrado = df_filtrado[df_filtrado['CALLE'].str.contains(calle, case=False, na=False) | df_filtrado['CALLE QUE INTERSECTA'].str.contains(calle, case=False, na=False)]
if numeracion:
    df_filtrado = df_filtrado[df_filtrado['NUMERACIÓN'].str.contains(numeracion, case=False, na=False)]
if palabra:
    df_filtrado = df_filtrado[df_filtrado['INFORME'].str.contains(palabra, case=False, na=False) | df_filtrado['DESCRIPCION DEL PROCEDIMIENTO (DETALLES RELEVANTES)'].str.contains(palabra, case=False, na=False)]
if comisaria:
    df_filtrado = df_filtrado[df_filtrado['COMISARIA'] == comisaria]

## RESALTAR ##
def highlight(val):
    if palabra and palabra.lower() in str(val).lower():
        return "background-color: yellow"
    return ""


## Muestro el resultado en una tabla ##
st.subheader("Resultados")
st.write(f"Total de registros: {len(df_filtrado)}")
#st.dataframe(df_filtrado[df_filtrado.columns[2:26]], width='stretch')
#st.dataframe(df_estilado,width='stretch')

## PAGINACION ##
#entradas_por_pagina = st.selectbox("Por página:", [10, 25, 50, 100])
entradas_por_pagina = 250
pagina = st.number_input("Página:", 1, max(1, (len(df_filtrado) // entradas_por_pagina) + 1))
inicio = (pagina - 1) * entradas_por_pagina
fin = inicio + entradas_por_pagina
if palabra:
    df_estilado = df_filtrado.iloc[inicio:fin].style.map(highlight)
    st.dataframe(df_estilado, width='stretch')
if not palabra:
    df_estilado = df_filtrado
    st.dataframe(df_estilado.iloc[inicio:fin], width='stretch')
st.write(f"Página {pagina} de {(len(df_filtrado) // entradas_por_pagina) + 1}")

## SIRAM ##
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
# Ruta de la plantilla (misma carpeta que este archivo). Ajusta el nombre.
RUTA_PLANTILLA = Path(__file__).parent / "plantilla_siram.xlsx"

FORMATO_FECHA_EXCEL = "DD-MM-YYYY"
LARGO_MAXIMO_CELDA = 32767  # límite de caracteres por celda en Excel


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def _normalizar(texto) -> str:
    """Para comparar nombres: ignora mayúsculas, tildes y espacios repetidos."""
    sin_tildes = "".join(
        c for c in unicodedata.normalize("NFKD", str(texto)) if not unicodedata.combining(c)
    )
    return " ".join(sin_tildes.split()).upper()


def _col(df: pd.DataFrame, nombre: str) -> pd.Series:
    """Devuelve la columna del CSV cuyo nombre coincide (normalizado) con 'nombre'."""
    buscado = _normalizar(nombre)
    for real in df.columns:
        if _normalizar(real) == buscado:
            return df[real]
    raise KeyError(
        f"La columna '{nombre}' no existe en el CSV. Columnas disponibles: {list(df.columns)}"
    )


# ---------------------------------------------------------------------------
# Transformaciones: cada una recibe el DataFrame y devuelve una Serie
# ---------------------------------------------------------------------------
def fecha_desde(columna: str) -> Callable[[pd.DataFrame], pd.Series]:
    """'25-12-2025 14:30' -> fecha real 25-12-2025 (sin hora)."""

    def _transformar(df: pd.DataFrame) -> pd.Series:
        texto = _col(df, columna).astype(str).str.strip()
        fechas = pd.to_datetime(texto, format="%Y-%m-%d %H:%M:%S", errors="coerce")
        # Por si alguna fila viene sin hora ('25-12-2025')
        fechas = fechas.fillna(pd.to_datetime(texto, format="%Y-%m-%d", errors="coerce"))
        return fechas.dt.date

    return _transformar


def _separar_coordenadas(df: pd.DataFrame, columna: str) -> pd.DataFrame:
    """'-33.4372,-70.6506' -> columnas 0 (latitud) y 1 (longitud) numéricas."""
    partes = (
        _col(df, columna).astype(str).str.split(",", n=1, expand=True).reindex(columns=[0, 1])
    )
    return partes.apply(lambda s: pd.to_numeric(s.str.strip(), errors="coerce"))


def latitud_desde(columna: str) -> Callable[[pd.DataFrame], pd.Series]:
    return lambda df: _separar_coordenadas(df, columna)[0]


def longitud_desde(columna: str) -> Callable[[pd.DataFrame], pd.Series]:
    return lambda df: _separar_coordenadas(df, columna)[1]


def constante(valor) -> Callable[[pd.DataFrame], pd.Series]:
    """Mismo valor en todas las filas (para datos que no vienen en el CSV)."""
    return lambda df: pd.Series([valor] * len(df), index=df.index)


# ---------------------------------------------------------------------------
# MAPEO  ->  {hoja: {"fila_encabezado": n, "columnas": {col_plantilla: origen}}}
#
#   origen puede ser:
#     - str       -> nombre de la columna del CSV, se copia tal cual
#     - callable  -> función(df) -> Serie, para columnas que se transforman
#
# Las columnas de la plantilla que NO aparecen aquí quedan vacías.
# Los nombres (de plantilla y de CSV) se comparan sin importar mayúsculas,
# tildes ni espacios repetidos, y el orden de las columnas da lo mismo.
# ---------------------------------------------------------------------------
MAPEO = {
    "INFORMACION DELICTUAL": {
        "fila_encabezado": 1,
        "columnas": {
            "nombre_documento": "ID ASIGNADO /TICKET",
            "fec_documento": fecha_desde("FECHA Y HORA"),  # YYYY-MM-DD HH:MM:SS -> YYYY-MM-DD
            "detalle": "INFORME",
        },
    },
    "DIRECCIONES": {
        "fila_encabezado": 1,
        "columnas": {
            "nombre_documento": "ID ASIGNADO /TICKET",  # mismo vínculo que la otra hoja
            "calle": "CALLE",
            "numero": "NUMERACIÓN",
            # "depto" no se mapea: queda vacío en la plantilla
            "comuna": constante("Ñuñoa"),  # siempre la misma
            "latitud": latitud_desde("COORDENADAS"),  # 'lat,lon' -> lat
            "longitud": longitud_desde("COORDENADAS"),  # 'lat,lon' -> lon
            # "tipo_direccion" no se mapea: queda vacío en la plantilla
        },
    },
}

Origen = Union[str, Callable[[pd.DataFrame], pd.Series]]


# ---------------------------------------------------------------------------
# Escritura
# ---------------------------------------------------------------------------
def _escribir_hoja(ws, df: pd.DataFrame, columnas: dict[str, Origen], fila_encabezado: int) -> None:
    # 1) Ubicar columnas de la plantilla por el nombre del encabezado
    encabezados = {
        _normalizar(c.value): c.column for c in ws[fila_encabezado] if c.value is not None
    }
    faltantes = [h for h in columnas if _normalizar(h) not in encabezados]
    if faltantes:
        raise ValueError(
            f"Hoja '{ws.title}': no encontré las columnas {faltantes} en la fila "
            f"{fila_encabezado}. Encabezados presentes: {list(encabezados)}"
        )
    indice = {h: encabezados[_normalizar(h)] for h in columnas}

    # 2) Calcular los datos de salida (copia directa o transformación)
    datos = {}
    for h, origen in columnas.items():
        serie = origen(df) if callable(origen) else _col(df, origen)
        datos[h] = serie.reset_index(drop=True)
    salida = pd.DataFrame(datos)

    # 3) Limpiar valores previos (solo en las columnas mapeadas; conserva estilos)
    primera = fila_encabezado + 1
    for fila in range(primera, ws.max_row + 1):
        for col in indice.values():
            ws.cell(row=fila, column=col).value = None

    # 4) Escribir fila por fila
    for fila, valores in enumerate(salida.itertuples(index=False), start=primera):
        for h, v in zip(salida.columns, valores):
            if pd.isna(v):
                v = None
            elif hasattr(v, "item"):  # tipos numpy -> tipos nativos de Python
                v = v.item()
            if isinstance(v, str):
                # Texto libre: quitar caracteres de control que Excel no admite
                # y respetar el largo máximo de celda
                v = ILLEGAL_CHARACTERS_RE.sub("", v)[:LARGO_MAXIMO_CELDA]
            celda = ws.cell(row=fila, column=indice[h], value=v)
            if isinstance(v, (date, datetime)):
                celda.number_format = FORMATO_FECHA_EXCEL
            elif isinstance(v, str) and v.startswith("="):
                celda.data_type = "s"  # que Excel no lo interprete como fórmula

    # 5) Si la hoja usa una "Tabla de Excel", extender su rango a los nuevos datos
    ultima = max(primera + len(salida) - 1, primera)
    for tabla in ws.tables.values():
        rango = CellRange(tabla.ref)
        if rango.min_row == fila_encabezado:
            rango.max_row = ultima
            tabla.ref = rango.coord
            if tabla.autoFilter is not None:
                tabla.autoFilter.ref = rango.coord


def generar_excel(df_filtrado: pd.DataFrame, ruta_plantilla: Path | str = RUTA_PLANTILLA) -> bytes:
    """Carga la plantilla, la rellena con df_filtrado y devuelve el .xlsx en bytes."""
    wb = load_workbook(ruta_plantilla)  # las demás hojas quedan intactas
    for nombre_hoja, cfg in MAPEO.items():
        if nombre_hoja not in wb.sheetnames:
            raise KeyError(f"La plantilla no tiene la hoja '{nombre_hoja}'. Hojas: {wb.sheetnames}")
        _escribir_hoja(wb[nombre_hoja], df_filtrado, cfg["columnas"], cfg["fila_encabezado"])

    buffer = BytesIO()
    wb.save(buffer)
    return buffer.getvalue()
###########
st.download_button(
    "Exportar SIRAM",
    data=generar_excel(df_filtrado),
    file_name="informacion_filtrada.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)