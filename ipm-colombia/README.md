# IPM Colombia — Dashboard de Pobreza Multidimensional

Dashboard interactivo para explorar el **Índice de Pobreza Multidimensional (IPM)** por departamento en Colombia, construido con Python, Dash y Plotly.

**Fuente de datos:** DANE · Encuesta de Calidad de Vida (ECV) 2018–2025

---

## Vista previa

El dashboard incluye:
- Mapa coroplético interactivo por departamento
- Tarjeta "Si Colombia fueran 100 personas" con privaciones seleccionables
- Comparativa de brechas campo–ciudad con sombreado visual
- Ranking horizontal de departamentos más afectados
- IPM promedio por región geográfica (Amazonía-Orinoquía, Caribe, Pacífica, Central, Oriental, Bogotá D.C.)
- Evolución histórica 2018–2025 filtrable por departamento
- Brecha de género por sexo del jefe de hogar

---

## Instalación

### 1. Clona el repositorio

```bash
git clone https://github.com/Dmgar/ipm-colombia.git
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

> Los archivos de datos **no se incluyen** en el repositorio por su tamaño y licencia. Ver sección de datos abajo.

---

## Datos necesarios

Coloca todos los archivos en la carpeta `data/` del proyecto:

```
data/
├── MGN2024_DPTO_POLITICO.zip   ← descargar manualmente del DANE
├── ipm_dpto.csv
├── ipm_indicadores_dpto.csv
└── ipm_sexo_dpto.csv
```

### Geometría departamental
- **Archivo:** `MGN2024_DPTO_POLITICO.zip`
- **Fuente:** [DANE — Marco Geoestadístico Nacional 2024](https://geoportal.dane.gov.co/servicios/descarga-y-metadatos/datos-geoestadisticos/)
- **Formato:** Shapefile comprimido en ZIP

### Datos IPM por departamento (`ipm_dpto.csv`)
- **Fuente:** DANE — ECV (Encuesta de Calidad de Vida)
- **Columnas requeridas:**

| Columna       | Tipo   | Descripción                                      |
|---------------|--------|--------------------------------------------------|
| `nombre_dpto` | str    | Nombre del departamento                          |
| `cod_dpto`    | str    | Código DANE del departamento (2 dígitos, con 0 inicial) |
| `Año`         | int    | Año de la medición                               |
| `Categoria`   | str    | `Total`, `Cabeceras`, `Centros poblados y rural disperso` |
| `IPM`         | float  | Valor del índice (porcentaje)                    |

### Datos de indicadores de privación (`ipm_indicadores_dpto.csv`)
Desagregación de las 15 privaciones del IPM por departamento, año y zona.

### Datos por sexo (`ipm_sexo_dpto.csv`)
IPM desagregado por sexo del jefe de hogar, para el análisis de brecha de género.

---

## Ejecución

```bash
python mapa_agua.py
```

Abre tu navegador en: **http://127.0.0.1:8050**

---

## Regiones incluidas

| Región                    | Departamentos                                             |
|---------------------------|-----------------------------------------------------------|
| Amazonía-Orinoquía        | Amazonas, Guainía, Guaviare, Vaupés, Vichada, Meta, Casanare, Arauca |
| Caribe                    | Atlántico, Bolívar, Cesar, Córdoba, La Guajira, Magdalena, Sucre, San Andrés |
| Pacífica                  | Chocó, Cauca, Nariño, Valle del Cauca                    |
| Central                   | Antioquia, Caldas, Caquetá, Huila, Putumayo, Quindío, Risaralda, Tolima |
| Oriental                  | Boyacá, Cundinamarca, Norte de Santander, Santander       |
| Bogotá D.C.               | Bogotá D.C.                                               |

---

## Tecnologías

| Librería     | Versión  | Uso                              |
|--------------|----------|----------------------------------|
| Dash         | 4.1.0    | Framework web interactivo        |
| Plotly       | 6.7.0    | Gráficas y mapa coroplético      |
| Pandas       | 3.0.1    | Procesamiento de datos           |
| GeoPandas    | 1.1.3    | Lectura de geometría espacial    |
| NumPy        | 2.4.3    | Cálculos numéricos               |
| Gunicorn     | 23.0.0   | Servidor WSGI para deploy        |

---

## Licencia

Datos: © DANE Colombia. Código: MIT License.
