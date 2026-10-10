"""
Módulo de Contexto Regional, Pares Latinoamericanos y Análisis OCDE/CEPAL.
Proporciona curaduría de datos socioeconómicos internacionales, indicadores comparados
de pobreza multidimensional, desigualdad, informalidad y capital humano, junto con
figuras interactivas de Plotly y análisis de impacto en desarrollo poblacional.

Fuentes oficiales:
- OCDE: OECD Income Distribution Database, OECD Economic Surveys (Colombia 2024), SOCX Database.
- CEPAL: Panorama Social de América Latina y el Caribe, Base de Datos No Monetaria.
- PNUD / OPHI: Global Multidimensional Poverty Index.
- Banco Mundial: World Development Indicators, Human Capital Project.
"""

from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from figuras import BASE_LAYOUT, FUENTE_MONO, FUENTE_SERIF
from ui import C, CARD, panel_seccion, tag_seccion, titulo_seccion, subtitulo_seccion, caja_insight, nota_fuente

# ══════════════════════════════════════════════════════════════════
# DATOS REGIONALES CURADOS (PARES LATINOAMERICANOS & BENCHMARKS)
# ══════════════════════════════════════════════════════════════════
DATOS_PAISES = {
    "Colombia": {
        "codigo": "COL",
        "bandera": "COL",
        "bloque": "Miembro OCDE (2020) · Alianza del Pacífico",
        "ipm_nacional": 12.1,
        "ipm_rural": 27.3,
        "brecha_rural_urbana": 18.4,
        "pobreza_relativa_ocde": 20.8,
        "gini": 0.548,
        "informalidad": 55.8,
        "gasto_social_pib": 13.5,
        "capital_humano_hci": 0.60,
        "anios_salir_pobreza": 11,
        "pilares": {
            "Educación y Logro": 41.2,
            "Salud y Nutrición": 12.5,
            "Agua y Saneamiento": 16.8,
            "Vivienda Digna": 14.3,
            "Trabajo y Prot. Social": 68.4,
        },
        "color": "#B5341A",
        "diagnostico": (
            "Colombia presenta un fuerte contraste interno: mientras sus capitales tienen estándares "
            "comparables a países de ingreso medio-alto, sus territorios periféricos y rurales registran privaciones "
            "crónicas que multiplican hasta por 5 las tasas urbanas. Registra el Gini más alto de la OCDE y una de "
            "las tasas de informalidad más persistentes del hemisferio."
        )
    },
    "Chile": {
        "codigo": "CHL",
        "bandera": "CHL",
        "bloque": "Miembro OCDE (2010) · Alianza del Pacífico",
        "ipm_nacional": 3.8,
        "ipm_rural": 9.4,
        "brecha_rural_urbana": 6.2,
        "pobreza_relativa_ocde": 16.1,
        "gini": 0.449,
        "informalidad": 27.4,
        "gasto_social_pib": 17.2,
        "capital_humano_hci": 0.65,
        "anios_salir_pobreza": 6,
        "pilares": {
            "Educación y Logro": 18.5,
            "Salud y Nutrición": 6.2,
            "Agua y Saneamiento": 4.1,
            "Vivienda Digna": 5.4,
            "Trabajo y Prot. Social": 34.5,
        },
        "color": "#1A6FA8",
        "diagnostico": (
            "Referente regional en baja pobreza multidimensional y cobertura de infraestructura básica. "
            "Su tasa de informalidad (27.4%) es menos de la mitad de la colombiana. Sin embargo, persisten tensiones "
            "en segregación educativa y suficiencia de pensiones."
        )
    },
    "Costa Rica": {
        "codigo": "CRI",
        "bandera": "CRI",
        "bloque": "Miembro OCDE (2021)",
        "ipm_nacional": 4.5,
        "ipm_rural": 11.2,
        "brecha_rural_urbana": 7.8,
        "pobreza_relativa_ocde": 20.5,
        "gini": 0.487,
        "informalidad": 37.2,
        "gasto_social_pib": 16.8,
        "capital_humano_hci": 0.63,
        "anios_salir_pobreza": 7,
        "pilares": {
            "Educación y Logro": 22.4,
            "Salud y Nutrición": 5.8,
            "Agua y Saneamiento": 3.5,
            "Vivienda Digna": 6.1,
            "Trabajo y Prot. Social": 42.1,
        },
        "color": "#2D6A4F",
        "diagnostico": (
            "Histórica inversión universal en salud primaria (EBAIS) y educación que ha blindado a la población "
            "frente a privaciones extremas en servicios públicos. Su desafío radica en un déficit fiscal recurrente "
            "y una informalidad en aumento en el sector servicios."
        )
    },
    "México": {
        "codigo": "MEX",
        "bandera": "MEX",
        "bloque": "Miembro OCDE (1994) · Alianza del Pacífico",
        "ipm_nacional": 7.2,
        "ipm_rural": 18.5,
        "brecha_rural_urbana": 13.1,
        "pobreza_relativa_ocde": 16.6,
        "gini": 0.435,
        "informalidad": 54.8,
        "gasto_social_pib": 12.8,
        "capital_humano_hci": 0.61,
        "anios_salir_pobreza": 8,
        "pilares": {
            "Educación y Logro": 34.6,
            "Salud y Nutrición": 21.5,
            "Agua y Saneamiento": 11.8,
            "Vivienda Digna": 12.2,
            "Trabajo y Prot. Social": 62.8,
        },
        "color": "#D97706",
        "diagnostico": (
            "Comparte con Colombia una alta informalidad estructural (>54%) y una fractura territorial norte-sur. "
            "La fragmentación en la atención médica y las reformas en salud han aumentado las privaciones en acceso a servicios "
            "médicos en los deciles más vulnerables."
        )
    },
    "Uruguay": {
        "codigo": "URY",
        "bandera": "URY",
        "bloque": "Mercosur",
        "ipm_nacional": 2.1,
        "ipm_rural": 4.8,
        "brecha_rural_urbana": 3.1,
        "pobreza_relativa_ocde": 14.2,
        "gini": 0.395,
        "informalidad": 21.5,
        "gasto_social_pib": 22.4,
        "capital_humano_hci": 0.60,
        "anios_salir_pobreza": 4,
        "pilares": {
            "Educación y Logro": 16.2,
            "Salud y Nutrición": 4.5,
            "Agua y Saneamiento": 2.8,
            "Vivienda Digna": 4.2,
            "Trabajo y Prot. Social": 28.6,
        },
        "color": "#4F46E5",
        "diagnostico": (
            "Líder sudamericano en menor desigualdad (Gini 0.395) y en gasto social público (22.4% del PIB). "
            "Cuenta con una red de seguridad social robusta que reduce sustancialmente el impacto de la pobreza multidimensional, "
            "aunque enfrenta retos en culminación de educación secundaria."
        )
    },
    "Brasil": {
        "codigo": "BRA",
        "bandera": "BRA",
        "bloque": "Mercosur · G20",
        "ipm_nacional": 6.2,
        "ipm_rural": 15.6,
        "brecha_rural_urbana": 11.2,
        "pobreza_relativa_ocde": 19.8,
        "gini": 0.520,
        "informalidad": 39.1,
        "gasto_social_pib": 19.5,
        "capital_humano_hci": 0.55,
        "anios_salir_pobreza": 9,
        "pilares": {
            "Educación y Logro": 29.8,
            "Salud y Nutrición": 9.8,
            "Agua y Saneamiento": 13.5,
            "Vivienda Digna": 11.8,
            "Trabajo y Prot. Social": 48.2,
        },
        "color": "#059669",
        "diagnostico": (
            "Pionero en transferencias condicionadas (Bolsa Família) y salud pública integrada (SUS). "
            "Mantiene marcadas brechas territoriales entre el Nordeste y el Centro-Sur, con niveles de desigualdad "
            "muy cercanos a los de Colombia."
        )
    },
    "Perú": {
        "codigo": "PER",
        "bandera": "PER",
        "bloque": "Alianza del Pacífico · Comunidad Andina",
        "ipm_nacional": 11.5,
        "ipm_rural": 34.2,
        "brecha_rural_urbana": 26.1,
        "pobreza_relativa_ocde": 18.5,
        "gini": 0.403,
        "informalidad": 71.2,
        "gasto_social_pib": 11.8,
        "capital_humano_hci": 0.61,
        "anios_salir_pobreza": 8,
        "pilares": {
            "Educación y Logro": 36.5,
            "Salud y Nutrición": 18.4,
            "Agua y Saneamiento": 24.6,
            "Vivienda Digna": 19.5,
            "Trabajo y Prot. Social": 78.4,
        },
        "color": "#DC2626",
        "diagnostico": (
            "Vecino andino con estabilidad macroeconómica pero altísima vulnerabilidad institucional. "
            "Su tasa de informalidad (71.2%) es la mayor entre economías medianas de la región, y la brecha rural-urbana "
            "en sierra y selva supera los 26 puntos porcentuales."
        )
    },
    "Ecuador": {
        "codigo": "ECU",
        "bandera": "ECU",
        "bloque": "Comunidad Andina",
        "ipm_nacional": 14.8,
        "ipm_rural": 36.5,
        "brecha_rural_urbana": 24.8,
        "pobreza_relativa_ocde": 21.2,
        "gini": 0.458,
        "informalidad": 51.3,
        "gasto_social_pib": 10.5,
        "capital_humano_hci": 0.59,
        "anios_salir_pobreza": 9,
        "pilares": {
            "Educación y Logro": 38.2,
            "Salud y Nutrición": 19.2,
            "Agua y Saneamiento": 21.4,
            "Vivienda Digna": 17.8,
            "Trabajo y Prot. Social": 66.8,
        },
        "color": "#EA580C",
        "diagnostico": (
            "Economía dolarizada con severas restricciones fiscales para inversión en capital social. "
            "Las zonas rurales e indígenas sufren de privaciones crónicas en agua potable y desnutrición infantil "
            "superior al 25%."
        )
    },
    "Promedio América Latina": {
        "codigo": "LAC",
        "bandera": "LAC",
        "bloque": "CEPAL / PNUD América Latina y el Caribe",
        "ipm_nacional": 12.8,
        "ipm_rural": 26.5,
        "brecha_rural_urbana": 16.2,
        "pobreza_relativa_ocde": 19.2,
        "gini": 0.465,
        "informalidad": 48.5,
        "gasto_social_pib": 14.5,
        "capital_humano_hci": 0.59,
        "anios_salir_pobreza": 7,
        "pilares": {
            "Educación y Logro": 31.5,
            "Salud y Nutrición": 14.2,
            "Agua y Saneamiento": 15.6,
            "Vivienda Digna": 13.9,
            "Trabajo y Prot. Social": 56.4,
        },
        "color": "#7C3AED",
        "diagnostico": (
            "La región más desigual del planeta. La pobreza multidimensional rural duplica sistemáticamente a la urbana. "
            "Casi la mitad de la fuerza laboral se encuentra en la informalidad, lo que limita la recaudación tributaria "
            "y crea una trampa de productividad generalizada."
        )
    },
    "Promedio OCDE": {
        "codigo": "OECD",
        "bandera": "OECD",
        "bloque": "Organización para la Cooperación y el Desarrollo Económicos",
        "ipm_nacional": 1.8,
        "ipm_rural": 3.2,
        "brecha_rural_urbana": 1.8,
        "pobreza_relativa_ocde": 11.4,
        "gini": 0.315,
        "informalidad": 14.8,
        "gasto_social_pib": 21.1,
        "capital_humano_hci": 0.74,
        "anios_salir_pobreza": 4.5,
        "pilares": {
            "Educación y Logro": 11.2,
            "Salud y Nutrición": 4.8,
            "Agua y Saneamiento": 1.5,
            "Vivienda Digna": 3.2,
            "Trabajo y Prot. Social": 18.2,
        },
        "color": "#0284C7",
        "diagnostico": (
            "Estándar de referencia de las economías desarrolladas. Destaca por alta formalidad laboral, redes universales "
            "de protección social (21.1% del PIB en gasto social) y un Índice de Capital Humano del 0.74 que garantiza alta "
            "movilidad intergeneracional."
        )
    }
}

PAISES_SELECCIONABLES = [p for p in DATOS_PAISES.keys() if p != "Colombia"]


# ══════════════════════════════════════════════════════════════════
# CONSTRUCTORES DE FIGURAS INTERACTIVAS
# ══════════════════════════════════════════════════════════════════

def build_fig_radar_regional(pais_comp="Chile"):
    """
    Gráfico de Radar (Scatterpolar) comparando los 5 pilares de privación
    entre Colombia y el país seleccionado.
    """
    col = DATOS_PAISES["Colombia"]["pilares"]
    cmp = DATOS_PAISES.get(pais_comp, DATOS_PAISES["Chile"])["pilares"]
    
    categorias = list(col.keys())
    valores_col = list(col.values()) + [list(col.values())[0]]
    valores_cmp = list(cmp.values()) + [list(cmp.values())[0]]
    cats_cerrado = categorias + [categorias[0]]
    
    info_cmp = DATOS_PAISES.get(pais_comp, DATOS_PAISES["Chile"])
    
    fig = go.Figure()
    
    # Traza Colombia
    fig.add_trace(go.Scatterpolar(
        r=valores_col,
        theta=cats_cerrado,
        fill="toself",
        fillcolor="rgba(181, 52, 26, 0.20)",
        line=dict(color="#B5341A", width=3),
        name="Colombia (COL)",
        hovertemplate="<b>Colombia (COL)</b><br>%{theta}: %{r:.1f}% de hogares con privación<extra></extra>"
    ))
    
    # Traza País Comparado
    fig.add_trace(go.Scatterpolar(
        r=valores_cmp,
        theta=cats_cerrado,
        fill="toself",
        fillcolor="rgba(26, 111, 168, 0.18)",
        line=dict(color=info_cmp["color"], width=2.5, dash="dash"),
        name=f"{pais_comp} ({info_cmp['codigo']})",
        hovertemplate=f"<b>{pais_comp} ({info_cmp['codigo']})</b><br>%{{theta}}: %{{r:.1f}}% de hogares con privación<extra></extra>"
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(max(valores_col), max(valores_cmp)) * 1.15],
                ticksuffix="%",
                tickfont=dict(family=FUENTE_MONO, size=10, color="#6B6B6B"),
                gridcolor="#E2DDD6",
            ),
            angularaxis=dict(
                tickfont=dict(family=FUENTE_SERIF, size=11, color="#1A1A1A"),
                gridcolor="#E2DDD6",
            ),
            bgcolor="white",
        ),
        font_family="Georgia, serif",
        height=480,
        margin=dict(t=40, b=40, l=60, r=60),
        legend=dict(
            orientation="h",
            y=1.12,
            x=0.5,
            xanchor="center",
            font=dict(family=FUENTE_SERIF, size=12),
        ),
        paper_bgcolor="white",
    )
    return fig


def build_fig_dispersion_pobreza_gini():
    """
    Gráfico de dispersión interactivo: Pobreza Multidimensional (%) vs Coeficiente de Gini.
    Ilustra los cuadrantes de bienestar y el posicionamiento de Colombia frente a la región y la OCDE.
    """
    filas = []
    for nombre, d in DATOS_PAISES.items():
        filas.append({
            "pais": nombre,
            "codigo": d["codigo"],
            "etiqueta": f"{nombre} ({d['codigo']})",
            "ipm": d["ipm_nacional"],
            "gini": d["gini"],
            "informalidad": d["informalidad"],
            "bloque": d["bloque"],
            "color": d["color"],
            "tamano": 28 if nombre == "Colombia" else (22 if "Promedio" in nombre else 16)
        })
    df = pd.DataFrame(filas)
    
    fig = go.Figure()
    
    # Cuadrantes de fondo
    fig.add_shape(type="rect", x0=0, x1=10, y0=0.25, y1=0.45,
                  fillcolor="rgba(45, 106, 79, 0.05)", line_width=0, layer="below")
    fig.add_shape(type="rect", x0=10, x1=25, y0=0.45, y1=0.60,
                  fillcolor="rgba(181, 52, 26, 0.05)", line_width=0, layer="below")
    
    # Líneas de referencia OCDE
    fig.add_hline(y=0.315, line_dash="dot", line_color="#0284C7", line_width=1.5,
                  annotation_text="Gini Promedio OCDE (0.315)", annotation_position="top left",
                  annotation_font=dict(family=FUENTE_MONO, size=10, color="#0284C7"))
    fig.add_vline(x=12.8, line_dash="dash", line_color="#7C3AED", line_width=1.5,
                  annotation_text="IPM Promedio América Latina (12.8%)", annotation_position="top right",
                  annotation_font=dict(family=FUENTE_MONO, size=10, color="#7C3AED"))
    
    # Puntos de dispersión
    for _, row in df.iterrows():
        es_col = row["pais"] == "Colombia"
        fig.add_trace(go.Scatter(
            x=[row["ipm"]],
            y=[row["gini"]],
            mode="markers+text",
            name=row["pais"],
            text=[f"<b>{row['codigo']}</b>" if es_col else row["codigo"]],
            textposition="top center",
            textfont=dict(
                family=FUENTE_MONO,
                size=12 if es_col else 10,
                color="#B5341A" if es_col else "#222222"
            ),
            marker=dict(
                size=row["tamano"],
                color=row["color"],
                line=dict(width=2.5 if es_col else 1.2, color="#FFFFFF"),
                symbol="star" if es_col else ("diamond" if "Promedio" in row["pais"] else "circle")
            ),
            hovertemplate=(
                f"<b>{row['pais']} ({row['codigo']})</b><br>"
                f"Bloque: {row['bloque']}<br>"
                f"IPM Nacional: <b>%{row['ipm']:.1f}%</b><br>"
                f"Coeficiente de Gini: <b>%{row['gini']:.3f}</b><br>"
                f"Informalidad Laboral: <b>%{row['informalidad']:.1f}%</b><extra></extra>"
            ),
            showlegend=False
        ))
        
    fig.update_layout(
        **{**BASE_LAYOUT, "margin": dict(t=50, b=60, l=70, r=40)},
        height=480,
        xaxis=dict(
            title=dict(text="Índice de Pobreza Multidimensional (%)", font=dict(family=FUENTE_SERIF, size=12)),
            ticksuffix="%",
            tickfont=dict(family=FUENTE_MONO, size=11),
            gridcolor="#F0EBE3",
            range=[0, 22]
        ),
        yaxis=dict(
            title=dict(text="Desigualdad de Ingresos (Coeficiente de Gini)", font=dict(family=FUENTE_SERIF, size=12)),
            tickfont=dict(family=FUENTE_MONO, size=11),
            gridcolor="#F0EBE3",
            range=[0.28, 0.58]
        ),
    )
    return fig


def build_fig_informalidad_gasto():
    """
    Gráfico de barras horizontales ordenadas: Tasa de Informalidad Laboral (%)
    y Gasto Social Público (% del PIB), destacando a Colombia.
    """
    filas = []
    for nombre, d in DATOS_PAISES.items():
        filas.append({
            "pais": nombre,
            "etiqueta": f"{nombre} ({d['codigo']})",
            "informalidad": d["informalidad"],
            "gasto_social": d["gasto_social_pib"],
            "es_colombia": (nombre == "Colombia")
        })
    df = pd.DataFrame(filas).sort_values("informalidad", ascending=True)
    
    fig = go.Figure()
    
    # Barra de Informalidad
    colores_inf = ["#B5341A" if row["es_colombia"] else "#D97706" if row["informalidad"] > 50 else "#6B7280" 
                   for _, row in df.iterrows()]
    fig.add_trace(go.Bar(
        y=df["etiqueta"],
        x=df["informalidad"],
        name="Tasa de Empleo Informal (%)",
        orientation="h",
        marker_color=colores_inf,
        text=df["informalidad"].map("{:.1f}%".format),
        textposition="outside",
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Informalidad: %{x:.1f}% de ocupados<extra></extra>"
    ))
    
    fig.add_vline(x=14.8, line_dash="dot", line_color="#0284C7", line_width=1.5,
                  annotation_text="Promedio OCDE (14.8%)", annotation_position="top left",
                  annotation_font=dict(family=FUENTE_MONO, size=10, color="#0284C7"))
                  
    fig.update_layout(
        **{**BASE_LAYOUT, "margin": dict(t=40, b=40, l=170, r=70)},
        height=480,
        xaxis=dict(
            title=dict(text="Tasa de Empleo Informal (% de la población ocupada)", font=dict(family=FUENTE_SERIF, size=11)),
            ticksuffix="%",
            tickfont=dict(family=FUENTE_MONO, size=10),
            gridcolor="#F0EBE3",
            range=[0, 90]
        ),
        yaxis=dict(autorange="reversed", tickfont=dict(family=FUENTE_SERIF, size=11)),
        showlegend=False
    )
    return fig


# ══════════════════════════════════════════════════════════════════
# COMPONENTE DE TARJETAS DE LECTURA RÁPIDA (KPIS DE BENCHMARKING)
# ══════════════════════════════════════════════════════════════════

def build_kpis_regionales(pais_sel="Chile"):
    """
    Genera la rejilla de tarjetas comparativas entre Colombia y el país seleccionado.
    """
    col = DATOS_PAISES["Colombia"]
    cmp = DATOS_PAISES.get(pais_sel, DATOS_PAISES["Chile"])
    
    dif_ipm = col["ipm_nacional"] - cmp["ipm_nacional"]
    dif_gini = col["gini"] - cmp["gini"]
    dif_inf = col["informalidad"] - cmp["informalidad"]
    dif_soc = col["gasto_social_pib"] - cmp["gasto_social_pib"]
    
    def tarjeta(titulo, icono, val_col, val_cmp, unidad, dif, es_inverso=False, decimales=1):
        formato = f"{{:.{decimales}f}}"
        # En gasto social, mayor es mejor; en pobreza, menor es mejor
        es_favorable = (dif < 0) if not es_inverso else (dif > 0)
        color_dif = "#2D6A4F" if es_favorable else "#B5341A"
        signo = "+" if dif > 0 else ""
        
        return html.Div(style={
            "background": "#FFFFFF",
            "borderRadius": "10px",
            "padding": "20px 22px",
            "borderLeft": f"4px solid {color_dif}",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
        }, children=[
            html.Div(style={"display": "flex", "alignItems": "center", "gap": "6px", "marginBottom": "6px"}, children=[
                html.Span(icono, className="material-symbols-outlined", style={
                    "fontSize": "1rem", "color": "#6B6B6B", "lineHeight": "1"
                }),
                html.P(titulo, style={
                    "fontFamily": FUENTE_MONO, "fontSize": "0.68rem", "color": "#6B6B6B",
                    "letterSpacing": "0.08em", "textTransform": "uppercase", "margin": 0
                }),
            ]),
            html.Div(style={"display": "flex", "alignItems": "baseline", "gap": "10px"}, children=[
                html.Span(f"{formato.format(val_col)}{unidad}", style={
                    "fontFamily": FUENTE_MONO, "fontSize": "1.7rem", "fontWeight": "700", "color": "#B5341A"
                }),
                html.Span(f"vs {formato.format(val_cmp)}{unidad}", style={
                    "fontFamily": FUENTE_SERIF, "fontSize": "0.9rem", "color": "#777777"
                }),
            ]),
            html.Div(style={"marginTop": "8px", "fontSize": "0.8rem", "fontFamily": FUENTE_MONO, "color": color_dif}, children=[
                html.Span(f"Brecha COL vs {cmp['codigo']}: "),
                html.B(f"{signo}{formato.format(dif)} {unidad}")
            ])
        ])
        
    return html.Div(style={
        "display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(220px, 1fr))",
        "gap": "16px", "marginBottom": "28px"
    }, children=[
        tarjeta("Incidencia IPM Nacional", "analytics", col["ipm_nacional"], cmp["ipm_nacional"], "%", dif_ipm),
        tarjeta("Desigualdad (Gini)", "balance", col["gini"], cmp["gini"], "", dif_gini, decimales=3),
        tarjeta("Informalidad Laboral", "badge", col["informalidad"], cmp["informalidad"], "%", dif_inf),
        tarjeta("Gasto Social Público", "account_balance", col["gasto_social_pib"], cmp["gasto_social_pib"], "% PIB", dif_soc, es_inverso=True),
    ])


# ══════════════════════════════════════════════════════════════════
# LAYOUT PRINCIPAL DE LA SECCIÓN REGIONAL
# ══════════════════════════════════════════════════════════════════

def build_seccion_regional_layout():
    """
    Construye el panel completo de la nueva sección: Contexto Regional y OCDE.
    """
    return html.Div(id="sec-regional", className="section-panel", children=[
        
        # ── Encabezado de la Sección ──────────────────────
        html.Div(className="page-header", children=[
            html.P("BENCHMARKING INTERNACIONAL · OCDE & CEPAL", className="page-header-tag"),
            html.H2("Colombia frente a sus Pares Latinoamericanos y la OCDE"),
            html.P(
                "Comparativa multidimensional de bienestar, desigualdad estructural, "
                "mercado laboral y capital humano basada en datos homogeneizados de la OCDE, "
                "CEPAL, Banco Mundial y PNUD."
            ),
        ]),
        
        html.Div(style={"padding": "0 48px 48px"}, children=[
            
            # ── Tarjeta de Contexto Teórico / OCDE ─────────
            html.Div(style={
                **CARD,
                "borderLeft": "4px solid #B5341A",
                "marginBottom": "28px",
                "background": "#FFFBF9"
            }, children=[
                html.H3("La 'Paradoja Colombiana' en el Club de Buenas Prácticas (OCDE)", style={
                    "fontFamily": "'Playfair Display', serif", "fontSize": "1.4rem", "marginBottom": "10px", "color": "#1A1A1A"
                }),
                html.P([
                    "Desde su ingreso formal a la Organización para la Cooperación y el Desarrollo Económicos (OCDE) en 2020, ",
                    "Colombia asumió estándares de política pública de economías de altos ingresos. Sin embargo, ",
                    html.B("Colombia lidera el bloque en desigualdad de ingresos (Gini 0.548)"), " y registra una tasa de informalidad laboral ",
                    "que casi cuadruplica el promedio OCDE (55.8% vs 14.8%). De acuerdo con el informe ",
                    html.I("OECD Economic Surveys: Colombia 2024"), ", una familia de bajos ingresos en Colombia tarda ",
                    html.B("hasta 11 generaciones"), " en alcanzar el ingreso medio nacional, frente a las 4.5 generaciones promedio en la OCDE."
                ], style={"fontFamily": FUENTE_SERIF, "fontSize": "0.95rem", "color": "#3A3A3A", "lineHeight": "1.7"})
            ]),
            
            # ── Selector de País de Contraste ───────────────
            html.Div(style={**CARD, "padding": "20px 28px", "marginBottom": "24px"}, children=[
                html.Div(style={"display": "flex", "alignItems": "center", "gap": "20px", "flexWrap": "wrap"}, children=[
                    html.Div(children=[
                        html.Label("Seleccionar país o bloque para contrastar con Colombia:", style={
                            "fontFamily": FUENTE_MONO, "fontSize": "0.72rem", "textTransform": "uppercase",
                            "letterSpacing": "0.08em", "color": "#6B6B6B", "display": "block", "marginBottom": "6px"
                        }),
                        dcc.Dropdown(
                            id="dd-pais-regional",
                            options=[{"label": f"{p} ({DATOS_PAISES[p]['codigo']}) · {DATOS_PAISES[p]['bloque']}", "value": p} 
                                     for p in PAISES_SELECCIONABLES],
                            value="Chile",
                            clearable=False,
                            style={"width": "420px", "fontFamily": "Georgia, serif"}
                        )
                    ]),
                    html.Div(id="tag-bloque-regional", style={"marginLeft": "auto", "paddingTop": "14px"})
                ])
            ]),
            
            # ── KPIs de Comparación Rápida ─────────────────
            html.Div(id="kpis-regionales"),
            
            # ── Rejilla: Radar Multidimensional + Diagnóstico
            html.Div(style={"display": "grid", "gridTemplateColumns": "1.2fr 1fr", "gap": "24px", "marginBottom": "32px"}, children=[
                
                # Columna 1: Radar de Privaciones
                html.Div(style=CARD, children=[
                    html.P("DIMENSIONES COMPARADAS · 5 PILARES", className="section-tag"),
                    html.H3("Silueta Multidimensional de Privaciones", style={
                        "fontFamily": "'Playfair Display', serif", "fontSize": "1.3rem", "marginBottom": "8px"
                    }),
                    html.P("Porcentaje de hogares con privación según pilares armonizados de la metodología Alkire-Foster / PNUD.", style={
                        "fontFamily": FUENTE_SERIF, "fontSize": "0.88rem", "color": "#6B6B6B", "marginBottom": "16px"
                    }),
                    dcc.Graph(id="g-radar-regional", config={"displayModeBar": False}),
                ]),
                
                # Columna 2: Diagnóstico Editorial y Cuadro Comparativo
                html.Div(style=CARD, children=[
                    html.P("DIAGNÓSTICO ESTRUCTURAL", className="section-tag"),
                    html.H3(id="titulo-diagnostico-regional", style={
                        "fontFamily": "'Playfair Display', serif", "fontSize": "1.3rem", "marginBottom": "12px"
                    }),
                    html.Div(id="texto-diagnostico-regional", style={
                        "fontFamily": FUENTE_SERIF, "fontSize": "0.93rem", "color": "#3A3A3A",
                        "lineHeight": "1.75", "marginBottom": "20px"
                    }),
                    html.Div(id="caja-brecha-rural-regional", style={
                        "background": "#FDF8F5", "borderLeft": "4px solid #B5341A",
                        "padding": "16px", "borderRadius": "0 8px 8px 0", "marginBottom": "16px"
                    }),
                    nota_fuente("Fuentes: DANE (ECV), OCDE (IDD 2024), CEPAL (Panorama Social 2024), PNUD/OPHI (Global MPI).")
                ])
            ]),
            
            # ── Rejilla 2: Gráficos Macro (Dispersión y Empleo)
            html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "24px", "marginBottom": "32px"}, children=[
                
                # Gráfico: Pobreza vs Desigualdad (Gini)
                html.Div(style=CARD, children=[
                    html.P("CUADRANTES DE DESARROLLO", className="section-tag"),
                    html.H3("Pobreza Multidimensional vs Desigualdad (Gini)", style={
                        "fontFamily": "'Playfair Display', serif", "fontSize": "1.25rem", "marginBottom": "8px"
                    }),
                    html.P("Muestra la ubicación de Colombia en el cuadrante de alta desigualdad relativa.", style={
                        "fontFamily": FUENTE_SERIF, "fontSize": "0.85rem", "color": "#6B6B6B", "marginBottom": "12px"
                    }),
                    dcc.Graph(figure=build_fig_dispersion_pobreza_gini(), config={"displayModeBar": False}),
                ]),
                
                # Gráfico: Informalidad vs Gasto Social
                html.Div(style=CARD, children=[
                    html.P("MERCADO LABORAL & PRODUCTIVIDAD", className="section-tag"),
                    html.H3("Tasa de Empleo Informal en la Región", style={
                        "fontFamily": "'Playfair Display', serif", "fontSize": "1.25rem", "marginBottom": "8px"
                    }),
                    html.P("Porcentaje de ocupados sin cobertura de seguridad social ni pensión (OIT / OCDE).", style={
                        "fontFamily": FUENTE_SERIF, "fontSize": "0.85rem", "color": "#6B6B6B", "marginBottom": "12px"
                    }),
                    dcc.Graph(figure=build_fig_informalidad_gasto(), config={"displayModeBar": False}),
                ])
            ]),
            
            # ── Sección 4: Impacto en Bienestar, Productividad y Capital Humano ────
            panel_seccion("#2D6A4F", [
                tag_seccion("#2D6A4F", "EVIDENCIA EMPÍRICA Y POLÍTICA PÚBLICA"),
                titulo_seccion("¿Cómo Afectan Estas Cifras al Bienestar y al Crecimiento de Colombia?"),
                subtitulo_seccion(
                    "La literatura económica contemporánea demuestra que las privaciones multidimensionales "
                    "no son solo síntomas de pobreza, sino frenos estructurales que destruyen la productividad agregada."
                ),
                
                html.Div(style={
                    "display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(280px, 1fr))",
                    "gap": "20px", "marginTop": "24px"
                }, children=[
                    
                    # Pilar 1: Capital Humano
                    html.Div(style={
                        "background": "#F7FBF8", "padding": "22px", "borderRadius": "8px",
                        "borderTop": "3px solid #2D6A4F"
                    }, children=[
                        html.H4([
                            html.Span("child_care", className="material-symbols-outlined", style={
                                "fontSize": "1.3rem", "marginRight": "8px", "color": "#2D6A4F", "verticalAlign": "middle"
                            }),
                            "1. Capital Humano y Primera Infancia"
                        ], style={
                            "fontFamily": "'Playfair Display', serif", "fontSize": "1.1rem", "marginBottom": "10px", "color": "#2D6A4F",
                            "display": "flex", "alignItems": "center"
                        }),
                        html.P(
                            "El Índice de Capital Humano (HCI) de Colombia es 0.60. Esto implica que un niño nacido hoy "
                            "alcanzará solo el 60% de su productividad potencial futura. En zonas donde más del 35% de los hogares "
                            "carecen de agua potable y saneamiento (Chocó, La Guajira), la desnutrición crónica y las infecciones "
                            "tempranas provocan daños neurológicos irreversibles en los primeros 1,000 días de vida.",
                            style={"fontFamily": FUENTE_SERIF, "fontSize": "0.88rem", "lineHeight": "1.65", "color": "#333"}
                        )
                    ]),
                    
                    # Pilar 2: Dualismo Laboral
                    html.Div(style={
                        "background": "#FFFBF5", "padding": "22px", "borderRadius": "8px",
                        "borderTop": "3px solid #D97706"
                    }, children=[
                        html.H4([
                            html.Span("work", className="material-symbols-outlined", style={
                                "fontSize": "1.3rem", "marginRight": "8px", "color": "#D97706", "verticalAlign": "middle"
                            }),
                            "2. Dualismo Laboral y Productividad"
                        ], style={
                            "fontFamily": "'Playfair Display', serif", "fontSize": "1.1rem", "marginBottom": "10px", "color": "#D97706",
                            "display": "flex", "alignItems": "center"
                        }),
                        html.P(
                            "Con un 55.8% de informalidad nacional y más del 80% en áreas rurales, la productividad laboral "
                            "colombiana equivale a menos del 35% del promedio de la OCDE. Los trabajadores informales tienen un ingreso "
                            "por hora 45% menor y carecen de protección ante accidentes o jubilación, perpetuando un círculo vicioso de "
                            "baja innovación y empleo de subsistencia.",
                            style={"fontFamily": FUENTE_SERIF, "fontSize": "0.88rem", "lineHeight": "1.65", "color": "#333"}
                        )
                    ]),
                    
                    # Pilar 3: Fractura Territorial
                    html.Div(style={
                        "background": "#FDF8F5", "padding": "22px", "borderRadius": "8px",
                        "borderTop": "3px solid #B5341A"
                    }, children=[
                        html.H4([
                            html.Span("landscape", className="material-symbols-outlined", style={
                                "fontSize": "1.3rem", "marginRight": "8px", "color": "#B5341A", "verticalAlign": "middle"
                            }),
                            "3. Trampa de Exclusión Territorial"
                        ], style={
                            "fontFamily": "'Playfair Display', serif", "fontSize": "1.1rem", "marginBottom": "10px", "color": "#B5341A",
                            "display": "flex", "alignItems": "center"
                        }),
                        html.P(
                            "La brecha rural-urbana de 18.4 puntos de IPM (27.3% rural vs 8.9% en cabeceras) sitúa a Colombia "
                            "entre los países con mayor fragmentación espacial de América Latina. Las familias en territorios "
                            "desconectados quedan atrapadas en la agricultura informal no tecnificada, sin acceso a créditos ni a bienes "
                            "públicos de transporte y conectividad digital.",
                            style={"fontFamily": FUENTE_SERIF, "fontSize": "0.88rem", "lineHeight": "1.65", "color": "#333"}
                        )
                    ]),
                    
                    # Pilar 4: Feminización de la Pobreza
                    html.Div(style={
                        "background": "#F8F5FB", "padding": "22px", "borderRadius": "8px",
                        "borderTop": "3px solid #7C3AED"
                    }, children=[
                        html.H4([
                            html.Span("family_restroom", className="material-symbols-outlined", style={
                                "fontSize": "1.3rem", "marginRight": "8px", "color": "#7C3AED", "verticalAlign": "middle"
                            }),
                            "4. Feminización y Economía del Cuidado"
                        ], style={
                            "fontFamily": "'Playfair Display', serif", "fontSize": "1.1rem", "marginBottom": "10px", "color": "#7C3AED",
                            "display": "flex", "alignItems": "center"
                        }),
                        html.P(
                            "La falta de cobertura en cuidado infantil temprano recae desproporcionadamente en las mujeres, "
                            "quienes dedican en promedio 7.5 horas diarias al trabajo de cuidados no remunerado frente a 2.5 horas en hombres. "
                            "Esto limita su inserción al mercado formal y agrava la vulnerabilidad económica de los hogares con jefatura femenina monoparental.",
                            style={"fontFamily": FUENTE_SERIF, "fontSize": "0.88rem", "lineHeight": "1.65", "color": "#333"}
                        )
                    ]),
                ]),
                
                # ── Simulador Didáctico de Cierre de Brechas ────
                html.Div(style={
                    "marginTop": "28px", "background": "#FFFFFF", "padding": "24px",
                    "borderRadius": "8px", "border": "1px solid #E2DDD6"
                }, children=[
                    html.H4([
                        html.Span("tune", className="material-symbols-outlined", style={
                            "fontSize": "1.35rem", "marginRight": "8px", "color": "#1A1A1A", "verticalAlign": "middle"
                        }),
                        "Simulador de Políticas: ¿Qué ganaría Colombia si cerrara sus brechas críticas?"
                    ], style={
                        "fontFamily": "'Playfair Display', serif", "fontSize": "1.2rem", "marginBottom": "10px", "color": "#1A1A1A",
                        "display": "flex", "alignItems": "center"
                    }),
                    html.P(
                        "Selecciona un objetivo de convergencia para proyectar el impacto económico y social:",
                        style={"fontFamily": FUENTE_SERIF, "fontSize": "0.9rem", "color": "#6B6B6B", "marginBottom": "14px"}
                    ),
                    html.Div(style={"display": "flex", "gap": "12px", "flexWrap": "wrap", "marginBottom": "20px"}, children=[
                        dcc.RadioItems(
                            id="radio-simulador",
                            options=[
                                {"label": " Universalizar Agua y Saneamiento Rural al 95%", "value": "agua"},
                                {"label": " Reducir Informalidad al promedio de Alianza del Pacífico (40%)", "value": "empleo"},
                                {"label": " Reducir Rezago Escolar e Inasistencia al nivel de Chile", "value": "educacion"}
                            ],
                            value="agua",
                            inline=True,
                            style={"fontFamily": FUENTE_SERIF, "fontSize": "0.92rem"}
                        )
                    ]),
                    html.Div(id="resultado-simulador", style={
                        "background": "#F7FBF8", "borderLeft": "4px solid #2D6A4F",
                        "padding": "16px 20px", "borderRadius": "0 6px 6px 0"
                    })
                ])
            ])
        ])
    ])
