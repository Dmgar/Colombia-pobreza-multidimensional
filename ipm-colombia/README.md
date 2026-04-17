# IPM Colombia — Dashboard de Pobreza Multidimensional

Dashboard interactivo para explorar el **Índice de Pobreza Multidimensional (IPM)** por departamento en Colombia, construido con Python, Dash y Plotly.

**Fuente de datos:** DANE · Encuesta de Calidad de Vida (ECV) 2018–2025

---

## Vista previa

El dashboard incluye:
- Mapa coroplético interactivo por departamento
- Comparativa de brechas campo–ciudad
- Ranking horizontal de departamentos más afectados
- IPM promedio por región geográfica (Amazonía-Orinoquía, Caribe, Pacífica, Central, Oriental, Bogotá D.C.)
- Gráfica de cambio año a año en formato horizontal legible

---

## Instalación

### 1. Clona el repositorio

```bash
git clone https://github.com/TU_USUARIO/ipm-colombia.git
cd ipm-colombia
```

### 2. Crea un entorno virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

---

 Los archivos de datos **no se incluyen** en el repositorio por su tamaño y licencia. Ver sección de datos abajo.

---

## Datos necesarios

### Geometría departamental
- **Archivo:** `MGN2024_DPTO_POLITICO.zip`
- **Fuente:** [DANE — Marco Geoestadístico Nacional 2024](https://geoportal.dane.gov.co/servicios/descarga-y-metadatos/datos-geoestadisticos/)
- **Formato:** Shapefile comprimido en ZIP

### Datos IPM
- **Archivo:** `ipm_dpto.csv`
- **Fuente:** DANE — ECV (Encuesta de Calidad de Vida)
- **Columnas requeridas:**

| Columna       | Tipo   | Descripción                                      |
|---------------|--------|--------------------------------------------------|
| `nombre_dpto` | str    | Nombre del departamento                          |
| `cod_dpto`    | str    | Código DANE del departamento (2 dígitos, con 0 inicial) |
| `Año`         | int    | Año de la medición                               |
| `Categoria`   | str    | `Total`, `Cabecera`, `Centros poblados y rural disperso` |
| `IPM`         | float  | Valor del índice (porcentaje)                    |

---

## Configuración de rutas

Antes de ejecutar, edita las rutas en `app.py` según tu sistema:

```python
# app.py — líneas 14-15
GEO_PATH = r"C:\ruta\a\MGN2024_DPTO_POLITICO.zip"
CSV_PATH = r"C:\ruta\a\ipm_dpto.csv"
```

---

## Ejecución

```bash
python app.py
```

Abre tu navegador en: **http://127.0.0.1:8050**

---

##  Regiones incluidas

| Región                    | Departamentos                                             |
|---------------------------|-----------------------------------------------------------|
| Amazonía-Orinoquía        | Amazonas, Guainía, Guaviare, Vaupés, Vichada, Meta, Casanare, Arauca |
| Caribe                    | Atlántico, Bolívar, Cesar, Córdoba, La Guajira, Magdalena, Sucre, San Andrés |
| Pacífica                  | Chocó, Cauca, Nariño, Valle del Cauca                    |
| Central                   | Antioquia, Caldas, Caquetá, Huila, Putumayo, Quindío, Risaralda, Tolima |
| Oriental                  | Boyacá, Cundinamarca, Norte de Santander, Santander       |
| Bogotá D.C. (Cabecera)    | Bogotá D.C.                                               |

---

## Tecnologías

| Librería     | Versión  | Uso                              |
|--------------|----------|----------------------------------|
| Dash         | 2.18.2   | Framework web interactivo        |
| Plotly       | 5.24.1   | Gráficas y mapa coroplético      |
| Pandas       | 2.2.3    | Procesamiento de datos           |
| GeoPandas    | 1.0.1    | Lectura de geometría espacial    |

---

##  Licencia

Datos: © DANE Colombia. Código: MIT License.
