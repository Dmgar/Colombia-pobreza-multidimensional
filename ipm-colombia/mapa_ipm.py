"""
IPM Colombia — Dashboard de Pobreza Multidimensional
Fuente: DANE · Encuesta de Calidad de Vida (ECV)
"""

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd

# ── Rutas de datos (ajusta según tu equipo) ────────────────────────
GEO_PATH = r"C:\Users\darye\Downloads\MGN2024_DPTO_POLITICO.zip"
CSV_PATH = r"C:\Users\darye\OneDrive\Escritorio\EDITORES_ABIERTOS\ipm_dpto.csv"

# ── Mapeo de departamentos a regiones ─────────────────────────────
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

# ── Colores y estilos ──────────────────────────────────────────────
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
# Carga de datos
# ══════════════════════════════════════════════════════════════════
geo_dpto = gpd.read_file(GEO_PATH)
imp_dpto = pd.read_csv(CSV_PATH, dtype={"cod_dpto": "str"})
geo_dpto.rename(columns={"dpto_ccdgo": "cod_dpto"}, inplace=True)

imp_dpto["region"] = imp_dpto["nombre_dpto"].map(REGIONES).fillna("Otra")

categorias = imp_dpto["Categoria"].unique().tolist()
anios      = sorted(imp_dpto["Año"].unique().tolist())

# ══════════════════════════════════════════════════════════════════
# App Dash
# ══════════════════════════════════════════════════════════════════
app = Dash(__name__, title="IPM Colombia · DANE")

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
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #F7F4EF; }

        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
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

        @media(max-width:900px){
            .kpi-grid { grid-template-columns:1fr 1fr; }
            .two-col  { grid-template-columns:1fr; }
            .map-narrative { grid-template-columns:1fr; }
            .controls-row  { flex-direction:column; }
        }
    </style>
</head>
<body>{%app_entry%}{%config%}{%scripts%}{%renderer%}</body>
</html>
"""

# ── Layout ─────────────────────────────────────────────────────────
app.layout = html.Div(style={"background": C["bg"], "minHeight": "100vh"}, children=[

    # HEADER
    html.Div(style={
        "background": C["text"], "color": "white",
        "padding": "48px 60px 40px", "marginBottom": "32px"
    }, children=[
        html.P("DANE · Encuesta de Calidad de Vida",
               className="section-tag", style={"color": "#B5341A", "marginBottom": "12px"}),
        html.H1("¿Dónde vive la pobreza en Colombia?",
                style={"fontFamily": "'Playfair Display',serif",
                       "fontSize": "clamp(2rem,4vw,3.2rem)",
                       "fontWeight": "900", "lineHeight": "1.1", "marginBottom": "16px"}),
        html.P(
            "El Índice de Pobreza Multidimensional (IPM) mide carencias en salud, educación "
            "y condiciones de vida. Esta exploración revela que la geografía sigue siendo "
            "destino en Colombia: nacer en la Amazonía o el Pacífico multiplica hasta 7 veces "
            "la probabilidad de vivir en pobreza multidimensional.",
            style={"fontFamily": "'Source Serif 4',serif", "fontSize": "1.05rem",
                   "color": "#B0B0B0", "maxWidth": "680px", "lineHeight": "1.7"}
        ),
    ]),

    html.Div(style={"padding": "0 60px 60px"}, children=[

        # CONTROLES
        html.Div(style={**CARD, "padding": "18px 28px"}, children=[
            html.Div(className="controls-row", children=[
                html.Div(className="ctrl-group", children=[
                    html.Label("Categoría de zona", className="ctrl-label"),
                    dcc.Dropdown(id="dd-cat",
                        options=[{"label": c, "value": c} for c in categorias],
                        value="Total", clearable=False,
                        style={"width": "360px", "fontFamily": "Georgia,serif"})
                ]),
                html.Div(className="ctrl-group", children=[
                    html.Label("Año", className="ctrl-label"),
                    dcc.Dropdown(id="dd-anio",
                        options=[{"label": str(a), "value": a} for a in anios],
                        value=max(anios), clearable=False,
                        style={"width": "120px", "fontFamily": "Georgia,serif"})
                ]),
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
                    html.P("Lectura del mapa", className="section-tag"),
                    html.Div(id="nar-mapa"),
                ], style={"paddingTop": "24px"})
            ])
        ]),

        # BRECHA CAMPO / CIUDAD
        html.Div(style=CARD, children=[
            html.P("La brecha campo–ciudad", className="section-tag"),
            html.Div(id="nar-brecha", style={"marginBottom": "16px"}),
            dcc.Graph(id="g-brecha", config={"displayModeBar": False})
        ]),

        # RANKING (horizontal) + REGIONES
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

        # CAMBIO AÑO ANTERIOR — horizontal, full-width
        html.Div(style=CARD, children=[
            html.P("Cambio respecto al año anterior", className="section-tag"),
            html.Div(id="nar-comp", style={"marginBottom": "12px"}),
            dcc.Graph(id="g-comp", config={"displayModeBar": False})
        ]),

        # FOOTER
        html.Div(style={"textAlign": "center", "paddingTop": "16px"}, children=[
            html.P("Fuente: DANE · ECV 2024-2025 · Proyecciones CNPV 2018",
                   style={"fontFamily": "'DM Mono',monospace", "fontSize": "0.72rem",
                          "color": C["muted"], "letterSpacing": "0.06em"})
        ])
    ])
])


# ══════════════════════════════════════════════════════════════════
# Callback principal
# ══════════════════════════════════════════════════════════════════
@app.callback(
    Output("kpis",      "children"),
    Output("nar-mapa",  "children"),
    Output("nar-brecha","children"),
    Output("nar-rank",  "children"),
    Output("nar-region","children"),
    Output("nar-comp",  "children"),
    Output("mapa",      "figure"),
    Output("g-brecha",  "figure"),
    Output("g-rank",    "figure"),
    Output("g-region",  "figure"),
    Output("g-comp",    "figure"),
    Input("dd-cat",  "value"),
    Input("dd-anio", "value"),
)
def actualizar(categoria, anio):
    df      = imp_dpto[(imp_dpto["Año"] == anio) & (imp_dpto["Categoria"] == categoria)].copy()
    df_tot  = imp_dpto[(imp_dpto["Año"] == anio) & (imp_dpto["Categoria"] == "Total")].copy()
    df_ant  = imp_dpto[(imp_dpto["Año"] == anio - 1) & (imp_dpto["Categoria"] == categoria)].copy()

    nacional  = df_tot["IPM"].mean()
    peor_dpto = df.loc[df["IPM"].idxmax(), "nombre_dpto"]
    peor_val  = df["IPM"].max()
    mejor_dpto= df.loc[df["IPM"].idxmin(), "nombre_dpto"]
    mejor_val = df["IPM"].min()

    # ── KPIs ──────────────────────────────────────────────────────
    def kpi(n, lbl):
        return html.Div(className="kpi-card", children=[
            html.Div(n, className="kpi-num"),
            html.Div(lbl, className="kpi-label"),
        ])

    kpis = [
        kpi(f"{nacional:.1f}%", f"IPM Nacional promedio · {anio}"),
        kpi(f"{peor_val:.1f}%", f"Más afectado: {peor_dpto}"),
        kpi(f"{peor_val/mejor_val:.1f}×", f"Brecha {peor_dpto} vs {mejor_dpto}"),
    ]

    # ── Narrativa mapa ─────────────────────────────────────────────
    nar_mapa = [
        html.Div(
            f"En {anio}, el IPM nacional ({categoria.lower()}) promedia {nacional:.1f}%. "
            f"{peor_dpto} lidera con {peor_val:.1f}%, mientras {mejor_dpto} "
            f"registra el valor más bajo: {mejor_val:.1f}%.",
            className="insight"
        ),
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

    # ── BRECHA campo/ciudad ────────────────────────────────────────
    cats_all = imp_dpto[imp_dpto["Año"] == anio]["Categoria"].unique().tolist()
    df_brecha = imp_dpto[
        (imp_dpto["Año"] == anio) & (imp_dpto["Categoria"].isin(cats_all))
    ].groupby(["nombre_dpto", "Categoria"])["IPM"].mean().reset_index()

    top12 = df_tot.nlargest(12, "IPM")["nombre_dpto"].tolist()
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
        text_auto=".1f"
    )
    fig_brecha.update_layout(
        **{**BASE_LAYOUT, "margin": dict(t=30, b=40, l=160, r=60)},
        height=400,
        legend=dict(orientation="h", y=1.06, x=0),
        yaxis=dict(autorange="reversed")
    )

    nar_brecha = html.Div(
        "En los departamentos más pobres, la diferencia entre zonas rurales y cabeceras "
        "municipales puede superar 30 puntos porcentuales. Vivir en el campo "
        "no es solo una elección de vida: en Colombia, sigue siendo un factor "
        "determinante de vulnerabilidad estructural.",
        className="insight"
    )

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

    nar_rank = html.Div(
        "Los departamentos con mayor IPM concentran las deudas históricas del Estado: "
        "acceso a agua potable, saneamiento, educación rural y atención en salud. "
        "El color identifica la región a la que pertenece cada departamento.",
        className="insight"
    )

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

    nar_region = html.Div(
        f"La región {reg_max} registra el IPM más alto ({reg_max_val:.1f}%), "
        f"casi {reg_max_val/reg_min_val:.1f} veces el de {reg_min} ({reg_min_val:.1f}%). "
        "Esta brecha regional refleja décadas de inversión pública desigual "
        "entre el centro y la periferia del país.",
        className="insight"
    )

    # ── CAMBIO AÑO ANTERIOR — barras horizontales ──────────────────
    if not df_ant.empty:
        df_comp = df_ant[["nombre_dpto", "IPM"]].rename(columns={"IPM": "ant"}).merge(
            df[["nombre_dpto", "IPM"]].rename(columns={"IPM": "act"}), on="nombre_dpto"
        )
        df_comp["delta"] = df_comp["act"] - df_comp["ant"]
        df_comp = df_comp.sort_values("delta", ascending=True)   # mejor arriba

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
        nar_comp = html.Div(
            f"Entre {anio-1} y {anio}, {mejoras} departamentos redujeron su IPM "
            f"(verde, izquierda) y {empeoró} lo aumentaron (rojo, derecha). "
            "Los avances no son uniformes ni garantizados: mientras algunas regiones "
            "avanzan, otras retroceden.",
            className="insight"
        )
    else:
        fig_comp = go.Figure()
        fig_comp.update_layout(**BASE_LAYOUT, height=400)
        nar_comp = html.Div("No hay datos del año anterior disponibles.", className="insight")

    return (kpis, nar_mapa, nar_brecha, nar_rank, nar_region, nar_comp,
            fig_mapa, fig_brecha, fig_rank, fig_region, fig_comp)


# ── Entry point ────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)