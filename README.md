# LinkedIn Scrapper - Documentación Técnica

## Descripción
Este proyecto, **LinkedIn Scrapper**, permite extraer datos de perfiles en LinkedIn utilizando técnicas de web scraping. Su finalidad principal es recopilar información estructurada como títulos, ubicaciones, y detalles profesionales, con funcionalidades avanzadas para normalizar y procesar los datos.

---

## Características
1. **Extracción de Datos**: 
   - Recupera información detallada de los perfiles, incluyendo nombre, título profesional y ubicación.

2. **Limpieza de datos**:
   - Limpieza de los datos recolectados para asegurar consistencia.
   - Divide campos complejos como la ubicación en componentes manejables.
   - Eliminación de caracteristicas especiales y emojis.

3. **Visualización**
   - Uso de mapamundi para ver la ubicación de cada contacto.
   - Matplotlib para el uso de gráficas.

---

## Estructura del Repositorio
1. **`src/`**:
   - Contiene los scripts principales para el scraping y procesamiento de datos.
   
2. **`data_folder/`**:
   - Almacena los datos extraídos en formato estructurado (JSON/CSV).
   - Variables de inicio de sesión.

---

## Uso del script

   - Establecemos las credenciales en el archivo secrets.yaml
   - Ejecutamos el main.py y esperamos a que se genere el archivo de connections_links.json
   - Para limpiar los datos ejecuta data_cleaner.py y el posterior analisis: data_analyzer.py (Este ultimo te generará unos gráficos que podrás descargar y un mapa html)