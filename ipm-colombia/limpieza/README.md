# Pipeline de Limpieza y Procesamiento de Datos — IPM Colombia

Módulo de preparación, extracción y estructuración de los datos oficiales del DANE para su consumo en el dashboard interactivo.

---

## Estructura del Módulo

- `procesar_datos.py`: Script CLI automatizado que procesa todas las hojas del anexo de Excel y genera los 3 CSVs directamente en `../data/`.
- `limpieza de datos.ipynb`: Notebook de Jupyter para análisis exploratorio y documentación paso a paso de las transformaciones.

---

## Archivo Fuente Requerido

El procesamiento requiere el anexo oficial publicado por el DANE:

- **Archivo:** `anex-PMultidimensional-Departamental-2025.xlsx`
- **Ubicación:** Guardar en `ipm-colombia/data/`
- **Fuente de descarga:** [DANE — Pobreza Multidimensional](https://www.dane.gov.co/index.php/estadisticas-por-tema/pobreza-y-condiciones-de-vida/pobreza-multidimensional)

> *Nota:* Este archivo no está incluido en el control de versiones (Git) por su naturaleza y peso.

---

## Ejecución Automatizada (Recomendada)

Desde la terminal, dentro de `ipm-colombia/`:

```bash
python limpieza/procesar_datos.py
```

### Transformaciones Realizadas

1. **IPM Departamental (`ipm_dpto.csv`):**
   - Hoja: `IPM_Departamentos`
   - Aplanado de encabezados multi-nivel `(Año, Categoría)`.
   - Limpieza de notas y caracteres (`2020**` → `2020`).
   - Normalización de nombres de departamento y asignación de código DANE (`cod_dpto`).
   - Salida: 784 filas (33 departamentos × 8 años: 2018–2025 × 3 categorías de zona).

2. **Indicadores de Privación (`ipm_indicadores_dpto.csv`):**
   - Hoja: `IPM_Indicadores_Departamento `
   - Detección de bloques por departamento y relleno hacia abajo (*forward fill* contextual).
   - Extracción de las 15 variables de privación del IPM (acceso a agua, saneamiento, educación, empleo informal, etc.).
   - Salida: 11,760 filas.

3. **Brecha por Sexo del Jefe de Hogar (`ipm_sexo_dpto.csv`):**
   - Hoja: `IPM_Sexo Jefe`
   - Reestructuración de series de tiempo por jefatura masculina y femenina.
   - Salida: 528 filas.
