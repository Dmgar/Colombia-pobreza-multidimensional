"""
Script para procesar el Excel oficial del DANE:
anex-PMultidimensional-Departamental-2025.xlsx

Genera los tres archivos CSV requeridos por el dashboard:
- data/ipm_dpto.csv
- data/ipm_indicadores_dpto.csv
- data/ipm_sexo_dpto.csv
"""

from pathlib import Path
import re
import sys
import pandas as pd

# Resolver ruta de datos dinámicamente
CURRENT_DIR = Path(__file__).resolve().parent

def encontrar_data_dir():
    candidatos = [
        CURRENT_DIR.parent / "data",              # Si está en ipm-colombia/limpieza/ -> ipm-colombia/data
        CURRENT_DIR / "data",                     # Si está en ipm-colombia/ -> ipm-colombia/data
        CURRENT_DIR.parent.parent / "ipm-colombia" / "data",
        Path.cwd() / "data",
        Path.cwd() / "ipm-colombia" / "data",
    ]
    for c in candidatos:
        if c.exists() and c.is_dir():
            return c
    # Fallback por defecto
    fallback = CURRENT_DIR.parent / "data"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback

DATA_DIR = encontrar_data_dir()
EXCEL_PATH = DATA_DIR / "anex-PMultidimensional-Departamental-2025.xlsx"

CODIGOS_DPTO = {
    "Antioquia": "05",
    "Atlántico": "08",
    "Bogotá D.C.": "11",
    "Bogotá": "11",
    "Bolívar": "13",
    "Boyacá": "15",
    "Caldas": "17",
    "Caquetá": "18",
    "Cauca": "19",
    "Cesar": "20",
    "Córdoba": "23",
    "Cundinamarca": "25",
    "Chocó": "27",
    "Huila": "41",
    "La Guajira": "44",
    "Magdalena": "47",
    "Meta": "50",
    "Nariño": "52",
    "Norte de Santander": "54",
    "Quindío": "63",
    "Risaralda": "66",
    "Santander": "68",
    "Sucre": "70",
    "Tolima": "73",
    "Valle del Cauca": "76",
    "Arauca": "81",
    "Casanare": "85",
    "Putumayo": "86",
    "San Andrés": "88",
    "San Andrés y Providencia": "88",
    "Amazonas": "91",
    "Guainía": "94",
    "Guaviare": "95",
    "Vaupés": "97",
    "Vichada": "99",
}

NORMALIZAR_DPTO = {
    "Bogotá": "Bogotá D.C.",
    "San Andrés y Providencia": "San Andrés",
}

def normalizar_nombre_dpto(nombre):
    if not isinstance(nombre, str):
        return nombre
    nombre = nombre.strip()
    return NORMALIZAR_DPTO.get(nombre, nombre)


def procesar_ipm_departamentos():
    print("-> Procesando Hoja 1: IPM_Departamentos...")
    df = pd.read_excel(EXCEL_PATH, sheet_name="IPM_Departamentos", header=[11, 12])
    
    col_dpto = df.columns[0]
    data_cols = [c for c in df.columns if c != col_dpto]
    
    registros = []
    for _, row in df.iterrows():
        dpto_val = row[col_dpto]
        if pd.isna(dpto_val):
            continue
        dpto = normalizar_nombre_dpto(str(dpto_val).strip())
        if dpto not in CODIGOS_DPTO:
            continue
            
        cod = CODIGOS_DPTO[dpto]
        for col in data_cols:
            anio_raw, cat_raw = col
            a_clean = re.sub(r"\*+", "", str(anio_raw)).strip()
            if not a_clean.isdigit():
                continue
            anio = int(a_clean)
            cat_clean = re.sub(r"\s+", " ", str(cat_raw)).strip()
            val = row[col]
            if pd.notna(val):
                try:
                    val_float = float(val)
                    registros.append({
                        "nombre_dpto": dpto,
                        "Año": anio,
                        "Categoria": cat_clean,
                        "IPM": val_float,
                        "cod_dpto": cod,
                    })
                except (ValueError, TypeError):
                    pass
                    
    df_res = pd.DataFrame(registros)
    out_file = DATA_DIR / "ipm_dpto.csv"
    df_res.to_csv(out_file, index=False, encoding="utf-8-sig")
    print(f"   OK: {len(df_res)} filas guardadas en {out_file.name}")
    print(f"   Departamentos únicos: {df_res['nombre_dpto'].nunique()}, Años: {sorted(df_res['Año'].unique())}")
    return df_res


def procesar_ipm_indicadores():
    print("-> Procesando Hoja 2: IPM_Indicadores_Departamento ...")
    df = pd.read_excel(EXCEL_PATH, sheet_name="IPM_Indicadores_Departamento ", header=[11, 12])
    
    col_dpto_tuple = df.columns[0]
    col_var_tuple = df.columns[1]
    cols_datos = [c for c in df.columns if c not in [col_dpto_tuple, col_var_tuple]]
    
    registros = []
    current_dpto = None
    
    for idx, row in df.iterrows():
        val_dpto = row[col_dpto_tuple]
        val_var = row[col_var_tuple]
        
        if pd.notna(val_dpto):
            nombre_candidato = normalizar_nombre_dpto(str(val_dpto).strip())
            if nombre_candidato in CODIGOS_DPTO:
                current_dpto = nombre_candidato
                
        if pd.notna(val_var) and current_dpto is not None:
            var_clean = str(val_var).strip()
            if var_clean.lower() in ["variable", "indicador"]:
                continue
                
            for col in cols_datos:
                anio_raw, cat_raw = col
                a_clean = re.sub(r"\*+", "", str(anio_raw)).strip()
                if not a_clean.isdigit():
                    continue
                anio = int(a_clean)
                cat_clean = re.sub(r"\s+", " ", str(cat_raw)).strip()
                val = row[col]
                if pd.notna(val):
                    try:
                        val_float = float(val)
                        registros.append({
                            "nombre_dpto": current_dpto,
                            "Variable": var_clean,
                            "Año": anio,
                            "Categoria": cat_clean,
                            "IPM": val_float,
                            "cod_dpto": CODIGOS_DPTO[current_dpto],
                        })
                    except (ValueError, TypeError):
                        pass
                        
    df_res = pd.DataFrame(registros)
    out_file = DATA_DIR / "ipm_indicadores_dpto.csv"
    df_res.to_csv(out_file, index=False, encoding="utf-8-sig")
    print(f"   OK: {len(df_res)} filas guardadas en {out_file.name}")
    print(f"   Departamentos: {df_res['nombre_dpto'].nunique()}, Variables: {df_res['Variable'].nunique()}, Años: {sorted(df_res['Año'].unique())}")
    return df_res


def procesar_ipm_sexo():
    print("-> Procesando Hoja 3: IPM_Sexo Jefe...")
    df_raw = pd.read_excel(EXCEL_PATH, sheet_name="IPM_Sexo Jefe", header=None)
    
    anios_row = df_raw.iloc[10].tolist()
    sexo_row = df_raw.iloc[12].tolist()
    
    current_anio = None
    anios_limpios = []
    for a in anios_row:
        if pd.notna(a):
            a_str = re.sub(r"\*+", "", str(a)).strip()
            if a_str.isdigit():
                current_anio = int(a_str)
        anios_limpios.append(current_anio)
        
    registros = []
    for r in range(13, len(df_raw)):
        dpto_raw = df_raw.iloc[r, 0]
        if pd.isna(dpto_raw):
            continue
        dpto = normalizar_nombre_dpto(str(dpto_raw).strip())
        if dpto not in CODIGOS_DPTO:
            continue
            
        cod = CODIGOS_DPTO[dpto]
        for col_idx in range(1, len(df_raw.columns)):
            anio = anios_limpios[col_idx]
            sexo = str(sexo_row[col_idx]).strip() if pd.notna(sexo_row[col_idx]) else None
            if anio is None or sexo not in ["Hombre", "Mujer"]:
                continue
            val = df_raw.iloc[r, col_idx]
            if pd.notna(val):
                try:
                    val_float = float(val)
                    registros.append({
                        "nombre_dpto": dpto,
                        "Año": anio,
                        "Sexo": sexo,
                        "Valor": val_float,
                        "cod_dpto": cod,
                    })
                except (ValueError, TypeError):
                    pass
                    
    df_res = pd.DataFrame(registros)
    out_file = DATA_DIR / "ipm_sexo_dpto.csv"
    df_res.to_csv(out_file, index=False, encoding="utf-8-sig")
    print(f"   OK: {len(df_res)} filas guardadas en {out_file.name}")
    print(f"   Departamentos: {df_res['nombre_dpto'].nunique()}, Sexos: {df_res['Sexo'].unique().tolist()}, Años: {sorted(df_res['Año'].unique())}")
    return df_res


def main():
    if not EXCEL_PATH.exists():
        print(f"Error: No se encontró el archivo Excel en {EXCEL_PATH}")
        print("Asegúrate de colocar 'anex-PMultidimensional-Departamental-2025.xlsx' en la carpeta data/")
        sys.exit(1)
        
    print(f"Iniciando procesamiento de datos DANE desde: {EXCEL_PATH}")
    procesar_ipm_departamentos()
    procesar_ipm_indicadores()
    procesar_ipm_sexo()
    print("Procesamiento completado con éxito.")


if __name__ == "__main__":
    main()
