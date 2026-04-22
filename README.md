# Aplicación visual procedimientos Ñuñoa
## Descripción
Herramienta visual para el análisis de procedimientos y reportes central Ñuñoa. Información integrada desde el 01/01/2025 al 21/04/2026.
## Acceso
Mediante el link: https://reportesnunoa.streamlit.app/
## Páginas
### Mapa Interactivo
Muestra los procedimientos por ubicación geo referenciada. El mapa muestra por defecto la comuna de Ñuñoa dividida por sus respectivos cuadrantes. Los puntos, además de ser representados en el mapa de forma individual, se muestra un mapa de calor que agrupa y muestra los sectores con mayor frecuencia de procedimientos. Para análisis más espécificos es posible usar la herramienta de selección de polígonos, que permite seleccionar ya sea un círculo, un rectangulo o un polígono personalizado, para poder obtener el desglose de esa área en específico. Al seleccionar cualquier figura de las antes mencionada se despliegan dos tablas adicionales (ambas exportables en formato .csv): una con el detalle de cada punto dentro del polígono, y otra que muestra el desglose agrupado por tipo de procedimiento.
### Dashboard
El dashboard sintetiza y agrupa la información de una forma de facil entendimiento. Se puede seleccionar un rango de fechas o por defecto se mostrará la totalidad de la información. Cuenta con distintas secciones divididas por el tipo de información que se muestra. Incluye una sección de métricas principales, análisis general, análisis temporal, desglose del total de procedimientos y análisis detallado. Todo lo que incluye esta sección es exportable en formato .PNG.
### Tabla Interactiva
Esta tabla contiene todas las entradas en las fechas integradas en la aplicación. Cuenta con múltiples filtros para una búsqueda eficiente y rápida. En cada momento muestra la cantidad de resultados encontrados y todas las tablas son exportables en formato .csv. Además de búsquedas por parámetros definidos (canal de ingreso, cuadrante, categoría, tipo de procedimiento, hora, día, mes, año) también incluye búsqueda por palabras clave en informes y reportes, como también de calles.
### Exportar Reportes
Esta sección genera un informe pdf con información relevante a partir de filtros que podrán ser seleccionados para acotar la búsqueda. Por defecto el informe se hará con toda la información existente, a no ser que se indique lo contrario. Se incluye la opción de seleccionar un título personalizado y al autor de dicho informe. En la portada se indica además el rango de fechas que comprende el informe, como la fecha en que el reporte fue generado. El informe incluye una tabla resumen con las métricas más relevantes, gráficos de barra y circulares, y tablas con un desglose más detallado de lo requerido.
### Gráficas Comparativas
Para períodos de tiempo donde hay información disponible de más de un año, en esta sección se podrá seleccionar ya sea por categoría, o por un grupo personalizado de procedemientos un rango de tiempo a analizar. Con lo anterior definido, se desplegarán: un gráfico de barras comparativo por año por cada tipo de procedimiento, un gráfico de línea para cada año donde se muestra el comportamiento diario de todos los procedimientos seleccionados, y finalmente una tabla con la información graficada previamente.

