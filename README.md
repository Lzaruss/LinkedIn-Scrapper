# LinkedIn Scrapper - Documentación Técnica

## Descripción
Este proyecto, **LinkedIn Scrapper**, permite extraer datos de perfiles en LinkedIn utilizando técnicas de web scraping. Su enfoque principal es recopilar información estructurada como títulos, ubicaciones, y detalles profesionales, con funcionalidades avanzadas para normalizar y procesar los datos.

---

## Características
1. **Extracción de Datos**: 
   - Recupera información detallada de los perfiles, incluyendo nombre, título profesional y ubicación.

2. **Normalización**:
   - Estandariza los datos recolectados para asegurar consistencia.
   - Divide campos complejos como la ubicación en componentes manejables.

3. **Compatibilidad**:
   - Soporte para manejar múltiples versiones de la página web, usando bibliotecas como **BeautifulSoup** y **cloudscraper**.

---

## Requisitos
- **Python**: Versiones 3.8 o superior.
- Dependencias principales (se instalan desde `requirements.txt`):
  - `cloudscraper`
  - `BeautifulSoup`
  - `requests`

---

## Estructura del Repositorio
1. **`src/`**:
   - Contiene los scripts principales para el scraping y procesamiento de datos.
   
2. **`data/`**:
   - Almacena los datos extraídos en formato estructurado (JSON/CSV).

3. **`utils/`**:
   - Scripts auxiliares para funciones comunes como normalización de datos y manejo de errores.

4. **`requirements.txt`**:
   - Lista de dependencias necesarias.

5. **README.md**:
   - Información general del proyecto.

---

## Configuración
1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/Lzaruss/LinkedIn-Scrapper.git
   cd LinkedIn-Scrapper
