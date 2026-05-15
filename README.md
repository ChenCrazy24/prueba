Analizador de Datos CSV

Este proyecto es una solución desarrollada en Python para la lectura, validación, filtrado y resumen de archivos de datos estructurados. 
Tecnologías Utilizadas
Python: Lenguaje principal del desarrollo.
Tkinter: Librería nativa utilizada para crear una interfaz gráfica de usuario amigable e intuitiva.
SQLite3: Motor de base de datos relacional integrado nativamente para persistir el historial de los análisis de forma local y segura.
Unittest: Framework nativo para la ejecución de pruebas unitarias automatizadas.

Funcionalidades y Validaciones
El sistema procesa archivos .csv y realiza un riguroso control de calidad en tiempo real:
Validaciones Estructurales: Detección de archivos vacíos y comprobación de columnas obligatorias (Folio, Fecha, Categoria, Monto, Estatus).
Integridad de Datos: Detección de folios duplicados, validación estricta de formato de fechas (AAAA-MM-DD) y comprobación de tipos de datos en montos numéricos.
Filtrado Dinámico: Capacidad de filtrar los registros por Estatus y/o Categoría antes de procesar el resumen.

Características Extra Implementadas:
Almacenamiento en Base de Datos: Guarda automáticamente un histórico de ejecuciones exitosas (fecha, totales y JSON) en un archivo “historial_analisis.db”.
Exportación: Permite al usuario guardar el resumen JSON generado en un archivo local a través de la interfaz.
Pruebas Unitarias: Incluye un script de validación matemática automatizada para garantizar la exactitud de los cálculos.

Instrucciones de Ejecución

1. Iniciar la Aplicación Principal
Desde la terminal, ubicado en la raíz del proyecto, ejecuta:
“python analizador.py”
Se abrirá la interfaz gráfica. Puedes probar el sistema utilizando los diferentes escenarios incluidos en el repositorio:
caso_ideal.csv: Datos limpios para un flujo sin errores.
caso_errores.csv: Datos con errores intencionales para probar las validaciones.
caso_incompleto.csv: Archivo sin la estructura de encabezados correcta.

2. Ejecutar Pruebas Unitarias
Para verificar la integridad de las funciones mediante el entorno de pruebas, ejecuta:
“python test_analizador.py”

Decisiones Técnicas
Se optó por una interfaz gráfica con Tkinter en lugar de una aplicación pura de consola para entregar un producto más cercano a un entorno real de servicio al cliente, priorizando la usabilidad sin requerir instalaciones complejas de terceros.
Para cumplir con el almacenamiento en Base de Datos de manera eficiente, se utilizó SQLite. Esto elimina la fricción de configurar puertos o credenciales, permitiendo que la evaluación del código sea directa y sin configuraciones extra.
Visión a Futuro: Para escalar esta automatización, el siguiente paso sería separar el motor de análisis en una API REST y utilizar librerías como pandas para el manejo de volúmenes masivos de datos.
