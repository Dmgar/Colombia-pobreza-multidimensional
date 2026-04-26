# Limpieza de Datos — IPM Colombia

Notebook de preparación y transformación de los datos crudos del DANE para su uso en el dashboard de Pobreza Multidimensional.

---

## ¿Qué hace este notebook?

Los datos del DANE se publican en Excel con encabezados multi-nivel (MultiIndex) que no son directamente usables con Pandas. Este notebook los transforma al formato limpio que consume el dashboard.

### Hoja 1 — IPM por departamento → `ipm_dpto.csv`

| Paso | Descripción |
|---|---|
| **1. Carga del Excel** | Lee la hoja `IPM_Departamentos` con encabezado multi-nivel en filas 11–12 |
| **2. Aplanado de columnas** | Convierte el MultiIndex `(Año, Categoría)` en columnas simples tipo `2018_Total` |
| **3. Formato largo** | Aplica `melt()` para una fila por observación |
| **4. Limpieza de texto** | Elimina asteriscos de años con notas (`2020**` → `2020`) y saltos de línea |
| **5. Códigos DANE** | Añade `cod_dpto` (2 dígitos) por departamento |
| **6. Exportación** | Guarda como `../data/ipm_dpto.csv` |

### Hoja 2 — Indicadores de privación → `ipm_indicadores_dpto.csv`

| Paso | Descripción |
|---|---|
| **1. Carga** | Lee la hoja de indicadores con el mismo patrón de MultiIndex |
| **2–5. Misma lógica** | Aplanado, `melt()`, limpieza de texto y códigos DANE |
| **6. Exportación** | Guarda como `../data/ipm_indicadores_dpto.csv` (15 variables × 33 dptos × 8 años × 3 zonas) |

### Hoja 3 — IPM por sexo → `ipm_sexo_dpto.csv`

| Paso | Descripción |
|---|---|
| **1. Carga** | Lee la hoja de sexo del jefe de hogar |
| **2–4. Limpieza** | Misma lógica de aplanado y `melt()`, la columna de valor se llama `Valor` |
| **5. Exportación** | Guarda como `../data/ipm_sexo_dpto.csv` (Hombre vs. Mujer por dpto y año) |

---

## Requisitos

El notebook necesita el archivo fuente del DANE:

- **Archivo:** `anex-PMultidimensional-Departamental-2025.xlsx`
- **Fuente:** [DANE — Pobreza Multidimensional](https://www.dane.gov.co/index.php/estadisticas-por-tema/pobreza-y-condiciones-de-vida/pobreza-multidimensional)
- **Hoja usada:** `IPM_Departamentos`

> Este archivo **no se incluye** en el repositorio. Debe descargarse directamente del portal del DANE.

---

## Cómo ejecutar

### 1. Ajusta la ruta del archivo Excel

En la **celda 2** del notebook, actualiza la ruta al archivo Excel según tu equipo:

```python
# ajusta a tu ruta
df = pd.read_excel(
    r"C:\tu\ruta\al\archivo.xlsx",
    ...
)
```

### 2. Ejecuta todas las celdas en orden

```
Menú → Kernel → Restart & Run All
```

### 3. Resultado

Al final de la ejecución, se generará el archivo `ipm_dpto.csv` en el directorio de trabajo actual. Muévelo a la carpeta `data/` del dashboard.

---

## Resultado esperado

```
     nombre_dpto   Año         Categoria   IPM  cod_dpto
0      Antioquia  2018             Total  15.3        05
1      Atlántico  2018             Total  21.1        08
2    Bogotá D.C.  2018             Total   4.1        11
...
[784 rows x 5 columns]
```

- **784 filas:** 33 departamentos × 8 años × 3 categorías de zona
- **Categorías:** `Total`, `Cabeceras`, `Centros poblados y rural disperso`
- **Años:** 2018–2025
