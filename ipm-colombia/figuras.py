"""
Utilidades compartidas para construir las figuras de Plotly del dashboard.

Las tres series temporales del tablero (agua/indicadores, género y evolución
anual del IPM) se dibujaban con el mismo código repetido tres veces: relleno
bajo la línea, línea con marcadores y etiquetas, marca de brecha y layout.
Aquí viven esas piezas una sola vez.
"""

import plotly.graph_objects as go

FUENTE_MONO = "DM Mono, monospace"
FUENTE_SERIF = "Source Serif 4, serif"
COLOR_EJE = "#6B6B6B"
COLOR_GRILLA = "#F0EBE3"

BASE_LAYOUT = dict(
    font_family="Georgia, serif",
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(t=40, b=50, l=180, r=40),
)


def add_area_bajo_linea(fig, x, y, fillcolor, nombre=None):
    """Sombrea el área entre la serie y el eje x, sin leyenda ni hover."""
    xs = list(x)
    fig.add_trace(go.Scatter(
        x=xs + xs[::-1],
        y=list(y) + [0] * len(xs),
        fill="toself",
        fillcolor=fillcolor,
        line=dict(width=0),
        showlegend=False,
        hoverinfo="skip",
        name=nombre,
    ))


def add_serie_anual(fig, x, y, nombre, color, ancho, dash, simbolo, hovertemplate=None):
    """Añade una serie anual en % como línea + marcadores + etiquetas de dato.

    `y` debe ser una Serie de pandas: sus valores se etiquetan con un decimal.
    """
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="lines+markers+text",
        name=nombre,
        line=dict(color=color, width=ancho, dash=dash),
        marker=dict(
            symbol=simbolo,
            size=10,
            color=color,
            line=dict(width=1.5, color="white"),
        ),
        text=y.map("{:.1f}%".format),
        textposition="top center",
        textfont=dict(family=FUENTE_MONO, size=10, color=color),
        hovertemplate=hovertemplate,
    ))


def add_marca_brecha(
    fig,
    x,
    y_desde,
    y_hasta,
    color,
    texto,
    xshift=18,
    tamano_fuente=12,
    bgcolor="rgba(255,248,245,0.9)",
    borderpad=5,
    familia_fuente=FUENTE_MONO,
):
    """Marca la brecha entre dos series en `x`: etiqueta y línea vertical."""
    fig.add_annotation(
        x=x,
        y=(y_desde + y_hasta) / 2,
        text=texto,
        showarrow=False,
        xanchor="left",
        xshift=xshift,
        font=dict(family=familia_fuente, size=tamano_fuente, color=color),
        bgcolor=bgcolor,
        bordercolor=color,
        borderwidth=1,
        borderpad=borderpad,
    )
    fig.add_shape(
        type="line",
        x0=x, x1=x,
        y0=y_desde, y1=y_hasta,
        line=dict(color=color, width=1.5, dash="dot"),
    )


def texto_brecha(brecha):
    """Etiqueta estándar de la marca de brecha, en puntos porcentuales."""
    return f"<b>Brecha<br>{brecha:+.1f} pp</b>"


def layout_serie_anual(anios, titulo_y, margin_r=80):
    """Layout común de las líneas temporales anuales (eje x = años, eje y = %)."""
    return dict(
        BASE_LAYOUT,
        height=460,
        margin=dict(t=50, b=150, l=60, r=margin_r),
        xaxis=dict(
            title=dict(text="Año", font=dict(size=11, color=COLOR_EJE)),
            tickmode="array",
            tickvals=list(anios),
            ticktext=[str(a) for a in anios],
            tickfont=dict(family=FUENTE_MONO, size=11),
            showgrid=True,
            gridcolor=COLOR_GRILLA,
            gridwidth=1,
            zeroline=False,
        ),
        yaxis=dict(
            title=dict(text=titulo_y, font=dict(size=11, color=COLOR_EJE)),
            ticksuffix="%",
            tickfont=dict(family=FUENTE_MONO, size=11),
            showgrid=True,
            gridcolor=COLOR_GRILLA,
            gridwidth=1,
            zeroline=False,
            rangemode="tozero",
        ),
        legend=dict(
            orientation="h",
            y=-0.55,
            x=0.5,
            xanchor="center",
            font=dict(family=FUENTE_SERIF, size=12),
            bgcolor="rgba(0,0,0,0)",
            itemwidth=80,
        ),
        hovermode="x unified",
    )
