"""
Componentes y estilos reutilizables del layout Dash del dashboard.

Cada sección repetía los mismos bloques inline: la fila de tarjetas de
contexto, los encabezados de sección, las cajas de insight, las leyendas y
los selectores. Aquí quedan definidos una sola vez.
"""

from dash import dcc, html


def _props(texto=None, id=None):
    """Props opcionales: Dash rechaza `id=None` o hijos vacíos explícitos."""
    props = {}
    if texto is not None:
        props["children"] = texto
    if id is not None:
        props["id"] = id
    return props

# ── Paleta y tarjeta base ─────────────────────────────────────────
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

FUENTE_MONO = "'DM Mono', monospace"
FUENTE_SERIF = "'Source Serif 4', serif"
FUENTE_TITULO = "'Playfair Display', serif"

ESTILO_CUERPO = {
    "fontFamily": FUENTE_SERIF,
    "fontSize":   "0.95rem",
    "color":      "#4A4A4A",
    "lineHeight": "1.6",
}

ESTILO_NOTA = {
    "fontFamily": FUENTE_SERIF,
    "fontSize":   "0.85rem",
    "color":      "#4A4A4A",
    "lineHeight": "1.7",
}

ESTILO_LABEL = {
    "fontFamily":    FUENTE_MONO,
    "fontSize":      "0.68rem",
    "letterSpacing": ".08em",
    "color":         "#6B6B6B",
    "textTransform": "uppercase",
    "display":       "block",
    "marginBottom":  "5px",
}


# ── Tarjetas de contexto (cabecera de cada sección) ───────────────
def fila_contexto(tarjetas, columnas="1.2fr 1fr 1fr"):
    """Rejilla con las tarjetas introductorias de una sección."""
    return html.Div(style={
        "marginBottom":        "32px",
        "display":             "grid",
        "gridTemplateColumns": columnas,
        "gap":                 "24px",
    }, children=tarjetas)


def tarjeta_texto(titulo, parrafos):
    """Tarjeta blanca con título y párrafos explicativos."""
    hijos = [html.H3(titulo, style={
        "fontFamily":   FUENTE_TITULO,
        "fontSize":     "1.4rem",
        "marginBottom": "12px",
        "color":        "#1A1A1A",
    })]
    for i, parrafo in enumerate(parrafos):
        ultimo = i == len(parrafos) - 1
        hijos.append(html.P(parrafo, style=(
            ESTILO_CUERPO if ultimo else {**ESTILO_CUERPO, "marginBottom": "12px"}
        )))
    return html.Div(style={**CARD, "marginBottom": "0"}, children=hijos)


def tarjeta_lista(titulo, items, fondo, color_items):
    """Tarjeta de color con título blanco y una lista de puntos."""
    return html.Div(style={**CARD, "background": fondo, "color": "white",
                           "marginBottom": "0"}, children=[
        html.H3(titulo, style={
            "fontFamily":   FUENTE_TITULO,
            "fontSize":     "1.2rem",
            "marginBottom": "14px",
            "color":        "white",
        }),
        html.Ul(style={
            "paddingLeft": "20px",
            "fontFamily":  FUENTE_SERIF,
            "fontSize":    "0.85rem",
            "lineHeight":  "1.7",
            "color":       color_items,
        }, children=[html.Li(item) for item in items]),
    ])


def item_destacado(etiqueta, texto):
    """Punto de lista con la etiqueta resaltada en blanco."""
    return [html.B(etiqueta, style={"color": "white"}), texto]


def tarjeta_nota(titulo, texto, fondo, color):
    """Tarjeta tenue con borde lateral de color y un párrafo de contexto."""
    return html.Div(style={**CARD, "background": fondo,
                           "borderLeft": f"4px solid {color}",
                           "marginBottom": "0"}, children=[
        html.H3(titulo, style={
            "fontFamily":   FUENTE_TITULO,
            "fontSize":     "1.2rem",
            "marginBottom": "14px",
            "color":        color,
        }),
        html.P(texto, style=ESTILO_NOTA),
    ])


# ── Encabezado y piezas internas de una sección ───────────────────
def panel_seccion(color, children):
    """Tarjeta principal de una sección, con franja superior de color."""
    return html.Div(style={**CARD, "borderTop": f"4px solid {color}"},
                    children=children)


def tag_seccion(color, texto=None, id=None):
    """Etiqueta monoespaciada sobre el titular de la sección."""
    return html.P(style={
        "fontFamily":    FUENTE_MONO,
        "fontSize":      "0.68rem",
        "letterSpacing": "0.13em",
        "color":         color,
        "marginBottom":  "6px",
    }, **_props(texto, id))


def titulo_seccion(texto=None, id=None):
    """Titular editorial de la sección."""
    return html.H2(style={
        "fontFamily":   FUENTE_TITULO,
        "fontSize":     "clamp(1.2rem, 2.5vw, 1.8rem)",
        "fontWeight":   "700",
        "color":        "#1A1A1A",
        "lineHeight":   "1.25",
        "marginBottom": "10px",
    }, **_props(texto, id))


def subtitulo_seccion(texto=None, id=None):
    """Bajada que acompaña al titular de la sección."""
    return html.P(style={
        "fontFamily":   FUENTE_SERIF,
        "fontSize":     "0.95rem",
        "color":        "#5A5A5A",
        "lineHeight":   "1.7",
        "maxWidth":     "780px",
        "marginBottom": "22px",
    }, **_props(texto, id))


def caja_insight(id=None, fondo="#FFF8F5", borde="#C94A17", color="#3A2A20",
                 tamano="0.93rem", margen="20px"):
    """Caja en cursiva con la lectura narrativa del gráfico."""
    return html.Div(style={
        "background":   fondo,
        "borderLeft":   f"3px solid {borde}",
        "padding":      "14px 18px",
        "borderRadius": "0 8px 8px 0",
        "fontFamily":   FUENTE_SERIF,
        "fontStyle":    "italic",
        "color":        color,
        "fontSize":     tamano,
        "lineHeight":   "1.65",
        "marginBottom": margen,
    }, **_props(id=id))


def nota_fuente(texto=None, id=None, margen_superior="12px"):
    """Nota metodológica al pie de la sección."""
    return html.P(style={
        "fontFamily":    FUENTE_MONO,
        "fontSize":      "0.68rem",
        "color":         "#9B8B6E",
        "letterSpacing": "0.04em",
        "marginTop":     margen_superior,
    }, **_props(texto, id))


# ── Leyendas, selectores y gráficos ───────────────────────────────
def fila_leyenda(items):
    """Contenedor de la leyenda manual de formas y trazos."""
    return html.Div(style={
        "display":      "flex",
        "gap":          "60px",
        "flexWrap":     "wrap",
        "marginBottom": "24px",
        "alignItems":   "center",
    }, children=items)


def item_leyenda(muestra, texto, color, negrita=True):
    """Ítem de leyenda: `muestra` es el estilo del trazo de ejemplo."""
    estilo_texto = {
        "fontFamily": FUENTE_SERIF,
        "fontSize":   "0.82rem",
        "color":      color,
    }
    if negrita:
        estilo_texto["fontWeight"] = "600"
    return html.Div(style={"display": "flex", "alignItems": "center", "gap": "8px"},
                    children=[
        html.Div(style=muestra),
        html.Div(texto, style=estilo_texto),
    ])


def campo_dropdown(label, dropdown, estilo=None):
    """Etiqueta en versalitas sobre un desplegable."""
    hijos = [html.Label(label, style=ESTILO_LABEL), dropdown]
    return html.Div(hijos, style=estilo) if estilo else html.Div(hijos)


def opciones_con_nacional(valores, etiqueta="Nacional (promedio)"):
    """Opciones de departamento precedidas por la opción nacional."""
    return ([{"label": etiqueta, "value": "Nacional"}] +
            [{"label": v, "value": v} for v in valores])


def grafico(id):
    """Gráfico sin barra de herramientas de Plotly."""
    return dcc.Graph(id=id, config={"displayModeBar": False})
