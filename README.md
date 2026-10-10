# Colombia — Índice de Pobreza Multidimensional (IPM)

Dashboard interactivo para la exploración, visualización y análisis geoespacial del **Índice de Pobreza Multidimensional (IPM)** en los 33 departamentos de Colombia. Construido con **Python**, **Dash**, **Plotly** y **GeoPandas**.

**Fuente oficial de datos:** DANE · Encuesta Nacional de Calidad de Vida (ECV) 2018–2025.

---

## Características del Dashboard

- **Panorama General & Mapa Coroplético:** Visualización geográfica interactiva con las geometrías oficiales del Marco Geoestadístico Nacional (MGN 2024) optimizadas en GeoJSON.
- **Contexto Regional & Benchmarking OCDE/CEPAL (Nuevo):** Comparativa internacional de Colombia frente a 9 pares latinoamericanos (Chile, Costa Rica, México, Brasil, Perú, Ecuador, Uruguay, Bolivia, Argentina) y los promedios regionales de la CEPAL y la OCDE.
- **Radar Multidimensional de 5 Pilares:** Evaluación comparativa en Educación y Logro, Salud y Nutrición, Agua y Saneamiento, Vivienda Digna, y Trabajo/Protección Social.
- **Cuadrantes de Desarrollo (Pobreza vs Gini):** Gráfico interactivo que expone la ubicación de Colombia en el cuadrante de alta desigualdad de la OCDE y su trampa de movilidad intergeneracional (11 generaciones para salir de la pobreza).
- **Análisis de Impacto en Bienestar Poblacional:** Diagnósticos rigurosos sobre la pérdida irreversible de capital humano en la primera infancia (HCI 0.60), el dualismo productivo por informalidad (>55% nacional, >80% rural) y la economía del cuidado no remunerado.
- **Simulador Didáctico de Políticas:** Proyección de reducción del IPM y ganancias en capital humano al universalizar agua rural o formalizar el empleo.
- **Brecha Campo–Ciudad:** Comparación directa entre cabeceras municipales y centros poblados / rural disperso con filtros dinámicos por zona, brecha neta y sentido.
- **Indicadores de Privación:** Módulo con selector de las 15 dimensiones de privación del IPM (acceso a agua, analfabetismo, saneamiento básico, empleo informal, salud, etc.) y dinámica "Si Colombia fueran 100 personas".
- **Ranking Departamental:** Vista horizontal de los departamentos con mayores y menores niveles de privación clasificados por región.
- **Evolución Temporal:** Análisis de series de tiempo (2018–2025) a nivel nacional y por departamento.
- **Brecha por Género:** Análisis comparativo de la incidencia de pobreza según el sexo del jefe de hogar (Hombre vs. Mujer).

---

## Estructura del Proyecto

```text
Colombia-pobreza-multidimensional/
├── .gitignore                      # Exclusión de entornos, cachés y archivos de datos
├── LICENSE                         # Licencia MIT
├── README.md                       # Documentación principal del repositorio
└── ipm-colombia/
    ├── app.py                      # Punto de entrada principal del dashboard
    ├── mapa_agua.py                # Implementación central del layout y callbacks Dash
    ├── contexto_regional.py        # Módulo de benchmarking latinoamericano y análisis OCDE/CEPAL
    ├── ui.py                       # Componentes reutilizables de UI y paletas editoriales
    ├── figuras.py                  # Generadores de gráficos y estilos de Plotly
    ├── requirements.txt            # Dependencias del proyecto (Dash, Plotly, PyShp, Shapely)
    ├── data/                       # Carpeta local de datos
    │   ├── colombia_dpto_simplified.geojson # Geometrías vectoriales optimizadas (552 KB)
    │   └── .gitkeep
    └── limpieza/                   # Scripts y notebooks de preparación de datos
        ├── README.md               # Documentación del pipeline de limpieza
        ├── procesar_datos.py       # Script automatizado para procesar el Excel del DANE
        └── limpieza de datos.ipynb # Notebook exploratorio de transformación
```

---

## Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/Dmgar/Colombia-pobreza-multidimensional.git
cd Colombia-pobreza-multidimensional/ipm-colombia
```

### 2. Crear y activar entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Datos y Procesamiento

Por políticas de licencia y tamaño, los archivos de datos **no se incluyen en el repositorio** y están excluidos mediante `.gitignore`.

### 1. Descarga de insumos oficiales

Coloca los siguientes archivos en la carpeta `ipm-colombia/data/`:

1. **Shapefile Departamental (Geometrías):**
   - Archivo: `MGN2024_DPTO_POLITICO.zip`
   - Fuente: [Geoportal DANE — Marco Geoestadístico Nacional 2024](https://geoportal.dane.gov.co/servicios/descarga-y-metadatos/datos-geoestadisticos/)

2. **Anexo Estadístico Departamental (Excel):**
   - Archivo: `anex-PMultidimensional-Departamental-2025.xlsx`
   - Fuente: [DANE — Pobreza Multidimensional](https://www.dane.gov.co/index.php/estadisticas-por-tema/pobreza-y-condiciones-de-vida/pobreza-multidimensional)

### 2. Procesamiento automático de los datos

Ejecuta el script de limpieza para transformar el Excel multi-nivel en los tres CSVs que consume el dashboard:

```bash
python limpieza/procesar_datos.py
```

Este proceso generará automáticamente en `ipm-colombia/data/`:
- `ipm_dpto.csv` (IPM general por departamento, año y zona)
- `ipm_indicadores_dpto.csv` (15 indicadores de privación desagregados)
- `ipm_sexo_dpto.csv` (IPM según sexo del jefe de hogar)

---

## Ejecución

Inicia el dashboard con cualquiera de los siguientes comandos:

```bash
python app.py
```
*(o alternativamente: `python mapa_agua.py`)*

Abre tu navegador en: **[http://127.0.0.1:8050](http://127.0.0.1:8050)**

### Variables de entorno opcionales

| Variable | Default | Descripción |
| :--- | :--- | :--- |
| `HOST` | `127.0.0.1` | Dirección de escucha |
| `PORT` | `8050` | Puerto de escucha |
| `DASH_DEBUG` | `false` | Activa recarga en caliente y consola interactiva |

---

## Tecnologías Utilizadas

- **Dash 4.1.0** — Framework web interactivo reactivo
- **Plotly 5.24.1 / 6.x** — Gráficos estadísticos, mapas coropléticos y radar multidimensional
- **PyShp 3.1 & Shapely 2.0** — Procesamiento vectorial y simplificación topológica de geometrías
- **Pandas** — Manipulación y estructuración de series temporales e indicadores
- **OpenPyXL** — Motor de lectura para hojas de cálculo Excel
- **Flask & Werkzeug** — Servidor backend WSGI

---

## Licencia

- **Código:** Licencia MIT.
- **Datos estadísticos y cartográficos:** © DANE (Departamento Administrativo Nacional de Estadística de Colombia).
