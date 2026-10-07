# IPM Colombia — Dashboard de Pobreza Multidimensional

Dashboard interactivo para explorar el **Índice de Pobreza Multidimensional (IPM)** por departamento en Colombia, construido con Python, Dash, Plotly y GeoPandas.

**Fuente de datos:** DANE · Encuesta Nacional de Calidad de Vida (ECV) 2018–2025

---

## Módulos del Dashboard

1. **Panorama General:** Mapa coroplético interactivo por departamento con métricas clave y departamentos extremos.
2. **Brecha Campo–Ciudad:** Comparativa de brechas territoriales con filtros por zona (Cabeceras, Rural disperso, Brecha neta y Total).
3. **Indicadores de Privación:** Selector dinámico de las 15 dimensiones de privación del IPM y visualización proporcional "Si Colombia fueran 100 personas".
4. **Ranking Departamental:** Ranking horizontal de departamentos más afectados organizado por regiones.
5. **Evolución Anual:** Serie histórica (2018–2025) filtrable por departamento y promedio nacional.
6. **Brecha de Género:** Análisis comparativo según el sexo del jefe de hogar.

---

## Estructura de Archivos

```text
ipm-colombia/
├── app.py                      # Punto de entrada principal recomendado
├── mapa_agua.py                # Lógica del dashboard, layout y callbacks
├── ui.py                       # Componentes de interfaz y diseño visual
├── figuras.py                  # Plantillas de gráficos y anotaciones Plotly
├── requirements.txt            # Lista de dependencias del entorno
├── data/                       # Almacenamiento local de insumos (ignorado en Git)
│   └── .gitkeep
└── limpieza/                   # Módulo de procesamiento y transformación
    ├── README.md               # Documentación específica de preparación
    ├── procesar_datos.py       # Script ejecutable de extracción y limpieza
    └── limpieza de datos.ipynb # Notebook interactivo
```

---

## Instalación y Ejecución Rápida

### 1. Activar entorno e instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Preparar los datos

Coloca los archivos oficiales en la carpeta `data/`:
- `MGN2024_DPTO_POLITICO.zip` (descargar del Geoportal DANE)
- `anex-PMultidimensional-Departamental-2025.xlsx` (descargar del portal DANE)

Ejecuta el script de procesamiento:

```bash
python limpieza/procesar_datos.py
```

### 3. Iniciar la aplicación

```bash
python app.py
```
*(o también: `python mapa_agua.py`)*

Ingresa desde tu navegador a: **http://127.0.0.1:8050**

---

## Configuración del Servidor

Variables de entorno configurables:

| Variable | Default | Descripción |
| :--- | :--- | :--- |
| `HOST` | `127.0.0.1` | Interfaz de red de escucha |
| `PORT` | `8050` | Puerto local |
| `DASH_DEBUG` | `false` | `true` activa el modo debug y hot reload |

---

## Licencia

- Código bajo licencia MIT.
- Datos de libre acceso suministrados por el DANE Colombia.
