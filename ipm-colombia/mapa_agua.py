"""
IPM Colombia — Dashboard de Pobreza Multidimensional
Fuente: DANE · Encuesta de Calidad de Vida (ECV)
Incluye módulo: Brecha en Acceso a Fuente de Agua (2018–2025)
"""

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd
import numpy as np # Para la demo, pero se puede quitar si no se usa

from pathlib import Path

# ══════════════════════════════════════════════════════════════════
# RUTAS DE DATOS (relativas al directorio del proyecto)
# ══════════════════════════════════════════════════════════════════
BASE_DIR     = Path(__file__).parent
GEO_PATH     = BASE_DIR / "data" / "MGN2024_DPTO_POLITICO.zip"
CSV_PATH     = BASE_DIR / "data" / "ipm_dpto.csv"
CSV_AGUA_PATH= BASE_DIR / "data" / "ipm_indicadores_dpto.csv"
CSV_SEXO_PATH= BASE_DIR / "data" / "ipm_sexo_dpto.csv"

# ══════════════════════════════════════════════════════════════════
# MAPEO DE DEPARTAMENTOS A REGIONES
# ══════════════════════════════════════════════════════════════════
REGIONES = {
    "Amazonas":          "Amazonía-Orinoquía",
    "Guainía":           "Amazonía-Orinoquía",
    "Guaviare":          "Amazonía-Orinoquía",
    "Vaupés":            "Amazonía-Orinoquía",
    "Vichada":           "Amazonía-Orinoquía",
    "Meta":              "Amazonía-Orinoquía",
    "Casanare":          "Amazonía-Orinoquía",
    "Arauca":            "Amazonía-Orinoquía",
    "Atlántico":         "Caribe",
    "Bolívar":           "Caribe",
    "Cesar":             "Caribe",
    "Córdoba":           "Caribe",
    "La Guajira":        "Caribe",
    "Magdalena":         "Caribe",
    "Sucre":             "Caribe",
    "San Andrés":        "Caribe",
    "Chocó":             "Pacífica",
    "Cauca":             "Pacífica",
    "Nariño":            "Pacífica",
    "Valle del Cauca":   "Pacífica",
    "Antioquia":         "Central",
    "Caldas":            "Central",
    "Caquetá":           "Central",
    "Huila":             "Central",
    "Putumayo":          "Central",
    "Quindío":           "Central",
    "Risaralda":         "Central",
    "Tolima":            "Central",
    "Boyacá":            "Oriental",
    "Cundinamarca":      "Oriental",
    "Norte de Santander":"Oriental",
    "Santander":         "Oriental",
    "Bogotá D.C.":       "Bogotá D.C. (Cabecera)",
}

REGION_COLORS = {
    "Amazonía-Orinoquía":     "#2D6A4F",
    "Caribe":                 "#1E6091",
    "Pacífica":               "#7B2D8B",
    "Central":                "#E07B39",
    "Oriental":               "#B5341A",
    "Bogotá D.C. (Cabecera)": "#555555",
}

# ══════════════════════════════════════════════════════════════════
# COLORES Y ESTILOS GLOBALES
# ══════════════════════════════════════════════════════════════════
C = {
    "bg":      "#F7F4EF",
    "card":    "#FFFFFF",
    "accent":  "#B5341A",
    "text":    "#1A1A1A",
    "muted":   "#6B6B6B",
    "border":  "#E2DDD6",
    "green":   "#2D6A4F",
    "green2":  "#74C69D",
}

CARD = {
    "background":   C["card"],
    "borderRadius": "12px",
    "padding":      "28px 32px",
    "boxShadow":    "0 2px 12px rgba(0,0,0,0.06)",
    "marginBottom": "24px",
}

BASE_LAYOUT = dict(
    font_family="Georgia, serif",
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(t=40, b=50, l=180, r=40),
)

# ══════════════════════════════════════════════════════════════════
# TEXTOS DINÁMICOS POR INDICADOR
# ══════════════════════════════════════════════════════════════════
TEXTOS_INDICADOR = {
    "Sin acceso a fuente de agua mejorada": {
        "tag":       "ACCESO A FUENTE DE AGUA · 2018–2025",
        "titulo":    "En el campo, carecer de agua limpia sigue siendo la norma.",
        "subtitulo": "Mientras en las cabeceras municipales el acceso a agua mejora año a año, "
                     "los centros poblados y zonas rurales dispersas acumulan una brecha "
                     "que el tiempo no ha cerrado — y en varios departamentos, ha crecido.",
        "fuente":    "Fuente: DANE · ECV 2018–2025. Hogares con privación en acceso a fuente de agua mejorada.",
    },
    "Analfabetismo": {
        "tag":       "ANALFABETISMO · 2018–2025",
        "titulo":    "Leer y escribir sigue siendo un privilegio en el campo colombiano.",
        "subtitulo": "Las zonas rurales dispersas concentran tasas de analfabetismo que triplican "
                     "las de las cabeceras municipales, una brecha que refleja décadas de abandono educativo.",
        "fuente":    "Fuente: DANE · ECV 2018–2025. Hogares con privación por analfabetismo.",
    },
    "Bajo logro educativo": {
        "tag":       "BAJO LOGRO EDUCATIVO · 2018–2025",
        "titulo":    "La educación completa aún es una deuda pendiente con el campo.",
        "subtitulo": "El logro educativo en zonas rurales dispersas avanza lentamente, "
                     "mientras la brecha frente a las cabeceras persiste año tras año.",
        "fuente":    "Fuente: DANE · ECV 2018–2025. Hogares con privación por bajo logro educativo.",
    },
    "Barreras a servicios para cuidado de la primera infancia": {
        "tag":       "PRIMERA INFANCIA · 2018–2025",
        "titulo":    "El acceso al cuidado infantil temprano divide dos Colombias desde el nacimiento.",
        "subtitulo": "Las barreras para acceder a servicios de primera infancia son especialmente "
                     "agudas en zonas rurales, afectando el desarrollo de los niños desde sus primeros años.",
        "fuente":    "Fuente: DANE · ECV 2018–2025. Hogares con privación en cuidado de primera infancia.",
    },
    "Barreras de acceso a servicios de salud": {
        "tag":       "ACCESO A SALUD · 2018–2025",
        "titulo":    "Enfermarse en el campo puede ser más costoso que la enfermedad misma.",
        "subtitulo": "La distancia, el costo y la oferta insuficiente de servicios de salud "
                     "golpean desproporcionalmente a las comunidades rurales dispersas.",
        "fuente":    "Fuente: DANE · ECV 2018–2025. Hogares con barreras de acceso a servicios de salud.",
    },
    "Desempleo de larga duración": {
        "tag":       "DESEMPLEO DE LARGA DURACIÓN · 2018–2025",
        "titulo":    "Sin trabajo estable, la pobreza se vuelve una trampa generacional.",
        "subtitulo": "El desempleo prolongado afecta de manera diferenciada a las zonas rurales, "
                     "donde las oportunidades laborales formales son escasas y estacionales.",
        "fuente":    "Fuente: DANE · ECV 2018–2025. Hogares con privación por desempleo de larga duración.",
    },
    "Hacinamiento crítico": {
        "tag":       "HACINAMIENTO CRÍTICO · 2018–2025",
        "titulo":    "Vivir hacinado no es una elección: es el resultado de años de déficit habitacional.",
        "subtitulo": "El hacinamiento crítico persiste con mayor fuerza en zonas rurales, "
                     "donde el acceso a vivienda digna continúa siendo una promesa incumplida.",
        "fuente":    "Fuente: DANE · ECV 2018–2025. Hogares con privación por hacinamiento crítico.",
    },
    "Inadecuada eliminación de excretas": {
        "tag":       "SANEAMIENTO BÁSICO · 2018–2025",
        "titulo":    "Sin saneamiento adecuado, la dignidad y la salud están en riesgo.",
        "subtitulo": "La eliminación inadecuada de excretas sigue siendo alarmantemente alta "
                     "en las zonas rurales dispersas, con consecuencias directas sobre la salud pública.",
        "fuente":    "Fuente: DANE · ECV 2018–2025. Hogares con privación por inadecuada eliminación de excretas.",
    },
    "Inasistencia escolar": {
        "tag":       "INASISTENCIA ESCOLAR · 2018–2025",
        "titulo":    "Millones de niños rurales siguen sin poder ir a la escuela.",
        "subtitulo": "La inasistencia escolar en zonas rurales dispersas revela que la distancia, "
                     "el trabajo infantil y la falta de infraestructura siguen siendo barreras reales.",
        "fuente":    "Fuente: DANE · ECV 2018–2025. Hogares con privación por inasistencia escolar.",
    },
    "Material inadecuado de paredes exteriores": {
        "tag":       "CONDICIONES DE VIVIENDA · 2018–2025",
        "titulo":    "Las paredes de una casa no deberían determinar el futuro de quien vive en ella.",
        "subtitulo": "El uso de materiales inadecuados en paredes exteriores refleja un déficit "
                     "habitacional que se concentra fuertemente en la Colombia rural.",
        "fuente":    "Fuente: DANE · ECV 2018–2025. Hogares con privación por material inadecuado de paredes.",
    },
    "Material inadecuado de pisos": {
        "tag":       "CONDICIONES DE VIVIENDA · 2018–2025",
        "titulo":    "Los pisos de tierra son un indicador silencioso de pobreza estructural.",
        "subtitulo": "El material inadecuado de pisos persiste en zonas rurales como síntoma "
                     "de un déficit habitacional que el Estado no ha logrado cerrar.",
        "fuente":    "Fuente: DANE · ECV 2018–2025. Hogares con privación por material inadecuado de pisos.",
    },
    "Rezago escolar": {
        "tag":       "REZAGO ESCOLAR · 2018–2025",
        "titulo":    "Estudiar con años de retraso tiene costos que se pagan toda la vida.",
        "subtitulo": "El rezago escolar en zonas rurales dispersas acumula desventajas "
                     "que limitan el acceso al mercado laboral y perpetúan la pobreza.",
        "fuente":    "Fuente: DANE · ECV 2018–2025. Hogares con privación por rezago escolar.",
    },
    "Sin aseguramiento en salud": {
        "tag":       "ASEGURAMIENTO EN SALUD · 2018–2025",
        "titulo":    "Sin seguro médico, una enfermedad puede hundir a una familia en la pobreza.",
        "subtitulo": "La falta de aseguramiento en salud golpea desproporcionalmente a las zonas "
                     "rurales, dejando a miles de familias sin red de protección ante emergencias.",
        "fuente":    "Fuente: DANE · ECV 2018–2025. Hogares con privación por falta de aseguramiento en salud.",
    },
    "Trabajo infantil": {
        "tag":       "TRABAJO INFANTIL · 2018–2025",
        "titulo":    "Cuando los niños trabajan, el futuro paga el precio del presente.",
        "subtitulo": "El trabajo infantil es más prevalente en zonas rurales dispersas, "
                     "donde la necesidad económica saca a los niños del aula y los lleva al campo.",
        "fuente":    "Fuente: DANE · ECV 2018–2025. Hogares con privación por trabajo infantil.",
    },
    "Trabajo informal": {
        "tag":       "TRABAJO INFORMAL · 2018–2025",
        "titulo":    "Trabajar sin derechos laborales es la norma, no la excepción, en el campo.",
        "subtitulo": "La informalidad laboral domina la estructura económica de las zonas rurales, "
                     "privando a los trabajadores de pensión, salud y estabilidad.",
        "fuente":    "Fuente: DANE · ECV 2018–2025. Hogares con privación por trabajo informal.",
    },
}

# ══════════════════════════════════════════════════════════════════
# CARGA Y LIMPIEZA DE DATOS DE AGUA
# ══════════════════════════════════════════════════════════════════
# --- Definir CATEGORIAS_AGUA ANTES de usarla ---
CATEGORIAS_AGUA = {
    "Cabeceras":                           "Cabecera",
    "Cabecera municipal":                 "Cabecera",
    "Centros poblados  y rural disperso": "Rural disperso",
    "Centros poblados y rural disperso":  "Rural disperso",
    "Total":                              "Total",
}

# --- Detectar automáticamente la columna de valor ---
COL_VALOR_CANDIDATAS = ['Incidencia', 'Porcentaje', 'Valor', 'Porcentaje_privacion', 'IPM']
COL_VALOR = None

# --- Cargar datos de indicadores ---
geo_dpto = gpd.read_file(GEO_PATH)
imp_dpto = pd.read_csv(CSV_PATH, dtype={"cod_dpto": "str"})
geo_dpto.rename(columns={"dpto_ccdgo": "cod_dpto"}, inplace=True)

imp_dpto["region"] = imp_dpto["nombre_dpto"].map(REGIONES).fillna("Otra")

ind_dpto = pd.read_csv(CSV_AGUA_PATH, dtype={"cod_dpto": "str"})

categorias = imp_dpto["Categoria"].unique().tolist()
anios      = sorted(imp_dpto["Año"].unique().tolist())

# Opciones para el dropdown de Evolución Anual
dptos_lista_evol = sorted([d for d in imp_dpto["nombre_dpto"].unique() if pd.notna(d)])
opciones_dptos_evol = [{"label": "Promedio Nacional", "value": "Nacional"}] + [{"label": d, "value": d} for d in dptos_lista_evol]

# --- Lista de todos los indicadores disponibles ---
INDICADORES_DISPONIBLES = [
    "Sin acceso a fuente de agua mejorada",
    "Analfabetismo",
    "Bajo logro educativo",
    "Barreras a servicios para cuidado de la primera infancia",
    "Barreras de acceso a servicios de salud",
    "Desempleo de larga duración",
    "Hacinamiento crítico",
    "Inadecuada eliminación de excretas",
    "Inasistencia escolar",
    "Material inadecuado de paredes exteriores",
    "Material inadecuado de pisos",
    "Rezago escolar",
    "Sin aseguramiento en salud",
    "Trabajo infantil",
    "Trabajo informal",
]

NOMBRE_INDICADOR_AGUA = INDICADORES_DISPONIBLES[0]

# ══════════════════════════════════════════════════════════════════
# DETECCIÓN DE COLUMNA DE VALOR (una sola vez sobre el CSV completo)
# ══════════════════════════════════════════════════════════════════
COL_VALOR = None
for _col in COL_VALOR_CANDIDATAS:
    if _col in ind_dpto.columns:
        COL_VALOR = _col
        break
if COL_VALOR is None:
    _posibles = [c for c in ind_dpto.columns
                 if c not in ['Año', 'cod_dpto', 'nombre_dpto', 'Categoria', 'Variable', 'Indicador']]
    if _posibles:
        COL_VALOR = _posibles[0]
        print(f"Advertencia: Usando '{COL_VALOR}' como columna de valor.")
    else:
        raise ValueError("No se pudo identificar la columna de valor en ind_dpto.")

# Limpieza base del CSV completo (una sola vez)
ind_dpto["Categoria"] = ind_dpto["Categoria"].str.strip()
ind_dpto["cat_label"] = ind_dpto["Categoria"].map(CATEGORIAS_AGUA)
ind_dpto["valor"]     = pd.to_numeric(ind_dpto[COL_VALOR], errors="coerce")
ind_dpto["Año"]       = pd.to_numeric(ind_dpto["Año"],     errors="coerce")

# ══════════════════════════════════════════════════════════════════
# PRECÁLCULO DE TODOS LOS INDICADORES AL ARRANCAR
# Cada indicador queda listo en CACHE_IND[nombre] = {"nac": df, "dpto": df}
# El callback solo hace CACHE_IND[indicador_agua] — sin filtrar ni agrupar
# ══════════════════════════════════════════════════════════════════
CACHE_IND = {}
for _ind in INDICADORES_DISPONIBLES:
    _mask = ind_dpto["Variable"].str.contains(_ind, case=False, na=False, regex=False)
    _df   = ind_dpto.loc[_mask & ind_dpto["cat_label"].notna()]

    _nac = (
        _df.groupby(["Año", "cat_label"])["valor"]
        .mean().reset_index()
        .rename(columns={"cat_label": "zona", "valor": "pct"})
    )
    _dpto = (
        _df.groupby(["Año", "nombre_dpto", "cat_label"])["valor"]
        .mean().reset_index()
        .rename(columns={"cat_label": "zona", "valor": "pct"})
    )
    CACHE_IND[_ind] = {"nac": _nac, "dpto": _dpto}

print(f"Cache lista: {len(CACHE_IND)} indicadores precalculados.")

# Variables de compatibilidad para referencias posteriores
df_agua_nac  = CACHE_IND[NOMBRE_INDICADOR_AGUA]["nac"]
df_agua_dpto = CACHE_IND[NOMBRE_INDICADOR_AGUA]["dpto"]
dptos_disponibles = sorted(df_agua_dpto["nombre_dpto"].dropna().unique().tolist())

# ══════════════════════════════════════════════════════════════════
# CARGA Y LIMPIEZA DE DATOS DE GÉNERO (Sexo del jefe de hogar)
# Columnas esperadas: nombre_dpto, Año, Sexo, Valor, cod_dpto
# ══════════════════════════════════════════════════════════════════
df_sexo = pd.read_csv(CSV_SEXO_PATH, dtype={"cod_dpto": "str"})
df_sexo["Año"]   = pd.to_numeric(df_sexo["Año"],   errors="coerce")
df_sexo["Valor"] = pd.to_numeric(df_sexo["Valor"], errors="coerce")
df_sexo = df_sexo.dropna(subset=["Año", "Valor", "Sexo", "nombre_dpto"])
df_sexo["Sexo"] = df_sexo["Sexo"].str.strip()

dptos_sexo    = sorted(df_sexo["nombre_dpto"].dropna().unique().tolist())
ANIO_MAX_SEXO = int(df_sexo["Año"].max())

print(f"Datos de género cargados: {len(df_sexo)} filas · {len(dptos_sexo)} departamentos.")

# ══════════════════════════════════════════════════════════════════
# PALETA Y ESTILOS ESPECÍFICOS DE LA SECCIÓN DE AGUA
# ══════════════════════════════════════════════════════════════════
COLOR_CABECERA = "#1A6FA8"       # azul oscuro → ciudad
COLOR_RURAL    = "#C94A17"       # rojo tierra → campo
COLOR_TOTAL    = "#9B8B6E"       # arena → promedio

PALETA_AGUA = {
    "Cabecera":      COLOR_CABECERA,
    "Rural disperso": COLOR_RURAL,
    "Total":         COLOR_TOTAL,
}

SIMBOLO_AGUA = {
    "Cabecera":      "circle",
    "Rural disperso": "diamond",
    "Total":         "square",
}

DASH_AGUA = {
    "Cabecera":      "solid",
    "Rural disperso": "dot",
    "Total":         "dash",
}

ANCHO_AGUA = {
    "Cabecera":      2.5,
    "Rural disperso": 3.5,   # más grueso para énfasis en la brecha
    "Total":         1.5,
}

# ══════════════════════════════════════════════════════════════════
# PALETA Y ESTILOS PARA LA SECCIÓN DE GÉNERO
# ══════════════════════════════════════════════════════════════════
COLOR_HOMBRE = "#1A6FA8"   # azul → hombre
COLOR_MUJER  = "#C94A17"   # rojo tierra → mujer

PALETA_SEXO  = {"Hombre": COLOR_HOMBRE, "Mujer": COLOR_MUJER}
DASH_SEXO    = {"Hombre": "solid",       "Mujer": "dot"}
SIMBOLO_SEXO = {"Hombre": "circle",      "Mujer": "diamond"}
ANCHO_SEXO   = {"Hombre": 2.5,           "Mujer": 3.0}

TEXTO_GENERO = {
    "tag":       "DISPARIDAD DE GÉNERO · 2018–2025",
    "titulo":    "La pobreza no afecta igual a hombres y mujeres.",
    "subtitulo": (
        "En Colombia, las mujeres enfrentan una doble vulnerabilidad: además de las carencias "
        "estructurales compartidas con sus comunidades, acumulan desventajas específicas en "
        "acceso al mercado laboral, protección social y autonomía económica dentro del hogar. "
        "Esta sección examina si el sexo del jefe de hogar se correlaciona con la incidencia "
        "de privación en cada departamento entre 2018 y 2025 — y dónde esa brecha es más aguda."
    ),
    "fuente":    "Fuente: DANE · ECV 2018–2025. Hogares con privación en Sin acceso a fuente de agua mejorada, desagregado por sexo del jefe de hogar.",
}

# ══════════════════════════════════════════════════════════════════
# FUNCIÓN CONSTRUCTORA DE LA FIGURA DE AGUA
# ══════════════════════════════════════════════════════════════════
def build_fig_agua(dpto_sel="Nacional", df_nac=None, df_dpto=None, nombre_ind="Sin acceso a fuente de agua mejorada"):
    if df_nac is None:
        df_nac = df_agua_nac
    if df_dpto is None:
        df_dpto = df_agua_dpto
    """
    Construye la figura de la brecha de acceso a agua.
    dpto_sel: "Nacional" usa el promedio nacional;
              cualquier otro nombre filtra ese departamento.
    """
    if dpto_sel == "Nacional":
        df_plot = df_nac.copy()
        subtitulo = "Promedio nacional · todas las categorías de zona"
    else:
        df_plot = df_dpto[df_dpto["nombre_dpto"] == dpto_sel].copy()
        df_plot = df_plot[["Año", "zona", "pct"]]
        subtitulo = f"Departamento: {dpto_sel}"

    fig = go.Figure()

    zonas_orden = ["Rural disperso", "Cabecera", "Total"]
    
    # Obtener años disponibles para este indicador
    anios_disponibles = sorted(df_plot["Año"].dropna().unique().tolist())
    anios_agua = [int(a) for a in anios_disponibles]

    for zona in zonas_orden:
        ds = df_plot[df_plot["zona"] == zona].sort_values("Año")
        if ds.empty:
            continue

        # Área de fondo sólo para Rural (énfasis visual)
        if zona == "Rural disperso":
            fig.add_trace(go.Scatter(
                x=list(ds["Año"]) + list(ds["Año"])[::-1],
                y=list(ds["pct"]) + [0] * len(ds),
                fill="toself",
                fillcolor="rgba(201, 74, 23, 0.08)",
                line=dict(width=0),
                showlegend=False,
                hoverinfo="skip",
                name="_relleno_rural",
            ))

        # Línea principal
        fig.add_trace(go.Scatter(
            x=ds["Año"],
            y=ds["pct"],
            mode="lines+markers+text",
            name=zona,
            line=dict(
                color=PALETA_AGUA[zona],
                width=ANCHO_AGUA[zona],
                dash=DASH_AGUA[zona],
            ),
            marker=dict(
                symbol=SIMBOLO_AGUA[zona],
                size=10,
                color=PALETA_AGUA[zona],
                line=dict(width=1.5, color="white"),
            ),
            # Etiquetas de datos en cada punto
            text=ds["pct"].map("{:.1f}%".format),
            textposition="top center",
            textfont=dict(
                family="DM Mono, monospace",
                size=10,
                color=PALETA_AGUA[zona],
            ),
            hovertemplate=(
                f"<b>{zona}</b><br>"
                "Año: %{x}<br>"
                "Porcentaje con privación: %{y:.1f}%"
                "<extra></extra>"
            ),
        ))

    # ── Anotaciones clave ────────────────────────────────────────
    # Flecha de brecha en el año más reciente disponible
    if not df_plot.empty:
        anio_max = int(df_plot["Año"].max())
        val_rural = df_plot.loc[
            (df_plot["Año"] == anio_max) & (df_plot["zona"] == "Rural disperso"), "pct"
        ]
        # Busca Cabecera; si no existe usa Total como referencia
        val_cab = df_plot.loc[
            (df_plot["Año"] == anio_max) & (df_plot["zona"] == "Cabecera"), "pct"
        ]
        if val_cab.empty:
            val_cab = df_plot.loc[
                (df_plot["Año"] == anio_max) & (df_plot["zona"] == "Total"), "pct"
            ]

        if not val_rural.empty and not val_cab.empty:
            vr = val_rural.values[0]
            vc = val_cab.values[0]
            brecha = vr - vc

            fig.add_annotation(
                x=anio_max,
                y=(vr + vc) / 2,
                text=f"<b>Brecha<br>{brecha:+.1f} pp</b>",
                showarrow=False,
                xanchor="left",
                xshift=18,
                font=dict(family="DM Mono, monospace", size=12, color="#B5341A"),
                bgcolor="rgba(255,248,245,0.9)",
                bordercolor="#B5341A",
                borderwidth=1,
                borderpad=5,
            )
            # Línea de brecha vertical
            fig.add_shape(
                type="line",
                x0=anio_max, x1=anio_max,
                y0=vc, y1=vr,
                line=dict(color="#B5341A", width=1.5, dash="dot"),
            )

    # ── Layout ───────────────────────────────────────────────────
    fig.update_layout(
        font_family="Georgia, serif",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=460,
        margin=dict(t=50, b=150, l=60, r=80),
        xaxis=dict(
            title=dict(text="Año", font=dict(size=11, color="#6B6B6B")),
            tickmode="array",
            tickvals=anios_agua,
            ticktext=[str(a) for a in anios_agua],
            tickfont=dict(family="DM Mono, monospace", size=11),
            showgrid=True,
            gridcolor="#F0EBE3",
            gridwidth=1,
            zeroline=False,
        ),
            yaxis=dict(
                title=dict(
                    text=f"Hogares con privación: {nombre_ind[:40]}{'...' if len(nombre_ind) > 40 else ''} (%)",
                font=dict(size=11, color="#6B6B6B"),
            ),
            ticksuffix="%",
            tickfont=dict(family="DM Mono, monospace", size=11),
            showgrid=True,
            gridcolor="#F0EBE3",
            gridwidth=1,
            zeroline=False,
            rangemode="tozero",
        ),
        legend=dict(
            orientation="h",
            y=-0.55,
            x=0.5,
            xanchor="center",
            font=dict(family="Source Serif 4, serif", size=12),
            bgcolor="rgba(0,0,0,0)",
            itemwidth=80,
        ),
        hovermode="x unified",
    )

    return fig

# ══════════════════════════════════════════════════════════════════
# FUNCIÓN CONSTRUCTORA: EVOLUCIÓN POR SEXO (líneas Hombre vs Mujer)
# ══════════════════════════════════════════════════════════════════
def build_fig_genero(dpto_sel="Nacional"):
    """
    Línea temporal Hombre vs Mujer del indicador de privación.
    dpto_sel: "Nacional" usa el promedio de todos los dptos;
              cualquier otro nombre filtra ese departamento.
    """
    if dpto_sel == "Nacional":
        df_plot = (
            df_sexo.groupby(["Año", "Sexo"])["Valor"]
            .mean().reset_index()
        )
    else:
        df_plot = df_sexo[df_sexo["nombre_dpto"] == dpto_sel][
            ["Año", "Sexo", "Valor"]
        ].copy()

    fig = go.Figure()
    anios_g = sorted([int(a) for a in df_plot["Año"].dropna().unique()])

    for sexo in ["Hombre", "Mujer"]:
        ds = df_plot[df_plot["Sexo"] == sexo].sort_values("Año")
        if ds.empty:
            continue

        # Relleno bajo la línea de Mujer para énfasis visual
        if sexo == "Mujer":
            fig.add_trace(go.Scatter(
                x=list(ds["Año"]) + list(ds["Año"])[::-1],
                y=list(ds["Valor"]) + [0] * len(ds),
                fill="toself",
                fillcolor="rgba(201, 74, 23, 0.07)",
                line=dict(width=0),
                showlegend=False,
                hoverinfo="skip",
            ))

        fig.add_trace(go.Scatter(
            x=ds["Año"],
            y=ds["Valor"],
            mode="lines+markers+text",
            name=sexo,
            line=dict(
                color=PALETA_SEXO[sexo],
                width=ANCHO_SEXO[sexo],
                dash=DASH_SEXO[sexo],
            ),
            marker=dict(
                symbol=SIMBOLO_SEXO[sexo],
                size=10,
                color=PALETA_SEXO[sexo],
                line=dict(width=1.5, color="white"),
            ),
            text=ds["Valor"].map("{:.1f}%".format),
            textposition="top center",
            textfont=dict(family="DM Mono, monospace", size=10, color=PALETA_SEXO[sexo]),
            hovertemplate=(
                f"<b>{sexo}</b><br>Año: %{{x}}<br>Privación: %{{y:.1f}}%<extra></extra>"
            ),
        ))

    # Anotación de brecha en el año más reciente
    if not df_plot.empty:
        anio_max = int(df_plot["Año"].max())
        val_m = df_plot.loc[(df_plot["Año"] == anio_max) & (df_plot["Sexo"] == "Mujer"),  "Valor"]
        val_h = df_plot.loc[(df_plot["Año"] == anio_max) & (df_plot["Sexo"] == "Hombre"), "Valor"]
        if not val_m.empty and not val_h.empty:
            vm, vh = val_m.values[0], val_h.values[0]
            brecha = vm - vh
            fig.add_annotation(
                x=anio_max,
                y=(vm + vh) / 2,
                text=f"<b>Brecha<br>{brecha:+.1f} pp</b>",
                showarrow=False,
                xanchor="left",
                xshift=18,
                font=dict(family="DM Mono, monospace", size=12, color="#B5341A"),
                bgcolor="rgba(255,248,245,0.9)",
                bordercolor="#B5341A",
                borderwidth=1,
                borderpad=5,
            )
            fig.add_shape(
                type="line",
                x0=anio_max, x1=anio_max,
                y0=min(vm, vh), y1=max(vm, vh),
                line=dict(color="#B5341A", width=1.5, dash="dot"),
            )

    fig.update_layout(
        font_family="Georgia, serif",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=460,
        margin=dict(t=50, b=150, l=60, r=90),
        xaxis=dict(
            title=dict(text="Año", font=dict(size=11, color="#6B6B6B")),
            tickmode="array",
            tickvals=anios_g,
            ticktext=[str(a) for a in anios_g],
            tickfont=dict(family="DM Mono, monospace", size=11),
            showgrid=True, gridcolor="#F0EBE3", gridwidth=1, zeroline=False,
        ),
        yaxis=dict(
            title=dict(text="Hogares con privación (%)", font=dict(size=11, color="#6B6B6B")),
            ticksuffix="%",
            tickfont=dict(family="DM Mono, monospace", size=11),
            showgrid=True, gridcolor="#F0EBE3", gridwidth=1, zeroline=False, rangemode="tozero",
        ),
        legend=dict(
            orientation="h", y=-0.55, x=0.5, xanchor="center",
            font=dict(family="Source Serif 4, serif", size=12),
            bgcolor="rgba(0,0,0,0)",
            itemwidth=80,
        ),
        hovermode="x unified",
    )
    return fig


# ══════════════════════════════════════════════════════════════════
# FUNCIÓN CONSTRUCTORA: DISPARIDAD POR DEPARTAMENTO (barras horizontales)
# ══════════════════════════════════════════════════════════════════
def build_fig_disparidad_dpto():
    """
    Barras horizontales: brecha (Mujer − Hombre) en el año más reciente,
    ordenadas de menor a mayor. Rojo = mujeres más afectadas; azul = hombres más afectados.
    Devuelve (fig, anio_max, df_pivot).
    """
    df_pivot = (
        df_sexo[df_sexo["Año"] == ANIO_MAX_SEXO]
        .pivot_table(index="nombre_dpto", columns="Sexo", values="Valor")
        .dropna()
    )
    df_pivot["brecha"] = df_pivot["Mujer"] - df_pivot["Hombre"]
    df_pivot = df_pivot.sort_values("brecha", ascending=True).reset_index()

    colors = [COLOR_MUJER if b > 0 else COLOR_HOMBRE for b in df_pivot["brecha"]]

    fig = go.Figure(go.Bar(
        x=df_pivot["brecha"],
        y=df_pivot["nombre_dpto"],
        orientation="h",
        marker_color=colors,
        text=df_pivot["brecha"].map("{:+.1f}".format),
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Brecha (Mujer − Hombre): %{x:+.1f} pp<extra></extra>"
        ),
    ))
    fig.add_vline(x=0, line_dash="dot", line_color="#999", line_width=1)

    x_max = df_pivot["brecha"].abs().max()
    fig.update_layout(
        **{**BASE_LAYOUT, "margin": dict(t=30, b=50, l=180, r=80)},
        height=max(500, len(df_pivot) * 22),
        xaxis_title="Brecha Mujer − Hombre (puntos porcentuales)",
        yaxis_title="",
        yaxis=dict(autorange="reversed"),
        shapes=[
            dict(
                type="rect", xref="x", yref="paper",
                x0=-x_max * 1.05, x1=0, y0=0, y1=1,
                fillcolor="rgba(26,111,168,0.04)", line_width=0,
            ),
            dict(
                type="rect", xref="x", yref="paper",
                x0=0, x1=x_max * 1.05, y0=0, y1=1,
                fillcolor="rgba(201,74,23,0.04)", line_width=0,
            ),
        ],
    )
    return fig, ANIO_MAX_SEXO, df_pivot
# ══════════════════════════════════════════════════════════════════
SECCION_AGUA_LAYOUT = html.Div(style={
    "background":    "#FFFFFF",
    "borderRadius":  "12px",
    "padding":       "28px 32px",
    "boxShadow":     "0 2px 12px rgba(0,0,0,0.06)",
    "marginBottom":  "24px",
    "borderTop":     "4px solid #1A6FA8",
}, children=[

    # ── Encabezado de sección ─────────────────────────────
    html.P(id="seccion-tag-agua",
           style={
               "fontFamily":    "'DM Mono', monospace",
               "fontSize":      "0.68rem",
               "letterSpacing": "0.13em",
               "color":         "#1A6FA8",
               "marginBottom":  "6px",
           }),

    # ── Mensaje clave ────────────────────────────────────
    html.H2(id="titulo-agua",
        style={
            "fontFamily":  "'Playfair Display', serif",
            "fontSize":    "clamp(1.2rem, 2.5vw, 1.8rem)",
            "fontWeight":  "700",
            "color":       "#1A1A1A",
            "lineHeight":  "1.25",
            "marginBottom": "10px",
        }
    ),

    # ── Subtítulo ────────────────────────────────────────
    html.P(id="subtitulo-agua",
        style={
            "fontFamily": "'Source Serif 4', serif",
            "fontSize":   "0.95rem",
            "color":      "#5A5A5A",
            "lineHeight": "1.7",
            "maxWidth":   "780px",
            "marginBottom": "22px",
        }
    ),

    # ── Insight narrativo ────────────────────────────────
    html.Div(
        id="insight-agua",
        style={
            "background":   "#FFF8F5",
            "borderLeft":   "3px solid #C94A17",
            "padding":      "14px 18px",
            "borderRadius": "0 8px 8px 0",
            "fontFamily":   "'Source Serif 4', serif",
            "fontStyle":    "italic",
            "color":        "#3A2A20",
            "fontSize":     "0.93rem",
            "lineHeight":   "1.65",
            "marginBottom": "20px",
        }
    ),

    # ── Leyenda de formas preattentivas ─────────────────
    html.Div(style={
        "display": "flex", "gap": "60px", "flexWrap": "wrap",
        "marginBottom": "24px", "alignItems": "center",
    }, children=[
        html.Div(style={"display": "flex", "alignItems": "center", "gap": "8px"}, children=[
            html.Div(style={
                "width": "32px", "height": "3px",
                "background": "#1A6FA8", "borderRadius": "2px"
            }),
            html.Div("◯  Cabecera municipal", style={
                "fontFamily": "'Source Serif 4', serif",
                "fontSize": "0.82rem", "color": "#1A6FA8", "fontWeight": "600"
            }),
        ]),
        html.Div(style={"display": "flex", "alignItems": "center", "gap": "8px"}, children=[
            html.Div(style={
                "width": "32px", "height": "3px",
                "background": "#C94A17",
                "borderTop": "3px dotted #C94A17",
                "borderBottom": "none"
            }),
            html.Div("◆  Rural disperso", style={
                "fontFamily": "'Source Serif 4', serif",
                "fontSize": "0.82rem", "color": "#C94A17", "fontWeight": "600"
            }),
        ]),
        html.Div(style={"display": "flex", "alignItems": "center", "gap": "8px"}, children=[
            html.Div(style={
                "width": "32px", "height": "2px",
                "background": "#9B8B6E",
                "borderTop": "2px dashed #9B8B6E",
            }),
            html.Div("▪  Total nacional", style={
                "fontFamily": "'Source Serif 4', serif",
                "fontSize": "0.82rem", "color": "#9B8B6E",
            }),
        ]),
    ]),

    # ── Selector de departamento ─────────────────────────
    html.Div([
    html.Label("Ver indicador", style={
        "fontFamily": "'DM Mono', monospace",
        "fontSize": "0.68rem", "letterSpacing": ".08em",
        "color": "#6B6B6B", "textTransform": "uppercase",
        "display": "block", "marginBottom": "5px",
    }),
    dcc.Dropdown(
        id="dd-indicador-agua",
        options=[{"label": ind, "value": ind} for ind in INDICADORES_DISPONIBLES],
        value=INDICADORES_DISPONIBLES[0],
        clearable=False,
        style={"width": "420px", "fontFamily": "Georgia,serif"},
    ),
]),
    html.Div(style={"marginBottom": "18px", "display": "flex", "gap": "16px", "alignItems": "flex-end"}, children=[
        html.Div([
            html.Label("Ver por departamento", style={
                "fontFamily": "'DM Mono', monospace",
                "fontSize": "0.68rem", "letterSpacing": ".08em",
                "color": "#6B6B6B", "textTransform": "uppercase",
                "display": "block", "marginBottom": "5px",
            }),
            dcc.Dropdown(
                id="dd-dpto-agua",
                options=(
                    [{"label": "Nacional (promedio)", "value": "Nacional"}] +
                    [{"label": d, "value": d} for d in dptos_disponibles]
                ),
                value="Nacional",
                clearable=False,
                style={"width": "280px", "fontFamily": "Georgia,serif"},
            ),
        ]),
    ]),

    # ── Gráfico ──────────────────────────────────────────
    dcc.Graph(id="g-agua", config={"displayModeBar": False}),

    # ── Nota metodológica ────────────────────────────────
    html.P(id="fuente-agua",
        style={
            "fontFamily": "'DM Mono', monospace",
            "fontSize": "0.68rem",
            "color": "#9B8B6E",
            "letterSpacing": "0.04em",
            "marginTop": "12px",
        }
    ),
])

# ══════════════════════════════════════════════════════════════════
# BLOQUE HTML PARA LA SECCIÓN DE GÉNERO
# ══════════════════════════════════════════════════════════════════
SECCION_GENERO_LAYOUT = html.Div(style={
    "background":    "#FFFFFF",
    "borderRadius":  "12px",
    "padding":       "28px 32px",
    "boxShadow":     "0 2px 12px rgba(0,0,0,0.06)",
    "marginBottom":  "24px",
    "borderTop":     "4px solid #C94A17",
}, children=[

    # ── Encabezado ───────────────────────────────────────
    html.P(TEXTO_GENERO["tag"], style={
        "fontFamily":    "'DM Mono', monospace",
        "fontSize":      "0.68rem",
        "letterSpacing": "0.13em",
        "color":         "#C94A17",
        "marginBottom":  "6px",
    }),

    html.H2(TEXTO_GENERO["titulo"], style={
        "fontFamily":   "'Playfair Display', serif",
        "fontSize":     "clamp(1.2rem, 2.5vw, 1.8rem)",
        "fontWeight":   "700",
        "color":        "#1A1A1A",
        "lineHeight":   "1.25",
        "marginBottom": "10px",
    }),

    html.P(TEXTO_GENERO["subtitulo"], style={
        "fontFamily":   "'Source Serif 4', serif",
        "fontSize":     "0.95rem",
        "color":        "#5A5A5A",
        "lineHeight":   "1.7",
        "maxWidth":     "780px",
        "marginBottom": "22px",
    }),

    # ── Insight narrativo (evolución) ─────────────────────
    html.Div(id="insight-genero", style={
        "background":   "#FFF8F5",
        "borderLeft":   "3px solid #C94A17",
        "padding":      "14px 18px",
        "borderRadius": "0 8px 8px 0",
        "fontFamily":   "'Source Serif 4', serif",
        "fontStyle":    "italic",
        "color":        "#3A2A20",
        "fontSize":     "0.93rem",
        "lineHeight":   "1.65",
        "marginBottom": "20px",
    }),

    # ── Leyenda ───────────────────────────────────────────
    html.Div(style={
        "display": "flex", "gap": "60px", "flexWrap": "wrap",
        "marginBottom": "24px", "alignItems": "center",
    }, children=[
        html.Div(style={"display": "flex", "alignItems": "center", "gap": "8px"}, children=[
            html.Div(style={"width": "32px", "height": "3px",
                            "background": "#1A6FA8", "borderRadius": "2px"}),
            html.Div("◯  Hombre (jefe de hogar)", style={
                "fontFamily": "'Source Serif 4', serif",
                "fontSize": "0.82rem", "color": "#1A6FA8", "fontWeight": "600",
            }),
        ]),
        html.Div(style={"display": "flex", "alignItems": "center", "gap": "8px"}, children=[
            html.Div(style={
                "width": "32px", "height": "0",
                "borderTop": "3px dotted #C94A17",
            }),
            html.Div("◆  Mujer (jefa de hogar)", style={
                "fontFamily": "'Source Serif 4', serif",
                "fontSize": "0.82rem", "color": "#C94A17", "fontWeight": "600",
            }),
        ]),
    ]),

    # ── Selector de departamento ──────────────────────────
    html.Div(style={"marginBottom": "18px"}, children=[
        html.Label("Ver por departamento", style={
            "fontFamily":    "'DM Mono', monospace",
            "fontSize":      "0.68rem",
            "letterSpacing": ".08em",
            "color":         "#6B6B6B",
            "textTransform": "uppercase",
            "display":       "block",
            "marginBottom":  "5px",
        }),
        dcc.Dropdown(
            id="dd-dpto-genero",
            options=(
                [{"label": "Nacional (promedio)", "value": "Nacional"}] +
                [{"label": d, "value": d} for d in dptos_sexo]
            ),
            value="Nacional",
            clearable=False,
            style={"width": "280px", "fontFamily": "Georgia,serif"},
        ),
    ]),

    # ── Gráfico: evolución Hombre vs Mujer ───────────────
    html.P("Evolución temporal por sexo del jefe de hogar",
           className="section-tag", style={"marginBottom": "4px"}),
    dcc.Graph(id="g-genero-evol", config={"displayModeBar": False}),

    # ── Separador ────────────────────────────────────────
    html.Hr(style={"border": "none", "borderTop": "1px solid #E2DDD6",
                   "margin": "32px 0 24px"}),

    # ── Gráfico: disparidad por departamento ─────────────
    html.P(f"Brecha de género por departamento · {ANIO_MAX_SEXO}",
           className="section-tag", style={"marginBottom": "8px"}),
    html.P(
        "Diferencia en puntos porcentuales entre hogares con jefa mujer y hogares con jefe hombre. "
        "Rojo: mayor privación en hogares liderados por mujeres. "
        "Azul: mayor privación en hogares liderados por hombres.",
        style={
            "fontFamily": "'Source Serif 4', serif",
            "fontSize":   "0.88rem",
            "color":      "#6B6B6B",
            "lineHeight": "1.6",
            "marginBottom": "12px",
        },
    ),
    html.Div(id="insight-disparidad-genero", style={
        "background":   "#F5F8FF",
        "borderLeft":   "3px solid #1A6FA8",
        "padding":      "14px 18px",
        "borderRadius": "0 8px 8px 0",
        "fontFamily":   "'Source Serif 4', serif",
        "fontStyle":    "italic",
        "color":        "#1A2A3A",
        "fontSize":     "0.91rem",
        "lineHeight":   "1.65",
        "marginBottom": "16px",
    }),
    dcc.Graph(id="g-genero-dpto", config={"displayModeBar": False}),

    # ── Nota metodológica ─────────────────────────────────
    html.P(TEXTO_GENERO["fuente"], style={
        "fontFamily":   "'DM Mono', monospace",
        "fontSize":     "0.68rem",
        "color":        "#9B8B6E",
        "letterSpacing": "0.04em",
        "marginTop":    "12px",
    }),
])

# ══════════════════════════════════════════════════════════════════
# APP DASH
# ══════════════════════════════════════════════════════════════════
app = Dash(__name__, title="IPM Colombia · DANE", external_stylesheets=['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'])

app.index_string = """
<!DOCTYPE html>
<html lang="es">
<head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Serif+4:ital,wght@0,300;0,400;1,300&family=DM+Mono:wght@400&display=swap" rel="stylesheet">
    <style>
        /* ── Reset ───────────────────────────────────────────── */
        * { box-sizing: border-box; margin: 0; padding: 0; }
        html, body { height: 100%; width: 100%; }
        body { background: #141414; }

        /* ── Shell: sidebar + contenido ─────────────────────── */
        #app-shell {
            display: flex;
            width: 100%;
            min-height: 100vh;
        }

        /* Dash inyecta un div extra — forzarlo a ocupar todo el ancho */
        #app-shell > div:first-child {
            display: flex;
            width: 100%;
            min-height: 100vh;
        }

        /* ── Sidebar ─────────────────────────────────────────── */
        .sidebar {
            width: 230px;
            min-width: 230px;
            background: #141414;
            min-height: 100vh;
            position: sticky;
            top: 0;
            height: 100vh;
            display: flex;
            flex-direction: column;
            z-index: 200;
            overflow-y: auto;
        }

        .sidebar-brand {
            padding: 28px 22px 24px;
            border-bottom: 1px solid rgba(255,255,255,0.07);
        }
        .sidebar-brand-tag {
            font-family: 'DM Mono', monospace;
            font-size: 0.58rem;
            letter-spacing: 0.18em;
            color: #B5341A;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        .sidebar-brand-title {
            font-family: 'Playfair Display', serif;
            font-size: 0.95rem;
            color: #F0EDE8;
            font-weight: 700;
            line-height: 1.35;
        }
        .sidebar-brand-sub {
            font-family: 'Source Serif 4', serif;
            font-size: 0.72rem;
            color: #666;
            margin-top: 6px;
            line-height: 1.4;
        }

        .sidebar-nav {
            padding: 16px 0;
            flex: 1;
        }

        .nav-section-label {
            font-family: 'DM Mono', monospace;
            font-size: 0.55rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: #444;
            padding: 14px 22px 6px;
        }

        .nav-item {
            display: flex;
            align-items: center;
            gap: 11px;
            padding: 11px 22px;
            cursor: pointer;
            border: none;
            border-left: 3px solid transparent;
            background: transparent;
            text-align: left;
            width: 100%;
            transition: background 0.15s, border-color 0.15s, color 0.15s;
            color: #888;
            text-decoration: none;
        }
        .nav-item:hover {
            background: rgba(255,255,255,0.04);
            color: #D0CCC6;
        }
        .nav-item.active {
            border-left-color: #B5341A;
            background: rgba(181,52,26,0.10);
            color: #F0EDE8;
        }
        .nav-icon {
            font-size: 1rem;
            width: 18px;
            text-align: center;
            flex-shrink: 0;
        }
        .nav-label {
            font-family: 'Source Serif 4', serif;
            font-size: 0.85rem;
            line-height: 1.2;
        }
        .nav-badge {
            margin-left: auto;
            font-family: 'DM Mono', monospace;
            font-size: 0.58rem;
            background: rgba(181,52,26,0.25);
            color: #C94A17;
            padding: 2px 6px;
            border-radius: 20px;
        }

        .sidebar-footer {
            padding: 18px 22px;
            border-top: 1px solid rgba(255,255,255,0.07);
        }
        .sidebar-footer p {
            font-family: 'DM Mono', monospace;
            font-size: 0.6rem;
            color: #444;
            letter-spacing: 0.06em;
            line-height: 1.6;
        }

        /* ── Contenido principal ─────────────────────────────── */
        .main-content {
            flex: 1;
            min-width: 0;
            overflow-y: auto;
        }

        /* ── Paneles de sección ──────────────────────────────── */
        .section-panel { display: none; }
        .section-panel.active { display: block; }

        /* ── Componentes originales ──────────────────────────── */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }
        .kpi-card {
            background: white;
            border-radius: 10px;
            padding: 22px 26px;
            border-left: 4px solid #B5341A;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        .kpi-num   { font-family:'DM Mono',monospace; font-size:2rem; color:#B5341A; line-height:1; }
        .kpi-label { font-family:'Source Serif 4',serif; font-size:0.82rem; color:#6B6B6B; margin-top:6px; }

        .insight {
            background: #FFF8F5;
            border-left: 3px solid #B5341A;
            padding: 14px 18px;
            border-radius: 0 8px 8px 0;
            font-family:'Source Serif 4',serif;
            font-style: italic;
            color: #3A2A20;
            font-size: 0.93rem;
            line-height: 1.65;
            margin-bottom: 18px;
        }

        .section-tag {
            font-family:'DM Mono',monospace;
            font-size:0.68rem;
            text-transform:uppercase;
            letter-spacing:0.13em;
            color:#B5341A;
            margin-bottom:8px;
        }

        .two-col { display:grid; grid-template-columns:1fr 1fr; gap:24px; }
        .map-narrative { display:grid; grid-template-columns:1fr 320px; gap:32px; align-items:start; }

        .controls-row { display:flex; gap:24px; align-items:flex-end; }
        .ctrl-group   { display:flex; flex-direction:column; gap:5px; }
        .ctrl-label   { font-family:'DM Mono',monospace; font-size:0.68rem; letter-spacing:.08em; color:#6B6B6B; text-transform:uppercase; }

        .legend-dot  { display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:6px; }
        .legend-item { font-family:'Source Serif 4',serif; font-size:0.82rem; color:#3A2A20; display:flex; align-items:center; margin-bottom:5px; }
        .legend-box  { margin-top:16px; }

        /* ── Page header dentro de cada sección ─────────────── */
        .page-header {
            padding: 36px 48px 28px;
            border-bottom: 1px solid #E2DDD6;
            margin-bottom: 32px;
        }
        .page-header-tag {
            font-family: 'DM Mono', monospace;
            font-size: 0.62rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: #B5341A;
            margin-bottom: 8px;
        }
        .page-header h2 {
            font-family: 'Playfair Display', serif;
            font-size: clamp(1.4rem, 2.5vw, 2rem);
            font-weight: 900;
            color: #1A1A1A;
            line-height: 1.15;
            margin-bottom: 10px;
        }
        .page-header p {
            font-family: 'Source Serif 4', serif;
            font-size: 0.92rem;
            color: #6B6B6B;
            max-width: 680px;
            line-height: 1.65;
        }

        /* ── Responsive ──────────────────────────────────────── */
        @media(max-width:1024px){
            .sidebar { width: 200px; min-width: 200px; }
        }
        @media(max-width:768px){
            .sidebar { width: 100%; height: auto; position: relative; flex-direction: row; flex-wrap: wrap; }
            #app-shell { flex-direction: column; }
            .kpi-grid { grid-template-columns:1fr 1fr; }
            .two-col  { grid-template-columns:1fr; }
            .map-narrative { grid-template-columns:1fr; }
            .controls-row  { flex-direction:column; }
        }
    </style>
</head>
<body>
<div id="app-shell">
{%app_entry%}
</div>
{%config%}{%scripts%}{%renderer%}
<script>
(function() {
    var SECTIONS = ['panorama', 'brecha', 'indicadores', 'ranking', 'evolucion', 'genero'];

    function showSection(sectionId) {
        SECTIONS.forEach(function(id) {
            var panel = document.getElementById('sec-' + id);
            var navEl = document.querySelector('[data-section="' + id + '"]');
            if (panel) panel.classList.remove('active');
            if (navEl) navEl.classList.remove('active');
        });
        var target = document.getElementById('sec-' + sectionId);
        var navTarget = document.querySelector('[data-section="' + sectionId + '"]');
        if (target) target.classList.add('active');
        if (navTarget) navTarget.classList.add('active');
        sessionStorage.setItem('ipm-section', sectionId);
    }

    // Delegación de eventos — funciona después de que React renderice
    document.addEventListener('click', function(e) {
        var item = e.target.closest('.nav-item');
        if (item && item.dataset.section) {
            e.preventDefault();
            showSection(item.dataset.section);
        }
    });

    // Inicializar cuando los paneles estén listos
    function initNav() {
        var panels = document.querySelectorAll('.section-panel');
        if (panels.length < SECTIONS.length) {
            setTimeout(initNav, 120);
            return;
        }
        var saved = sessionStorage.getItem('ipm-section') || 'panorama';
        showSection(saved);
    }
    setTimeout(initNav, 300);
})();
</script>
</body>
</html>
"""

# ── Helpers de layout ──────────────────────────────────────────────
def page_header(tag, title, desc):
    """Encabezado reutilizable para cada sección."""
    return html.Div(className="page-header", children=[
        html.P(tag, className="page-header-tag"),
        html.H2(title),
        html.P(desc),
    ])

def nav_item(icon, label, section, badge=None):
    children = [
        html.Span(icon, className="nav-icon"),
        html.Span(label, className="nav-label"),
    ]
    if badge:
        children.append(html.Span(badge, className="nav-badge"))
    return html.Button(
        children,
        className="nav-item",
        **{"data-section": section},
    )

# ── Layout ─────────────────────────────────────────────────────────
app.layout = html.Div(style={"display": "flex", "width": "100%", "minHeight": "100vh", "background": "#141414"}, children=[

    # ════════════════════════════════════════════════════
    # SIDEBAR
    # ════════════════════════════════════════════════════
    html.Aside(className="sidebar", children=[

        # Brand
        html.Div(className="sidebar-brand", children=[
            html.P("DANE · ECV 2018–2025", className="sidebar-brand-tag"),
            html.P("IPM Colombia", className="sidebar-brand-title"),
            html.P("Índice de Pobreza\nMultidimensional", className="sidebar-brand-sub"),
        ]),

        # Navegación
        html.Nav(className="sidebar-nav", children=[
            html.P("Explorar", className="nav-section-label"),
            nav_item("🗺️", "Panorama general",   "panorama"),
            nav_item("⚖️", "Brecha campo–ciudad", "brecha"),
            nav_item("💧", "Indicadores de privación", "indicadores", "15"),
            nav_item("📊", "Ranking departamental", "ranking"),
            nav_item("📈", "Evolución anual",     "evolucion"),
            nav_item("⚥",  "Brecha por género",   "genero"),
        ]),

        # Footer sidebar
        html.Div(className="sidebar-footer", children=[
            html.P("Fuente: DANE · ECV\n2024–2025 · CNPV 2018"),
        ]),
    ]),

    # ════════════════════════════════════════════════════
    # CONTENIDO PRINCIPAL
    # ════════════════════════════════════════════════════
    html.Main(className="main-content", style={"background": C["bg"]}, children=[

        # ── Header oscuro: solo título ───────────────────
        html.Div(style={
            "background": C["text"], "color": "white",
            "padding": "32px 48px 28px",
        }, children=[
            html.P("DANE · Encuesta de Calidad de Vida",
                   className="section-tag", style={"color": "#B5341A", "marginBottom": "10px"}),
            html.H1("¿Dónde vive la pobreza en Colombia?",
                    style={"fontFamily": "'Playfair Display',serif",
                           "fontSize": "clamp(1.6rem,3vw,2.6rem)",
                           "fontWeight": "900", "lineHeight": "1.1", "marginBottom": "12px"}),
            html.P(
                "El IPM mide carencias en salud, educación y condiciones de vida. "
                "Nacer en la Amazonía o el Pacífico multiplica hasta 7 veces "
                "la probabilidad de vivir en pobreza multidimensional.",
                style={"fontFamily": "'Source Serif 4',serif", "fontSize": "0.95rem",
                       "color": "#9A9A9A", "maxWidth": "620px", "lineHeight": "1.65"}
            ),
        ]),

        # ── Barra de filtros globales (fondo claro) ──────
        html.Div(style={
            "background": "#FFFFFF",
            "borderBottom": "1px solid #E2DDD6",
            "padding": "14px 48px",
            "display": "flex",
            "gap": "24px",
            "alignItems": "flex-end",
            "flexWrap": "wrap",
            "position": "sticky",
            "top": "0",
            "zIndex": "100",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.06)",
        }, children=[
            html.Div(style={"display": "flex", "alignItems": "center", "gap": "6px",
                            "marginRight": "8px"}, children=[
                html.Span("Filtros globales", style={
                    "fontFamily": "'DM Mono',monospace",
                    "fontSize": "0.65rem",
                    "letterSpacing": "0.12em",
                    "textTransform": "uppercase",
                    "color": "#B5341A",
                }),
            ]),
            html.Div(className="ctrl-group", children=[
                html.Label("Categoría de zona", className="ctrl-label"),
                dcc.Dropdown(id="dd-cat",
                    options=[{"label": c, "value": c} for c in categorias],
                    value="Total", clearable=False,
                    style={"width": "300px", "fontFamily": "Georgia,serif"})
            ]),
            html.Div(className="ctrl-group", children=[
                html.Label("Año", className="ctrl-label"),
                dcc.Dropdown(id="dd-anio",
                    options=[{"label": str(a), "value": a} for a in anios],
                    value=max(anios), clearable=False,
                    style={"width": "110px", "fontFamily": "Georgia,serif"})
            ]),
            html.Div(style={"marginLeft": "auto", "alignSelf": "center"}, children=[
                html.P("Aplica a: Panorama · Brecha · Ranking · Evolución",
                       style={"fontFamily": "'DM Mono',monospace", "fontSize": "0.6rem",
                              "color": "#AAAAAA", "letterSpacing": "0.05em"}),
            ]),
        ]),

        # ══════════════════════════════════════════════════
        # SECCIÓN 1 — Panorama general
        # ══════════════════════════════════════════════════
        html.Div(id="sec-panorama", className="section-panel", children=[
            page_header(
                "PANORAMA GENERAL",
                "Colombia en cifras de pobreza",
                "Indicadores clave del IPM nacional y distribución territorial "
                "por departamento según el año y categoría de zona seleccionados."
            ),
            html.Div(style={"padding": "0 48px 48px"}, children=[
                
                # Contexto General Multidimensional
                html.Div(style={"marginBottom": "32px", "display": "grid", "gridTemplateColumns": "2fr 1fr", "gap": "24px"}, children=[
                    html.Div(style={**CARD, "marginBottom": "0"}, children=[
                        html.H3("¿Qué es la Pobreza Multidimensional?", style={"fontFamily": "'Playfair Display', serif", "fontSize": "1.4rem", "marginBottom": "12px", "color": "#1A1A1A"}),
                        html.P(
                            "El Índice de Pobreza Multidimensional (IPM) permite comprender que la pobreza no es solo la falta de ingresos, "
                            "sino el conjunto de múltiples privaciones simultáneas que enfrentan los hogares en aspectos fundamentales de su bienestar.",
                            style={"fontFamily": "'Source Serif 4', serif", "fontSize": "0.95rem", "color": "#4A4A4A", "lineHeight": "1.6", "marginBottom": "12px"}
                        ),
                        html.P(
                            "A diferencia de la pobreza monetaria, el IPM evalúa si los hogares tienen acceso a educación oportuna, si los niños asisten al colegio, "
                            "si cuentan con aseguramiento en salud, si disponen de acceso a agua mejorada y saneamiento, y si habitan en condiciones de hacinamiento crítico, entre otras. "
                            "Un hogar se considera en situación de pobreza multidimensional si concentra privaciones en al menos el 33.3% del índice ponderado.",
                            style={"fontFamily": "'Source Serif 4', serif", "fontSize": "0.95rem", "color": "#4A4A4A", "lineHeight": "1.6"}
                        )
                    ]),
                    html.Div(style={**CARD, "background": "#B5341A", "color": "white", "marginBottom": "0"}, children=[
                        html.H3("5 Dimensiones Evaluadas", style={"fontFamily": "'Playfair Display', serif", "fontSize": "1.2rem", "marginBottom": "14px", "color": "white"}),
                        html.Ul(style={"paddingLeft": "20px", "fontFamily": "'Source Serif 4', serif", "fontSize": "0.85rem", "lineHeight": "1.7", "color": "#FFF0ED"}, children=[
                            html.Li("Condiciones Educativas"),
                            html.Li("Condiciones de la Niñez y Juventud"),
                            html.Li("Trabajo"),
                            html.Li("Salud"),
                            html.Li("Servicios Públicos y Vivienda"),
                        ])
                    ])
                ]),

                # Gráfico: Si Colombia fueran 100 personas
                html.Div(style={**CARD, "marginBottom": "32px", "display": "flex", "gap": "32px", "alignItems": "center", "flexWrap": "wrap"}, children=[
                    html.Div(style={"flex": "1", "minWidth": "300px"}, children=[
                        html.H3("Si Colombia fueran 100 personas...", style={"fontFamily": "'Playfair Display', serif", "fontSize": "1.6rem", "marginBottom": "16px", "color": "#1A1A1A"}),
                        html.P(
                            "Selecciona una privación específica para ver cuántas personas de cada 100 se ven afectadas, cruzando los datos con los filtros globales de Año y Zona.",
                            style={"fontFamily": "'Source Serif 4', serif", "fontSize": "0.95rem", "color": "#6B6B6B", "marginBottom": "16px", "lineHeight": "1.6"}
                        ),
                        html.Label("Privación a visualizar", className="ctrl-label"),
                        dcc.Dropdown(
                            id="dd-waffle",
                            options=[{"label": ind, "value": ind} for ind in INDICADORES_DISPONIBLES],
                            value="Sin acceso a fuente de agua mejorada",
                            clearable=False,
                            style={"fontFamily": "Georgia,serif", "marginBottom": "24px"}
                        ),
                        html.Div(id="text-waffle", style={
                            "fontFamily": "'Source Serif 4', serif",
                            "fontSize": "1.1rem",
                            "color": "#333",
                            "lineHeight": "1.6",
                            "background": "#FDFBF7",
                            "padding": "16px",
                            "borderRadius": "8px",
                            "borderLeft": "4px solid #B5341A"
                        })
                    ])
                ]),

                # KPIs
                html.Div(id="kpis", className="kpi-grid"),

                # MAPA + narrativa
                html.Div(style=CARD, children=[
                    html.Div(className="map-narrative", children=[
                        html.Div([
                            html.P("Distribución territorial", className="section-tag"),
                            dcc.Graph(id="mapa", config={"displayModeBar": False})
                        ]),
                        html.Div([
                            html.P("Lectura del indicador de pobreza", className="section-tag"),
                            html.Div(id="nar-mapa"),
                        ], style={"paddingTop": "24px"})
                    ])
                ]),
            ]),
        ]),

        # ══════════════════════════════════════════════════
        # SECCIÓN 2 — Brecha campo–ciudad (IPM)
        # ══════════════════════════════════════════════════
        html.Div(id="sec-brecha", className="section-panel", children=[
            page_header(
                "BRECHA CAMPO–CIUDAD · IPM",
                "Dos Colombias separadas por la geografía",
                "En los departamentos más pobres, la diferencia entre zonas rurales y "
                "cabeceras municipales puede superar 30 puntos porcentuales de IPM."
            ),
            html.Div(style={"padding": "0 48px 48px"}, children=[
                html.Div(style={"marginBottom": "32px", "display": "grid", "gridTemplateColumns": "1.2fr 1fr 1fr", "gap": "24px"}, children=[
                    html.Div(style={**CARD, "marginBottom": "0"}, children=[
                        html.H3("La Desigualdad Territorial", style={"fontFamily": "'Playfair Display', serif", "fontSize": "1.4rem", "marginBottom": "12px", "color": "#1A1A1A"}),
                        html.P(
                            "La brecha campo-ciudad refleja la concentración histórica de la inversión, servicios e infraestructura en las cabeceras municipales, "
                            "dejando a las zonas rurales dispersas rezagadas en casi todos los indicadores de calidad de vida.",
                            style={"fontFamily": "'Source Serif 4', serif", "fontSize": "0.95rem", "color": "#4A4A4A", "lineHeight": "1.6", "marginBottom": "12px"}
                        ),
                        html.P(
                            "Esta sección permite comparar directamente el IPM de las zonas urbanas con el de los centros poblados y áreas rurales dispersas. "
                            "Un alto valor de brecha indica que el lugar de residencia determina en gran medida las oportunidades y el nivel de privación de los hogares.",
                            style={"fontFamily": "'Source Serif 4', serif", "fontSize": "0.95rem", "color": "#4A4A4A", "lineHeight": "1.6"}
                        )
                    ]),
                    html.Div(style={**CARD, "background": "#2D6A4F", "color": "white", "marginBottom": "0"}, children=[
                        html.H3("Definición de Zonas", style={"fontFamily": "'Playfair Display', serif", "fontSize": "1.2rem", "marginBottom": "14px", "color": "white"}),
                        html.Ul(style={"paddingLeft": "20px", "fontFamily": "'Source Serif 4', serif", "fontSize": "0.85rem", "lineHeight": "1.7", "color": "#E6F4EA"}, children=[
                            html.Li([html.B("Cabecera: ", style={"color": "white"}), "Área urbana principal del municipio."]),
                            html.Li([html.B("Rural disperso: ", style={"color": "white"}), "Zonas alejadas y centros poblados menores."]),
                            html.Li([html.B("Total: ", style={"color": "white"}), "Promedio ponderado del departamento."]),
                        ])
                    ]),
                    html.Div(style={**CARD, "background": "#F5F8FF", "borderLeft": "4px solid #1A6FA8", "marginBottom": "0"}, children=[
                        html.H3("Contexto Regional", style={"fontFamily": "'Playfair Display', serif", "fontSize": "1.2rem", "marginBottom": "14px", "color": "#1A6FA8"}),
                        html.P(
                            "En América Latina, la pobreza rural sistemáticamente duplica o triplica a la urbana. "
                            "La CEPAL advierte que el rezago en infraestructura y el aislamiento geográfico "
                            "convierten a las zonas rurales dispersas en los territorios más excluidos del continente, "
                            "un patrón estructural del cual Colombia es claro ejemplo.",
                            style={"fontFamily": "'Source Serif 4', serif", "fontSize": "0.85rem", "color": "#4A4A4A", "lineHeight": "1.7"}
                        )
                    ])
                ]),
                html.Div(style={"display": "flex", "gap": "16px", "marginBottom": "20px"}, children=[
                    html.Div(className="ctrl-group", children=[
                        html.Label("Ordenar por zona", className="ctrl-label"),
                        dcc.Dropdown(id="dd-orden-brecha",
                            options=[
                                {"label": "Brecha (Total departamental)", "value": "Total"},
                                {"label": "Cabecera", "value": "Cabecera"},
                                {"label": "Rural disperso", "value": "Centros poblados  y rural disperso"}
                            ],
                            value="Total", clearable=False,
                            style={"width": "260px", "fontFamily": "Georgia,serif"}
                        )
                    ]),
                    html.Div(className="ctrl-group", children=[
                        html.Label("Sentido", className="ctrl-label"),
                        dcc.Dropdown(id="dd-sentido-brecha",
                            options=[
                                {"label": "Descendente (Mayor a menor)", "value": "desc"},
                                {"label": "Ascendente (Menor a mayor)", "value": "asc"}
                            ],
                            value="desc", clearable=False,
                            style={"width": "260px", "fontFamily": "Georgia,serif"}
                        )
                    ])
                ]),
                html.Div(style=CARD, children=[
                    html.Div(id="nar-brecha", style={"marginBottom": "16px"}),
                    dcc.Graph(id="g-brecha", config={"displayModeBar": False})
                ]),
            ]),
        ]),

        # ══════════════════════════════════════════════════
        # SECCIÓN 3 — Indicadores de privación (agua, etc.)
        # ══════════════════════════════════════════════════
        html.Div(id="sec-indicadores", className="section-panel", children=[
            page_header(
                "INDICADORES DE PRIVACIÓN · 2018–2025",
                "Las brechas que el tiempo no ha cerrado",
                "Explora 15 indicadores del IPM — desde acceso a agua potable hasta "
                "trabajo infantil — y cómo evolucionan en el campo vs. la ciudad."
            ),
            html.Div(style={"padding": "0 48px 48px"}, children=[
                html.Div(style={"marginBottom": "32px", "display": "grid", "gridTemplateColumns": "1.2fr 1fr 1fr", "gap": "24px"}, children=[
                    html.Div(style={**CARD, "marginBottom": "0"}, children=[
                        html.H3("Profundizando en las Privaciones", style={"fontFamily": "'Playfair Display', serif", "fontSize": "1.4rem", "marginBottom": "12px", "color": "#1A1A1A"}),
                        html.P(
                            "El Índice de Pobreza Multidimensional se compone de múltiples indicadores específicos que evalúan dimensiones clave del bienestar. "
                            "Desagregar el índice general en estas variables permite identificar con precisión en qué aspectos están fallando las políticas sociales.",
                            style={"fontFamily": "'Source Serif 4', serif", "fontSize": "0.95rem", "color": "#4A4A4A", "lineHeight": "1.6", "marginBottom": "12px"}
                        ),
                        html.P(
                            "En esta sección puede explorar cada indicador de forma individual, visualizando su evolución histórica y "
                            "analizando las profundas diferencias que persisten entre las áreas urbanas y las zonas rurales dispersas para cada necesidad básica.",
                            style={"fontFamily": "'Source Serif 4', serif", "fontSize": "0.95rem", "color": "#4A4A4A", "lineHeight": "1.6"}
                        )
                    ]),
                    html.Div(style={**CARD, "background": "#7B2D8B", "color": "white", "marginBottom": "0"}, children=[
                        html.H3("Aspectos a Explorar", style={"fontFamily": "'Playfair Display', serif", "fontSize": "1.2rem", "marginBottom": "14px", "color": "white"}),
                        html.Ul(style={"paddingLeft": "20px", "fontFamily": "'Source Serif 4', serif", "fontSize": "0.85rem", "lineHeight": "1.7", "color": "#F3E8F5"}, children=[
                            html.Li("Acceso a agua y saneamiento."),
                            html.Li("Condiciones de la vivienda."),
                            html.Li("Barreras de acceso a salud."),
                            html.Li("Logro y rezago escolar."),
                            html.Li("Trabajo informal e infantil."),
                        ])
                    ]),
                    html.Div(style={**CARD, "background": "#FFF5F8", "borderLeft": "4px solid #C94A17", "marginBottom": "0"}, children=[
                        html.H3("Más Allá del Ingreso", style={"fontFamily": "'Playfair Display', serif", "fontSize": "1.2rem", "marginBottom": "14px", "color": "#C94A17"}),
                        html.P(
                            "Incluso cuando las familias logran superar la línea de pobreza monetaria, las carencias estructurales "
                            "como la falta de saneamiento básico o rezago escolar persisten. El enfoque multidimensional "
                            "revela que la provisión de bienes públicos es el principal motor de desigualdad persistente "
                            "en América Latina.",
                            style={"fontFamily": "'Source Serif 4', serif", "fontSize": "0.85rem", "color": "#4A4A4A", "lineHeight": "1.7"}
                        )
                    ])
                ]),
                SECCION_AGUA_LAYOUT,
            ]),
        ]),

        # ══════════════════════════════════════════════════
        # SECCIÓN 4 — Ranking departamental
        # ══════════════════════════════════════════════════
        html.Div(id="sec-ranking", className="section-panel", children=[
            page_header(
                "RANKING DEPARTAMENTAL",
                "Los departamentos con mayor deuda social",
                "Comparación de los 10 departamentos más afectados y el IPM promedio "
                "por región, revelando la desigualdad territorial del país."
            ),
            html.Div(style={"padding": "0 48px 48px"}, children=[
                html.Div(style={"marginBottom": "32px", "display": "grid", "gridTemplateColumns": "1.2fr 1fr 1fr", "gap": "24px"}, children=[
                    html.Div(style={**CARD, "marginBottom": "0"}, children=[
                        html.H3("Geografía de la Pobreza en Colombia", style={"fontFamily": "'Playfair Display', serif", "fontSize": "1.4rem", "marginBottom": "12px", "color": "#1A1A1A"}),
                        html.P(
                            "El análisis por departamentos revela cómo la pobreza multidimensional no se distribuye de manera uniforme "
                            "a lo largo del territorio nacional. Históricamente, las regiones periféricas han presentado mayores niveles de vulnerabilidad.",
                            style={"fontFamily": "'Source Serif 4', serif", "fontSize": "0.95rem", "color": "#4A4A4A", "lineHeight": "1.6", "marginBottom": "12px"}
                        ),
                        html.P(
                            "Este ranking permite identificar no solo cuáles son los territorios con mayores necesidades "
                            "sino también cómo se agrupan geográficamente. Comparar las regiones evidencia la brecha existente "
                            "entre el centro del país y sus fronteras, la costa Pacífica y la Amazonía.",
                            style={"fontFamily": "'Source Serif 4', serif", "fontSize": "0.95rem", "color": "#4A4A4A", "lineHeight": "1.6"}
                        )
                    ]),
                    html.Div(style={**CARD, "background": "#1A6FA8", "color": "white", "marginBottom": "0"}, children=[
                        html.H3("Regiones de Análisis", style={"fontFamily": "'Playfair Display', serif", "fontSize": "1.2rem", "marginBottom": "14px", "color": "white"}),
                        html.Ul(style={"paddingLeft": "20px", "fontFamily": "'Source Serif 4', serif", "fontSize": "0.85rem", "lineHeight": "1.7", "color": "#E5F0F9"}, children=[
                            html.Li("Amazonía-Orinoquía"),
                            html.Li("Caribe"),
                            html.Li("Pacífica"),
                            html.Li("Central y Oriental"),
                            html.Li("Bogotá D.C."),
                        ])
                    ]),
                    html.Div(style={**CARD, "background": "#F0FAF5", "borderLeft": "4px solid #2D6A4F", "marginBottom": "0"}, children=[
                        html.H3("Descentralización y Desigualdad", style={"fontFamily": "'Playfair Display', serif", "fontSize": "1.2rem", "marginBottom": "14px", "color": "#2D6A4F"}),
                        html.P(
                            "América Latina es la región más desigual del mundo. Esta brecha no es solo social, sino marcadamente territorial. "
                            "Las periferias (costas y selvas) heredan profundos rezagos frente a los centros administrativos andinos, "
                            "demostrando que el Estado no ha logrado una integración equitativa del territorio nacional.",
                            style={"fontFamily": "'Source Serif 4', serif", "fontSize": "0.85rem", "color": "#4A4A4A", "lineHeight": "1.7"}
                        )
                    ])
                ]),
                html.Div(className="two-col", children=[
                    html.Div(style=CARD, children=[
                        html.P("Departamentos más afectados", className="section-tag"),
                        html.Div(id="nar-rank", style={"marginBottom": "12px"}),
                        dcc.Graph(id="g-rank", config={"displayModeBar": False})
                    ]),
                    html.Div(style=CARD, children=[
                        html.P("IPM promedio por región", className="section-tag"),
                        html.Div(id="nar-region", style={"marginBottom": "12px"}),
                        dcc.Graph(id="g-region", config={"displayModeBar": False})
                    ]),
                ]),
            ]),
        ]),

        # ══════════════════════════════════════════════════
        # SECCIÓN 5 — Evolución anual
        # ══════════════════════════════════════════════════
        html.Div(id="sec-evolucion", className="section-panel", children=[
            page_header(
                "EVOLUCIÓN ANUAL",
                "¿Quiénes avanzan y quiénes retroceden?",
                "Variación del IPM respecto al año anterior por departamento. "
                "Los avances no son uniformes: mientras unas regiones mejoran, otras retroceden."
            ),
            html.Div(style={"padding": "0 48px 48px"}, children=[
                html.Div(style={"marginBottom": "32px", "display": "grid", "gridTemplateColumns": "1.2fr 1fr 1fr", "gap": "24px"}, children=[
                    html.Div(style={**CARD, "marginBottom": "0"}, children=[
                        html.H3("Dinámica de la Pobreza en el Tiempo", style={"fontFamily": "'Playfair Display', serif", "fontSize": "1.4rem", "marginBottom": "12px", "color": "#1A1A1A"}),
                        html.P(
                            "La reducción de la pobreza multidimensional requiere políticas de Estado sostenidas en el tiempo. "
                            "Al observar la evolución anual, podemos identificar si los departamentos están logrando avances constantes "
                            "o si enfrentan estancamientos y retrocesos ante crisis económicas, sociales o climáticas.",
                            style={"fontFamily": "'Source Serif 4', serif", "fontSize": "0.95rem", "color": "#4A4A4A", "lineHeight": "1.6", "marginBottom": "12px"}
                        ),
                        html.P(
                            "Una barra verde hacia la izquierda indica una disminución (mejora) en el IPM respecto al año anterior. "
                            "Una barra roja hacia la derecha señala un aumento (empeoramiento) en la incidencia de la pobreza "
                            "multidimensional en dicho territorio.",
                            style={"fontFamily": "'Source Serif 4', serif", "fontSize": "0.95rem", "color": "#4A4A4A", "lineHeight": "1.6"}
                        )
                    ]),
                    html.Div(style={**CARD, "background": "#E07B39", "color": "white", "marginBottom": "0"}, children=[
                        html.H3("Lectura de la Variación", style={"fontFamily": "'Playfair Display', serif", "fontSize": "1.2rem", "marginBottom": "14px", "color": "white"}),
                        html.Ul(style={"paddingLeft": "20px", "fontFamily": "'Source Serif 4', serif", "fontSize": "0.85rem", "lineHeight": "1.7", "color": "#FDF2EC"}, children=[
                            html.Li([html.B("Hacia la izquierda (Verde): ", style={"color": "white"}), "Reducción de la pobreza."]),
                            html.Li([html.B("Hacia la derecha (Rojo): ", style={"color": "white"}), "Aumento de la pobreza."]),
                            html.Li("Calculado en puntos porcentuales (pp)."),
                        ])
                    ]),
                    html.Div(style={**CARD, "background": "#FEF5F2", "borderLeft": "4px solid #E07B39", "marginBottom": "0"}, children=[
                        html.H3("Sensibilidad a las Crisis", style={"fontFamily": "'Playfair Display', serif", "fontSize": "1.2rem", "marginBottom": "14px", "color": "#E07B39"}),
                        html.P(
                            "El progreso social es frágil. Eventos como la pandemia del COVID-19 o fenómenos climáticos (El Niño) "
                            "tienen el potencial de borrar años de reducción de pobreza en América Latina en apenas meses. "
                            "La resiliencia de los territorios depende directamente de la robustez de sus instituciones locales.",
                            style={"fontFamily": "'Source Serif 4', serif", "fontSize": "0.85rem", "color": "#4A4A4A", "lineHeight": "1.7"}
                        )
                    ])
                ]),
                html.Div(style={"display": "flex", "gap": "16px", "marginBottom": "20px"}, children=[
                    html.Div(className="ctrl-group", children=[
                        html.Label("Seleccionar territorio histórico", className="ctrl-label"),
                        dcc.Dropdown(id="dd-dpto-evolucion",
                            options=opciones_dptos_evol,
                            value="Nacional", clearable=False,
                            style={"width": "300px", "fontFamily": "Georgia,serif"}
                        )
                    ]),
                ]),
                html.Div(style=CARD, children=[
                    html.P("Histórico de Pobreza (2018–2025)", className="section-tag"),
                    dcc.Graph(id="g-line-evolucion", config={"displayModeBar": False})
                ]),
                html.Div(style=CARD, children=[
                    html.P("Cambio respecto al año anterior", className="section-tag"),
                    html.Div(id="nar-comp", style={"marginBottom": "12px"}),
                    dcc.Graph(id="g-comp", config={"displayModeBar": False})
                ]),
                # Footer
                html.Div(style={"textAlign": "center", "paddingTop": "8px"}, children=[
                    html.P("Fuente: DANE · ECV 2024–2025 · Proyecciones CNPV 2018",
                           style={"fontFamily": "'DM Mono',monospace", "fontSize": "0.72rem",
                                  "color": C["muted"], "letterSpacing": "0.06em"})
                ]),
            ]),
        ]),

        # ══════════════════════════════════════════════════
        # SECCIÓN 6 — Brecha por género
        # ══════════════════════════════════════════════════
        html.Div(id="sec-genero", className="section-panel", children=[
            page_header(
                "BRECHA POR GÉNERO · 2018–2025",
                "¿Ser mujer cambia la probabilidad de vivir en pobreza?",
                "En Colombia, el sexo del jefe de hogar no es neutral: "
                "los hogares liderados por mujeres concentran brechas adicionales "
                "en acceso a agua, saneamiento y otros indicadores de privación. "
                "Esta sección desagrega la privación por sexo en cada departamento."
            ),
            html.Div(style={"padding": "0 48px 48px"}, children=[
                html.Div(style={"marginBottom": "32px", "display": "grid", "gridTemplateColumns": "1.2fr 1fr 1fr", "gap": "24px"}, children=[
                    html.Div(style={**CARD, "marginBottom": "0"}, children=[
                        html.H3("La Dimensión de Género en la Pobreza", style={"fontFamily": "'Playfair Display', serif", "fontSize": "1.4rem", "marginBottom": "12px", "color": "#1A1A1A"}),
                        html.P(
                            "La pobreza no es neutral al género. Los hogares con jefatura femenina suelen enfrentar mayores barreras debido a "
                            "la desigualdad salarial, la carga desproporcionada del trabajo de cuidado no remunerado y el acceso limitado a activos productivos.",
                            style={"fontFamily": "'Source Serif 4', serif", "fontSize": "0.95rem", "color": "#4A4A4A", "lineHeight": "1.6", "marginBottom": "12px"}
                        ),
                        html.P(
                            "Al analizar los indicadores con perspectiva de género, "
                            "podemos visibilizar cómo el hecho de ser mujer agrava las vulnerabilidades preexistentes, especialmente en la ruralidad.",
                            style={"fontFamily": "'Source Serif 4', serif", "fontSize": "0.95rem", "color": "#4A4A4A", "lineHeight": "1.6"}
                        )
                    ]),
                    html.Div(style={**CARD, "background": "#C94A17", "color": "white", "marginBottom": "0"}, children=[
                        html.H3("Conceptos Clave", style={"fontFamily": "'Playfair Display', serif", "fontSize": "1.2rem", "marginBottom": "14px", "color": "white"}),
                        html.Ul(style={"paddingLeft": "20px", "fontFamily": "'Source Serif 4', serif", "fontSize": "0.85rem", "lineHeight": "1.7", "color": "#FFF0ED"}, children=[
                            html.Li([html.B("Jefatura Femenina: ", style={"color": "white"}), "Hogares donde la principal responsable económica es una mujer."]),
                            html.Li([html.B("Doble Vulnerabilidad: ", style={"color": "white"}), "Cruzar las brechas territoriales con desigualdades de género."]),
                        ])
                    ]),
                    html.Div(style={**CARD, "background": "#FDF2EC", "borderLeft": "4px solid #B5341A", "marginBottom": "0"}, children=[
                        html.H3("Feminización de la Pobreza", style={"fontFamily": "'Playfair Display', serif", "fontSize": "1.2rem", "marginBottom": "14px", "color": "#B5341A"}),
                        html.P(
                            "De acuerdo con la CEPAL, por cada 100 hombres viviendo en pobreza en América Latina, hay aproximadamente 118 mujeres. "
                            "Este índice de feminidad de la pobreza es impulsado por la informalidad laboral y la economía del cuidado, "
                            "atrapando a las mujeres en un ciclo de dependencia y exclusión económica.",
                            style={"fontFamily": "'Source Serif 4', serif", "fontSize": "0.85rem", "color": "#4A4A4A", "lineHeight": "1.7"}
                        )
                    ])
                ]),
                SECCION_GENERO_LAYOUT,
            ]),
        ]),

    ])  # /main-content
])


# ══════════════════════════════════════════════════════════════════
# CALLBACK 1: Solo IPM — se dispara con dd-cat y dd-anio
# ══════════════════════════════════════════════════════════════════
@app.callback(
    Output("kpis",       "children"),
    Output("nar-mapa",   "children"),
    Output("nar-brecha", "children"),
    Output("nar-rank",   "children"),
    Output("nar-region", "children"),
    Output("nar-comp",   "children"),
    Output("mapa",       "figure"),
    Output("g-brecha",   "figure"),
    Output("g-rank",     "figure"),
    Output("g-region",   "figure"),
    Output("g-comp",     "figure"),
    Input("dd-cat",  "value"),
    Input("dd-anio", "value"),
    Input("dd-orden-brecha", "value"),
    Input("dd-sentido-brecha", "value"),
)
def actualizar_ipm(categoria, anio, orden_zona, sentido):
    df      = imp_dpto[(imp_dpto["Año"] == anio) & (imp_dpto["Categoria"] == categoria)].copy()
    df_tot  = imp_dpto[(imp_dpto["Año"] == anio) & (imp_dpto["Categoria"] == "Total")].copy()
    df_ant  = imp_dpto[(imp_dpto["Año"] == anio - 1) & (imp_dpto["Categoria"] == categoria)].copy()

    nacional   = df_tot["IPM"].mean()
    peor_dpto  = df.loc[df["IPM"].idxmax(), "nombre_dpto"]
    peor_val   = df["IPM"].max()
    mejor_dpto = df.loc[df["IPM"].idxmin(), "nombre_dpto"]
    mejor_val  = df["IPM"].min()

    n_dptos_criticos = (df["IPM"] > nacional).sum()

    # ── KPIs ──────────────────────────────────────────────────────
    def kpi(n, lbl, color="#B5341A"):
        return html.Div(className="kpi-card", style={"borderLeftColor": color}, children=[
            html.Div(n, className="kpi-num", style={"color": color}),
            html.Div(lbl, className="kpi-label"),
        ])

    kpis = [
        kpi(f"{nacional:.1f}%", f"IPM Promedio · {anio}"),
        kpi(f"{peor_val:.1f}%", f"Mayor privación: {peor_dpto}"),
        kpi(f"{mejor_val:.1f}%", f"Menor privación: {mejor_dpto}", color="#2D6A4F"),
        kpi(f"{n_dptos_criticos}", f"Territorios sobre el promedio"),
    ]

    # ── Narrativa mapa ─────────────────────────────────────────────
    nar_mapa = [
        html.Div([
            f"En {anio}, el IPM nacional ({categoria.lower()}) promedia ",
            html.B(f"{nacional:.1f}%", style={"color": "#1A1A1A"}),
            f". ", html.B(peor_dpto, style={"color": "#B5341A"}), " lidera con ",
            html.B(f"{peor_val:.1f}%", style={"color": "#B5341A"}),
            f", mientras ", html.B(mejor_dpto, style={"color": "#2D6A4F"}),
            " registra el valor más bajo: ", html.B(f"{mejor_val:.1f}%", style={"color": "#2D6A4F"}), "."
        ], className="insight"),
        html.P(
            "Las zonas más oscuras del mapa concentran comunidades indígenas, "
            "afrodescendientes y poblaciones rurales que históricamente han permanecido "
            "al margen de la inversión social del Estado.",
            style={"fontFamily": "'Source Serif 4',serif", "fontSize": "0.88rem",
                   "color": C["muted"], "lineHeight": "1.65"}
        )
    ]

    # ── MAPA ──────────────────────────────────────────────────────
    geom = geo_dpto.merge(df, on="cod_dpto").set_index("nombre_dpto")
    fig_mapa = px.choropleth_map(
        geom, geojson=geom.geometry, locations=geom.index,
        color="IPM", color_continuous_scale="OrRd",
        range_color=(0, geom["IPM"].max()),
        center={"lat": 4.5709, "lon": -74.2973}, zoom=4,
        map_style="carto-positron",
        labels={"IPM": "IPM (%)"},
        hover_name=geom.index, hover_data={"IPM": ":.1f"}
    )
    fig_mapa.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=430,
        coloraxis_colorbar=dict(title="IPM %", thickness=12, len=0.7)
    )

    # ── BRECHA campo/ciudad (IPM) ──────────────────────────────────
    cats_all = imp_dpto[imp_dpto["Año"] == anio]["Categoria"].unique().tolist()
    df_brecha = imp_dpto[
        (imp_dpto["Año"] == anio) & (imp_dpto["Categoria"].isin(cats_all))
    ].groupby(["nombre_dpto", "Categoria"])["IPM"].mean().reset_index()

    # Ordenamiento dinámico basado en filtros
    df_pivot = df_brecha.pivot(index="nombre_dpto", columns="Categoria", values="IPM").reset_index()
    sort_col = orden_zona if orden_zona in df_pivot.columns else "Total"
    ascending = (sentido == "asc")
    df_pivot = df_pivot.sort_values(by=sort_col, ascending=ascending)
    top12 = df_pivot.head(12)["nombre_dpto"].tolist()
    
    df_brecha12 = df_brecha[df_brecha["nombre_dpto"].isin(top12)]

    pal_brecha = {
        "Total":  "#E8956D",
        "Cabecera": "#4A90D9",
        "Centros poblados  y rural disperso": C["green"],
    }
    fig_brecha = px.bar(
        df_brecha12, x="IPM", y="nombre_dpto", color="Categoria",
        barmode="group", orientation="h",
        color_discrete_map=pal_brecha,
        labels={"nombre_dpto": "", "IPM": "IPM (%)", "Categoria": "Zona"},
        text_auto=".1f",
        category_orders={"nombre_dpto": top12[::-1]}
    )
    fig_brecha.update_traces(textposition="outside", cliponaxis=False)
    fig_brecha.update_layout(
        **{**BASE_LAYOUT, "margin": dict(t=30, b=40, l=160, r=80)},
        height=650,
        legend=dict(orientation="h", y=1.06, x=0),
        xaxis=dict(range=[0, df_brecha12["IPM"].max() * 1.15]),
        yaxis=dict(autorange="reversed")
    )

    nar_brecha = html.Div([
        "En los departamentos más afectados, la diferencia entre ",
        html.B("zonas rurales", style={"color": C["green"]}), " y ",
        html.B("cabeceras", style={"color": "#4A90D9"}),
        " municipales es alarmante. Vivir en el campo implica enormes desventajas, siendo un ",
        html.Span("factor determinante de vulnerabilidad estructural", style={"background": "#FEE2E2", "color": "#B5341A", "padding": "2px 6px", "borderRadius": "4px", "fontWeight": "bold"}),
        "."
    ], className="insight")

    # ── RANKING horizontal ─────────────────────────────────────────
    top10 = df.nlargest(10, "IPM").sort_values("IPM")
    region_colors_bar = [
        REGION_COLORS.get(REGIONES.get(d, "Otra"), "#999999")
        for d in top10["nombre_dpto"]
    ]
    fig_rank = go.Figure(go.Bar(
        x=top10["IPM"],
        y=top10["nombre_dpto"],
        orientation="h",
        marker_color=region_colors_bar,
        text=top10["IPM"].map("{:.1f}%".format),
        textposition="outside",
        cliponaxis=False,
    ))
    fig_rank.update_layout(
        **BASE_LAYOUT,
        height=360,
        xaxis_title="IPM (%)", yaxis_title="",
        xaxis_range=[0, top10["IPM"].max() * 1.18],
        yaxis=dict(autorange="reversed")
    )

    nar_rank = html.Div([
        "Los departamentos con mayor IPM concentran las deudas históricas del Estado: ",
        html.B("acceso a agua, saneamiento y educación rural", style={"color": "#B5341A", "textDecoration": "underline"}),
        ". El color identifica la región a la que pertenece cada departamento."
    ], className="insight")

    # ── REGIONES ───────────────────────────────────────────────────
    df["region"] = df["nombre_dpto"].map(REGIONES).fillna("Otra")
    df_reg = df.groupby("region")["IPM"].mean().reset_index().sort_values("IPM", ascending=True)
    df_reg["color"] = df_reg["region"].map(REGION_COLORS)

    fig_region = go.Figure(go.Bar(
        x=df_reg["IPM"],
        y=df_reg["region"],
        orientation="h",
        marker_color=df_reg["color"],
        text=df_reg["IPM"].map("{:.1f}%".format),
        textposition="outside",
        cliponaxis=False,
    ))
    fig_region.update_layout(
        **BASE_LAYOUT,
        height=360,
        xaxis_title="IPM promedio (%)", yaxis_title="",
        xaxis_range=[0, df_reg["IPM"].max() * 1.2],
        yaxis=dict(autorange="reversed")
    )

    reg_max = df_reg.loc[df_reg["IPM"].idxmax(), "region"]
    reg_max_val = df_reg["IPM"].max()
    reg_min = df_reg.loc[df_reg["IPM"].idxmin(), "region"]
    reg_min_val = df_reg["IPM"].min()

    nar_region = html.Div([
        f"La región ", html.B(reg_max), f" registra el IPM más alto (",
        html.B(f"{reg_max_val:.1f}%", style={"color": "#B5341A"}), "), casi ",
        html.Span(f"{reg_max_val/reg_min_val:.1f} veces", style={"background": "#FCE8E6", "color": "#B5341A", "padding": "2px 6px", "borderRadius": "4px", "fontWeight": "bold"}),
        f" el de ", html.B(reg_min), f" ({reg_min_val:.1f}%). ",
        "Esta brecha regional refleja décadas de inversión pública desigual entre el centro y la periferia."
    ], className="insight")

    # ── CAMBIO AÑO ANTERIOR ────────────────────────────────────────
    if not df_ant.empty:
        df_comp = df_ant[["nombre_dpto", "IPM"]].rename(columns={"IPM": "ant"}).merge(
            df[["nombre_dpto", "IPM"]].rename(columns={"IPM": "act"}), on="nombre_dpto"
        )
        df_comp["delta"] = df_comp["act"] - df_comp["ant"]
        df_comp = df_comp.sort_values("delta", ascending=True)

        colors_delta = [C["green"] if d < 0 else C["accent"] for d in df_comp["delta"]]

        fig_comp = go.Figure(go.Bar(
            x=df_comp["delta"],
            y=df_comp["nombre_dpto"],
            orientation="h",
            marker_color=colors_delta,
            text=df_comp["delta"].map("{:+.1f}".format),
            textposition="outside",
            cliponaxis=False,
        ))
        fig_comp.add_vline(x=0, line_dash="dot", line_color="#999", line_width=1)
        fig_comp.update_layout(
            **{**BASE_LAYOUT, "margin": dict(t=30, b=40, l=180, r=80)},
            height=620,
            xaxis_title="Variación en puntos porcentuales",
            yaxis_title="",
            yaxis=dict(autorange="reversed"),
            shapes=[dict(
                type="rect", xref="x", yref="paper",
                x0=df_comp["delta"].min() * 1.01, x1=0,
                y0=0, y1=1,
                fillcolor="rgba(45,106,79,0.04)", line_width=0,
            ), dict(
                type="rect", xref="x", yref="paper",
                x0=0, x1=df_comp["delta"].max() * 1.01,
                y0=0, y1=1,
                fillcolor="rgba(181,52,26,0.04)", line_width=0,
            )]
        )

        mejoras = (df_comp["delta"] < 0).sum()
        empeoró = (df_comp["delta"] > 0).sum()
        nar_comp = html.Div([
            f"Entre {anio-1} y {anio}, ",
            html.Span(f"↓ {mejoras} redujeron su IPM", style={"color": "#2D6A4F", "fontWeight": "bold", "background": "#E6F4EA", "padding": "2px 6px", "borderRadius": "4px", "marginRight": "4px"}),
            " y ",
            html.Span(f"↑ {empeoró} lo aumentaron", style={"color": "#B5341A", "fontWeight": "bold", "background": "#FCE8E6", "padding": "2px 6px", "borderRadius": "4px", "marginLeft": "4px"}),
            ". Los avances no son uniformes ni garantizados: mientras algunas regiones avanzan, otras retroceden."
        ], className="insight")
    else:
        fig_comp = go.Figure()
        fig_comp.update_layout(**BASE_LAYOUT, height=400)
        nar_comp = html.Div("No hay datos del año anterior disponibles.", className="insight")

    return (kpis, nar_mapa, nar_brecha, nar_rank, nar_region, nar_comp,
            fig_mapa, fig_brecha, fig_rank, fig_region, fig_comp)


# ══════════════════════════════════════════════════════════════════
# CALLBACK 2: Solo indicadores — se dispara con dd-indicador-agua y dd-dpto-agua
# ══════════════════════════════════════════════════════════════════
@app.callback(
    Output("g-agua",           "figure"),
    Output("insight-agua",     "children"),
    Output("seccion-tag-agua", "children"),
    Output("titulo-agua",      "children"),
    Output("subtitulo-agua",   "children"),
    Output("fuente-agua",      "children"),
    Input("dd-indicador-agua", "value"),
    Input("dd-dpto-agua",      "value"),
)
def actualizar_indicador(indicador_agua, dpto_agua):
    _cache           = CACHE_IND[indicador_agua]
    df_agua_nac_sel  = _cache["nac"]
    df_agua_dpto_sel = _cache["dpto"]

    fig_agua = build_fig_agua(dpto_agua, df_agua_nac_sel, df_agua_dpto_sel, indicador_agua)

    fuente = df_agua_nac_sel if dpto_agua == "Nacional" else df_agua_dpto_sel[
        df_agua_dpto_sel["nombre_dpto"] == dpto_agua
    ][["Año", "zona", "pct"]]

    if not fuente.empty:
        anio_max_agua = int(fuente["Año"].max())
        vr_s = fuente.loc[(fuente["Año"] == anio_max_agua) & (fuente["zona"] == "Rural disperso"), "pct"]
        vc_s = fuente.loc[(fuente["Año"] == anio_max_agua) & (fuente["zona"] == "Cabecera"), "pct"]
        if vc_s.empty:
            vc_s = fuente.loc[(fuente["Año"] == anio_max_agua) & (fuente["zona"] == "Total"), "pct"]
            ref_label = "el promedio total"
        else:
            ref_label = "cabeceras municipales"

        if not vr_s.empty and not vc_s.empty:
            vr, vc = vr_s.values[0], vc_s.values[0]
            brecha = vr - vc
            ctx = "nacional" if dpto_agua == "Nacional" else f"en {dpto_agua}"

            UMBRAL = 0.5  # diferencia mínima considerada significativa (pp)

            if abs(brecha) < UMBRAL:
                # Brecha nula o despreciable
                insight_agua = (
                    f"En {anio_max_agua}, la privación en '{indicador_agua}' es prácticamente "
                    f"igual entre zonas rurales dispersas ({vr:.1f}%) y {ref_label} ({vc:.1f}%) {ctx}. "
                    f"Una diferencia de apenas {brecha:+.1f} pp indica que este indicador "
                    f"no presenta brecha territorial significativa en este período."
                )
            elif brecha > 0:
                # Rural peor que urbano (caso habitual)
                insight_agua = (
                    f"En {anio_max_agua}, el {vr:.1f}% de hogares rurales dispersos {ctx} presentaba privación "
                    f"en '{indicador_agua}', frente al {vc:.1f}% en {ref_label}. "
                    f"Una brecha de {brecha:+.1f} pp que penaliza al campo: "
                    f"vivir fuera de la cabecera sigue siendo un factor de desventaja estructural."
                )
            else:
                # Urbano peor que rural (brecha invertida)
                insight_agua = (
                    f"En {anio_max_agua}, la privación en '{indicador_agua}' es mayor en {ref_label} "
                    f"({vc:.1f}%) que en zonas rurales dispersas ({vr:.1f}%) {ctx}. "
                    f"Una brecha invertida de {brecha:+.1f} pp: en este indicador, "
                    f"las zonas urbanas presentan mayor privación que el campo."
                )
        else:
            insight_agua = "No se encontraron datos suficientes para calcular la brecha."
    else:
        insight_agua = "No se encontraron datos suficientes para calcular la brecha."

    textos = TEXTOS_INDICADOR.get(indicador_agua, {
        "tag":       f"{indicador_agua.upper()} · 2018–2025",
        "titulo":    f"Brecha en {indicador_agua} entre campo y ciudad.",
        "subtitulo": f"Evolución del indicador '{indicador_agua}' por zona geográfica.",
        "fuente":    f"Fuente: DANE · ECV 2018–2025. Hogares con privación: {indicador_agua}.",
    })

    return (fig_agua, insight_agua,
            textos["tag"], textos["titulo"], textos["subtitulo"], textos["fuente"])


# ══════════════════════════════════════════════════════════════════
# CALLBACK 3: Género — se dispara con dd-dpto-genero
# ══════════════════════════════════════════════════════════════════
@app.callback(
    Output("g-genero-evol",            "figure"),
    Output("g-genero-dpto",            "figure"),
    Output("insight-genero",           "children"),
    Output("insight-disparidad-genero","children"),
    Input("dd-dpto-genero",            "value"),
)
def actualizar_genero(dpto_sel):
    # ── Gráfico 1: evolución temporal ────────────────────────────
    fig_evol = build_fig_genero(dpto_sel)

    # ── Gráfico 2: disparidad por departamento ───────────────────
    fig_dpto, anio_max_dpto, df_pivot = build_fig_disparidad_dpto()

    # ── Insight: evolución ────────────────────────────────────────
    if dpto_sel == "Nacional":
        df_plot = df_sexo.groupby(["Año", "Sexo"])["Valor"].mean().reset_index()
    else:
        df_plot = df_sexo[df_sexo["nombre_dpto"] == dpto_sel][["Año", "Sexo", "Valor"]].copy()

    insight_evol = "No se encontraron datos suficientes para calcular la brecha de género."
    if not df_plot.empty:
        anio_max_evol = int(df_plot["Año"].max())
        val_m = df_plot.loc[(df_plot["Año"] == anio_max_evol) & (df_plot["Sexo"] == "Mujer"),  "Valor"]
        val_h = df_plot.loc[(df_plot["Año"] == anio_max_evol) & (df_plot["Sexo"] == "Hombre"), "Valor"]
        if not val_m.empty and not val_h.empty:
            vm, vh = val_m.values[0], val_h.values[0]
            brecha = vm - vh
            ctx = "a nivel nacional" if dpto_sel == "Nacional" else f"en {dpto_sel}"
            UMBRAL = 0.5

            if abs(brecha) < UMBRAL:
                insight_evol = (
                    f"En {anio_max_evol}, la privación es prácticamente igual entre hogares con jefa mujer "
                    f"({vm:.1f}%) y hogares con jefe hombre ({vh:.1f}%) {ctx}. "
                    f"La brecha de género ({brecha:+.1f} pp) no es estadísticamente significativa "
                    "en este indicador para este período."
                )
            elif brecha > 0:
                insight_evol = (
                    f"En {anio_max_evol}, los hogares con jefa mujer {ctx} presentaban una privación "
                    f"del {vm:.1f}%, frente al {vh:.1f}% en hogares con jefe hombre. "
                    f"Una brecha de {brecha:+.1f} pp que refleja la doble vulnerabilidad de las mujeres: "
                    "además de las carencias territoriales, acumulan desventajas de género en el acceso "
                    "a recursos básicos."
                )
            else:
                insight_evol = (
                    f"En {anio_max_evol}, los hogares liderados por hombres presentaban mayor privación "
                    f"({vh:.1f}%) que los liderados por mujeres ({vm:.1f}%) {ctx}. "
                    f"Una brecha invertida de {brecha:+.1f} pp que puede reflejar patrones de "
                    "jefatura femenina concentrados en zonas urbanas o con mayor acceso a redes de apoyo."
                )

    # ── Insight: disparidad por departamento ─────────────────────
    insight_disp = "No hay datos suficientes para calcular la disparidad por departamento."
    if not df_pivot.empty:
        idx_max = df_pivot["brecha"].idxmax()
        idx_min = df_pivot["brecha"].idxmin()
        dpto_mayor  = df_pivot.loc[idx_max, "nombre_dpto"]
        brecha_mayor = df_pivot.loc[idx_max, "brecha"]
        dpto_menor  = df_pivot.loc[idx_min, "nombre_dpto"]
        brecha_menor = df_pivot.loc[idx_min, "brecha"]
        n_adv_mujer = (df_pivot["brecha"] > 0.5).sum()
        n_adv_hombre = (df_pivot["brecha"] < -0.5).sum()

        insight_disp = (
            f"En {anio_max_dpto}, {dpto_mayor} registra la mayor desventaja para hogares liderados "
            f"por mujeres ({brecha_mayor:+.1f} pp). "
            f"{dpto_menor} presenta la mayor desventaja para hogares liderados por hombres "
            f"({brecha_menor:+.1f} pp). "
            f"En total, {n_adv_mujer} departamentos muestran mayor privación en hogares con jefa mujer "
            f"y {n_adv_hombre} en hogares con jefe hombre. "
            "Las barras rojas indican que las mujeres están en desventaja; las azules, los hombres."
        )

    return fig_evol, fig_dpto, insight_evol, insight_disp


# ══════════════════════════════════════════════════════════════════
# CALLBACK NUEVO: Evolución Anual Línea Histórica
# ══════════════════════════════════════════════════════════════════
@app.callback(
    Output("g-line-evolucion", "figure"),
    Input("dd-dpto-evolucion", "value")
)
def actualizar_linea_evolucion(dpto):
    df_filtrado = imp_dpto.copy()
    
    # Calcular promedios según selección
    if dpto == "Nacional":
        df_plot = df_filtrado.groupby(["Año", "Categoria"])["IPM"].mean().reset_index()
    else:
        df_plot = df_filtrado[df_filtrado["nombre_dpto"] == dpto]
    
    # Obtener valores para Cabecera, Rural y Total
    # Usamos contains por las ligeras diferencias de nombres
    df_cab = df_plot[df_plot["Categoria"].str.contains("Cabecera", case=False, na=False)].sort_values("Año")
    df_rur = df_plot[df_plot["Categoria"].str.contains("rural disperso", case=False, na=False)].sort_values("Año")
    df_tot = df_plot[df_plot["Categoria"].str.contains("Total", case=False, na=False)].sort_values("Año")
    
    fig = go.Figure()
    
    # Área de fondo para Rural Disperso
    if not df_rur.empty:
        fig.add_trace(go.Scatter(
            x=list(df_rur["Año"]) + list(df_rur["Año"])[::-1],
            y=list(df_rur["IPM"]) + [0] * len(df_rur),
            fill="toself",
            fillcolor="rgba(201, 74, 23, 0.08)",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip"
        ))
    
    # Trace 1: Cabecera
    fig.add_trace(go.Scatter(
        x=df_cab["Año"], y=df_cab["IPM"],
        mode="lines+markers+text",
        name="Cabecera",
        line=dict(color=PALETA_AGUA["Cabecera"], width=ANCHO_AGUA["Cabecera"], dash=DASH_AGUA["Cabecera"]),
        marker=dict(size=10, symbol=SIMBOLO_AGUA["Cabecera"], color=PALETA_AGUA["Cabecera"], line=dict(width=1.5, color="white")),
        text=df_cab["IPM"].map("{:.1f}%".format),
        textposition="top center",
        textfont=dict(family="DM Mono, monospace", size=10, color=PALETA_AGUA["Cabecera"])
    ))
    
    # Trace 2: Rural Disperso
    fig.add_trace(go.Scatter(
        x=df_rur["Año"], y=df_rur["IPM"],
        mode="lines+markers+text",
        name="Rural Disperso",
        line=dict(color=PALETA_AGUA["Rural disperso"], width=ANCHO_AGUA["Rural disperso"], dash=DASH_AGUA["Rural disperso"]),
        marker=dict(size=10, symbol=SIMBOLO_AGUA["Rural disperso"], color=PALETA_AGUA["Rural disperso"], line=dict(width=1.5, color="white")),
        text=df_rur["IPM"].map("{:.1f}%".format),
        textposition="top center",
        textfont=dict(family="DM Mono, monospace", size=10, color=PALETA_AGUA["Rural disperso"])
    ))
    
    # Trace 3: Total
    fig.add_trace(go.Scatter(
        x=df_tot["Año"], y=df_tot["IPM"],
        mode="lines+markers+text",
        name="Total",
        line=dict(color=PALETA_AGUA["Total"], width=ANCHO_AGUA["Total"], dash=DASH_AGUA["Total"]),
        marker=dict(size=10, symbol=SIMBOLO_AGUA["Total"], color=PALETA_AGUA["Total"], line=dict(width=1.5, color="white")),
        text=df_tot["IPM"].map("{:.1f}%".format),
        textposition="top center",
        textfont=dict(family="DM Mono, monospace", size=10, color=PALETA_AGUA["Total"])
    ))
    
    # Añadir línea vertical y etiqueta para la brecha en el año más reciente
    if not df_rur.empty and not df_cab.empty:
        anio_max = df_tot["Año"].max()
        val_rur = df_rur.loc[df_rur["Año"] == anio_max, "IPM"]
        val_cab = df_cab.loc[df_cab["Año"] == anio_max, "IPM"]
        if not val_rur.empty and not val_cab.empty:
            vr = val_rur.values[0]
            vc = val_cab.values[0]
            fig.add_shape(
                type="line",
                x0=anio_max, x1=anio_max,
                y0=vc, y1=vr,
                line=dict(color=PALETA_AGUA["Rural disperso"], width=1.5, dash="dot")
            )
            fig.add_annotation(
                x=anio_max, y=(vr + vc)/2,
                text=f"Brecha:<br><b>+{vr - vc:.1f} pp</b>",
                showarrow=False,
                xanchor="left", xshift=10,
                font=dict(family="'DM Mono', monospace", size=11, color=PALETA_AGUA["Rural disperso"]),
                bgcolor="rgba(255,255,255,0.8)", bordercolor=PALETA_AGUA["Rural disperso"], borderwidth=1, borderpad=3
            )
    
    titulo_dpto = "Promedio Nacional" if dpto == "Nacional" else dpto
    
    _layout = BASE_LAYOUT.copy()
    _layout.update(
        height=460,
        margin=dict(t=50, b=150, l=60, r=80),
        xaxis=dict(
            title=dict(text="Año", font=dict(size=11, color="#6B6B6B")),
            tickmode="array",
            tickvals=df_tot["Año"].tolist(),
            ticktext=[str(a) for a in df_tot["Año"].tolist()],
            tickfont=dict(family="DM Mono, monospace", size=11),
            showgrid=True,
            gridcolor="#F0EBE3",
            gridwidth=1,
            zeroline=False,
        ),
        yaxis=dict(
            title=dict(text=f"IPM: {titulo_dpto}", font=dict(size=11, color="#6B6B6B")),
            ticksuffix="%",
            tickfont=dict(family="DM Mono, monospace", size=11),
            showgrid=True,
            gridcolor="#F0EBE3",
            gridwidth=1,
            zeroline=False,
            rangemode="tozero",
        ),
        legend=dict(
            orientation="h",
            y=-0.55,
            x=0.5,
            xanchor="center",
            font=dict(family="Source Serif 4, serif", size=12),
            bgcolor="rgba(0,0,0,0)",
            itemwidth=80,
        ),
        hovermode="x unified"
    )
    fig.update_layout(**_layout)
    
    return fig


# ══════════════════════════════════════════════════════════════════
# CALLBACK NUEVO: Waffle Chart (100 Personas)
# ══════════════════════════════════════════════════════════════════
@app.callback(
    Output("text-waffle", "children"),
    Input("dd-waffle", "value"),
    Input("dd-anio", "value"),
    Input("dd-cat", "value")
)
def actualizar_waffle(indicador, anio, categoria):
    # Obtener el dataframe base para este indicador (promedio nacional por zona)
    df_nac = CACHE_IND[indicador]["nac"]
    
    # Mapear la categoría global al nombre interno del dataset de indicadores
    zona = "Total"
    if "cabecera" in categoria.lower():
        zona = "Cabecera"
    elif "rural" in categoria.lower() or "centros" in categoria.lower():
        zona = "Rural disperso"
        
    val_series = df_nac.loc[(df_nac["Año"] == anio) & (df_nac["zona"] == zona), "pct"]
    
    if val_series.empty:
        return html.P("No hay datos disponibles para esta selección.")
        
    val = float(val_series.values[0])
    num_afectados = int(round(val))
            
    # Generar el texto narrativo
    texto_narrativo = html.Div([
        f"En el año {anio}, si tomamos una muestra representativa de ",
        html.B("100 personas"),
        f" en la categoría ",
        html.B(categoria.lower()),
        f", aproximadamente ",
        html.Span(f"{num_afectados}", style={"color": "#B5341A", "fontWeight": "900", "fontSize": "1.4rem"}),
        " sufren privación por ",
        html.B(indicador.lower()),
        "."
    ])
    
    return texto_narrativo


# Exponer el servidor Flask subyacente (necesario para Gunicorn/Render)
server = app.server

# ── Entry point ────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)