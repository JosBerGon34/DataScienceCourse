# src/dash_timeseries.py
import io
import urllib.request
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output, callback
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose

# ==============================================================================
# 1. RELATIVE PATHS & TWO-JOBLIB LOADING
# ==============================================================================


RAW_BASE = "https://raw.githubusercontent.com/JosBerGon34/DataScienceCourse/main/models"
BASE_DIR = Path(__file__).resolve().parent
CANDIDATE_MODEL_DIRS = [
    BASE_DIR.parent / "models",  # works when script is inside src/
    BASE_DIR / "models",         # works when script is at app root
]


def load_joblib_from_url_or_local(filename: str, url: str):
    for folder in CANDIDATE_MODEL_DIRS:
        local_path = folder / filename
        if local_path.is_file():
            return joblib.load(local_path)

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return joblib.load(io.BytesIO(resp.read()))

dicts_bundle = load_joblib_from_url_or_local(
    "ts_dicts_bundle.joblib",
    f"{RAW_BASE}/ts_dicts_bundle.joblib",
)
model_bundle = load_joblib_from_url_or_local(
    "sarimax_spain_bundle.joblib",
    f"{RAW_BASE}/sarimax_spain_bundle.joblib",
)

CONFIG_DICTS = dicts_bundle["config_dicts"]
MULTIBAR_EDA = dicts_bundle["multibar_eda"]

BASE_SARIMAX = model_bundle["sarimax_model"]
TS_DF = model_bundle["ts_df"]
TRAIN_DF = model_bundle["train_df"]
VAL_DF = model_bundle["val_df"]
EXOG_COLS = model_bundle["exog_cols"]


# ==============================================================================
# 2. MULTI-BAR PLOT BUILDER (FROM DICTIONARY, ONE COLOR PER PARTY)
# ==============================================================================
def build_multibar_from_dict(multibar_data: dict) -> go.Figure:
    """Builds a grouped multi-bar chart across the 3 ESS rounds with distinct colors per party."""
    rounds = list(multibar_data.keys())
    all_parties = []
    for r in rounds:
        for p in multibar_data[r]["parties"]:
            if p not in all_parties:
                all_parties.append(p)

    palette = px.colors.qualitative.Bold + px.colors.qualitative.Vivid
    party_colors = {p: palette[i % len(palette)] for i, p in enumerate(all_parties)}

    fig = go.Figure()
    for party in all_parties:
        y_vals = []
        for r in rounds:
            p_list = multibar_data[r]["parties"]
            v_list = multibar_data[r]["vote_pct"]
            y_vals.append(v_list[p_list.index(party)] if party in p_list else 0.0)

        fig.add_trace(
            go.Bar(
                name=party,
                x=rounds,
                y=y_vals,
                marker_color=party_colors[party],
                text=[f"{v:.1f}%" if v > 2.5 else "" for v in y_vals],
                textposition="outside",
            )
        )

    fig.update_layout(
        barmode="group",
        template="plotly_dark",
        paper_bgcolor="#161b22",
        plot_bgcolor="#0d1117",
        title="Evolución Política de España: Porcentaje de Voto por Partido (ESS1 · ESS6 · ESS11)",
        xaxis_title="Ronda ESS (Año de Campo)",
        yaxis_title="Porcentaje de Voto Válido (%)",
        yaxis=dict(range=[0, 52]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11)),
        margin=dict(l=40, r=20, t=85, b=40),
    )
    return fig


FIG_MULTIBAR = build_multibar_from_dict(MULTIBAR_EDA)

# ==============================================================================
# 3. DASH APPLICATION LAYOUT
# ==============================================================================
app = Dash(__name__, title="Evolución Política de España — Time Series & Macro")

CARD_STYLE = {
    "backgroundColor": "#161b22",
    "border": "1px solid #30363d",
    "borderRadius": "8px",
    "padding": "18px",
    "marginBottom": "20px",
}

app.layout = html.Div(
    style={"backgroundColor": "#0d1117", "color": "#c9d1d9", "fontFamily": "Inter, system-ui, sans-serif", "padding": "24px", "minHeight": "100vh"},
    children=[
        html.Div([
            html.H1("Evolución Política de España", style={"margin": "0 0 6px 0", "color": "#58a6ff"}),
            html.P(
                "Mini-EDA Multivariante por Formación (ESS1 · ESS6 · ESS11) + Serie Temporal Continua (lrscale vs. Vectores Macroeconómicos SARIMAX)",
                style={"margin": "0 0 20px 0", "color": "#8b949e", "fontSize": "14px"},
            ),
        ]),

        # SECTION 1: STATIC MULTI-BAR REFERENCE (ESS1, ESS6, ESS11)
        html.Div(style=CARD_STYLE, children=[
            html.H3("1. Mini-EDA: Estructura Partidista por Ronda (Referencia Estática)", style={"marginTop": "0", "color": "#f0f6fc"}),
            dcc.Graph(figure=FIG_MULTIBAR, style={"height": "440px"}),
        ]),

        # SECTION 2: CONTINUOUS TIME SERIES & EXOGENOUS SARIMAX
        html.Div(style=CARD_STYLE, children=[
            html.H3("2. Dinámica Temporal Continua (lrscale & Vectores Macroeconómicos)", style={"marginTop": "0", "color": "#f0f6fc"}),
            dcc.Tabs(
                id="ts-tabs",
                value="tab-eda",
                colors={"border": "#30363d", "primary": "#58a6ff", "background": "#0d1117"},
                children=[
                    dcc.Tab(label="A. Serie Temporal & Vectores Económicos (ADF)", value="tab-eda", children=[
                        html.Div(style={"marginTop": "16px"}, children=[
                            html.Div(style={"display": "flex", "gap": "28px", "flexWrap": "wrap", "alignItems": "center", "marginBottom": "12px"}, children=[
                                dcc.RadioItems(
                                    id="eda-diff-toggle",
                                    options=[
                                        {"label": " Serie Original + Vectores Macro (Z-score)", "value": "orig"},
                                        {"label": " Primera Diferencia Δy_t (Estacionaria)", "value": "diff"},
                                    ],
                                    value="orig",
                                    inline=True,
                                    labelStyle={"marginRight": "18px"},
                                ),
                                html.Div(style={"minWidth": "280px", "flex": "1"}, children=[
                                    html.Label("Ventana Móvil k (Trimestres):", style={"fontWeight": "600", "fontSize": "13px"}),
                                    dcc.Slider(id="eda-window-slider", min=2, max=12, step=1, value=4, marks={i: f"{i}Q" for i in range(2, 13, 2)}),
                                ]),
                            ]),
                            html.Div(id="adf-diagnostic-banner", style={"padding": "10px", "backgroundColor": "#0d1117", "borderRadius": "6px", "marginBottom": "12px"}),
                            dcc.Graph(id="eda-ts-graph", style={"height": "470px"}),
                        ])
                    ]),
                    dcc.Tab(label="B. Descomposición Estacional Trimestral", value="tab-decomp", children=[
                        html.Div(style={"marginTop": "16px"}, children=[
                            dcc.RadioItems(
                                id="decomp-model-radio",
                                options=[
                                    {"label": " Modelo Aditivo (Y = T + S + R)", "value": "additive"},
                                    {"label": " Modelo Multiplicativo (Y = T × S × R)", "value": "multiplicative"},
                                ],
                                value="additive",
                                inline=True,
                                labelStyle={"marginRight": "20px", "marginBottom": "12px"},
                            ),
                            dcc.Graph(id="decomp-graph", style={"height": "580px"}),
                        ])
                    ]),
                    dcc.Tab(label="C. Forecasting Exógeno SARIMAX & Stress-Test", value="tab-forecast", children=[
                        html.Div(style={"marginTop": "16px"}, children=[
                            html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(220px, 1fr))", "gap": "18px", "marginBottom": "16px"}, children=[
                                html.Div([
                                    html.Label("Horizonte h (Trimestres desde 2022-Q1):", style={"fontWeight": "600", "fontSize": "13px"}),
                                    dcc.Slider(id="fc-horizon-slider", min=8, max=24, step=4, value=16, marks={i: f"{i}Q" for i in [8, 12, 16, 20, 24]}),
                                ]),
                                html.Div([
                                    html.Label("Shock PIB per cápita (€):", style={"fontWeight": "600", "fontSize": "13px"}),
                                    dcc.Slider(id="shock-gdp-slider", min=-3000, max=3000, step=500, value=0, marks={-3000: "-3k", 0: "0", 3000: "+3k"}),
                                ]),
                                html.Div([
                                    html.Label("Shock Desempleo (pp):", style={"fontWeight": "600", "fontSize": "13px"}),
                                    dcc.Slider(id="shock-unemp-slider", min=-4.0, max=6.0, step=1.0, value=0.0, marks={-4: "-4%", 0: "0%", 6: "+6%"}),
                                ]),
                                html.Div([
                                    html.Label("Shock Inflación (pp):", style={"fontWeight": "600", "fontSize": "13px"}),
                                    dcc.Slider(id="shock-infl-slider", min=-3.0, max=5.0, step=1.0, value=0.0, marks={-3: "-3%", 0: "0%", 5: "+5%"}),
                                ]),
                            ]),
                            html.Div(id="forecast-metrics-card", style={"padding": "12px", "backgroundColor": "#0d1117", "borderRadius": "6px", "marginBottom": "12px"}),
                            dcc.Graph(id="forecast-graph", style={"height": "480px"}),
                        ])
                    ]),
                ],
            ),
        ]),
    ],
)


# ==============================================================================
# 4. REACTIVE CALLBACKS
# ==============================================================================
@callback(
    Output("eda-ts-graph", "figure"),
    Output("adf-diagnostic-banner", "children"),
    Input("eda-diff-toggle", "value"),
    Input("eda-window-slider", "value"),
)
def update_eda_tab(diff_mode, window_k):
    series = TS_DF["lrscale_visual"].copy()
    label = "lrscale (0=Izq, 10=Der)"
    if diff_mode == "diff":
        series = series.diff().dropna()
        label = "Primera Diferencia Δlrscale"

    roll_mean = series.rolling(window=window_k).mean()
    adf_stat, p_val, _, _, crit_vals, _ = adfuller(series.dropna())
    is_stat = p_val < 0.05

    banner = html.Div(style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "flexWrap": "wrap"}, children=[
        html.Span(f"Test ADF: Estadístico = {adf_stat:.4f} | p-value = {p_val:.4f} | Crítico 5% = {crit_vals['5%']:.4f}"),
        html.Span(
            "ESTACIONARIA (p < 0.05)" if is_stat else "NO ESTACIONARIA (p >= 0.05)",
            style={"backgroundColor": "#2ea043" if is_stat else "#da3633", "color": "#fff", "padding": "3px 10px", "borderRadius": "10px", "fontSize": "12px", "fontWeight": "600"},
        ),
    ])

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=series.index, y=series, mode="lines", name=label, line=dict(color="#58a6ff", width=2.6)), secondary_y=False)
    fig.add_trace(go.Scatter(x=roll_mean.index, y=roll_mean, mode="lines", name=f"Media Móvil ({window_k}Q)", line=dict(color="#f0883e", dash="dash")), secondary_y=False)

    if diff_mode == "orig":
        anchors = TS_DF[TS_DF["lr_anchor"].notna()]
        fig.add_trace(
            go.Scatter(x=anchors.index, y=anchors["lr_anchor"], mode="markers", name="Anclas Reales", marker=dict(color="#ffffff", size=7, symbol="diamond")),
            secondary_y=False,
        )
        # Overlay the 3 macroeconomic vectors in distinct colors (standardized Z-score on secondary axis)
        for col, name, color in [
            ("gdp_per_capita", "PIB per cápita (Z)", "#3fb950"),
            ("unemployment_pct", "Desempleo % (Z)", "#f85149"),
            ("inflation_pct", "Inflación % (Z)", "#d2a8ff"),
        ]:
            z_vec = (TS_DF[col] - TS_DF[col].mean()) / TS_DF[col].std()
            fig.add_trace(
                go.Scatter(x=TS_DF.index, y=z_vec, mode="lines", name=name, line=dict(color=color, width=1.6, dash="dot"), opacity=0.85),
                secondary_y=True,
            )

    fig.update_layout(
        template="plotly_dark", paper_bgcolor="#161b22", plot_bgcolor="#0d1117",
        xaxis=dict(rangeslider=dict(visible=True)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=55, b=40),
    )
    fig.update_yaxes(title_text="lrscale (0–10)", secondary_y=False)
    fig.update_yaxes(title_text="Vectores Económicos (Z-score)", secondary_y=True)
    return fig, banner


@callback(
    Output("decomp-graph", "figure"),
    Input("decomp-model-radio", "value"),
)
def update_decomp_tab(model_type):
    decomp = seasonal_decompose(TS_DF["lrscale_visual"], model=model_type, period=4)
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.05,
                        subplot_titles=("Observada", "Tendencia", "Estacionalidad (4Q)", "Residuos"))
    for idx, (comp, color) in enumerate([(decomp.observed, "#58a6ff"), (decomp.trend, "#f0883e"), (decomp.seasonal, "#3fb950"), (decomp.resid, "#f85149")], start=1):
        fig.add_trace(go.Scatter(x=comp.index, y=comp, mode="lines", line=dict(color=color, width=1.8), showlegend=False), row=idx, col=1)
    fig.update_layout(template="plotly_dark", paper_bgcolor="#161b22", plot_bgcolor="#0d1117", margin=dict(l=40, r=30, t=50, b=30))
    return fig


@callback(
    Output("forecast-graph", "figure"),
    Output("forecast-metrics-card", "children"),
    Input("fc-horizon-slider", "value"),
    Input("shock-gdp-slider", "value"),
    Input("shock-unemp-slider", "value"),
    Input("shock-infl-slider", "value"),
)
def update_forecast_tab(horizon, gdp_shock, unemp_shock, infl_shock):
    future_idx = pd.date_range("2022-01-01", periods=horizon, freq="QS")
    exog_future = pd.DataFrame({col: VAL_DF[col].reindex(future_idx).ffill() for col in EXOG_COLS}, index=future_idx)

    exog_future["gdp_per_capita"] += gdp_shock
    exog_future["unemployment_pct"] = np.clip(exog_future["unemployment_pct"] + unemp_shock, 5.0, 35.0)
    exog_future["inflation_pct"] += infl_shock

    fc_res = BASE_SARIMAX.get_forecast(steps=horizon, exog=exog_future)
    pred_mean = fc_res.predicted_mean
    ci_95 = fc_res.conf_int(alpha=0.05)
    ci_80 = fc_res.conf_int(alpha=0.20)

    real_val = VAL_DF["lr_anchor"].dropna()
    common_dates = real_val.index.intersection(pred_mean.index)
    y_true, y_pred = real_val.loc[common_dates], pred_mean.loc[common_dates]

    rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
    mae = np.mean(np.abs(y_true - y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    metrics_ui = html.Div(style={"display": "flex", "justifyContent": "space-around", "flexWrap": "wrap", "gap": "14px"}, children=[
        html.Div([html.Span("RMSE (Anclas Reales Val): ", style={"color": "#8b949e"}), html.Strong(f"{rmse:.4f}", style={"color": "#58a6ff"})]),
        html.Div([html.Span("MAE: ", style={"color": "#8b949e"}), html.Strong(f"{mae:.4f}", style={"color": "#58a6ff"})]),
        html.Div([html.Span("MAPE: ", style={"color": "#8b949e"}), html.Strong(f"{mape:.2f}%", style={"color": "#58a6ff"})]),
        html.Div([html.Span("AIC (Train): ", style={"color": "#8b949e"}), html.Strong(f"{BASE_SARIMAX.aic:.2f}", style={"color": "#3fb950"})]),
    ])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=TRAIN_DF.index, y=TRAIN_DF["lrscale_float"], mode="lines", name="Train (2002–2021)", line=dict(color="#58a6ff", width=2)))
    fig.add_trace(go.Scatter(
        x=list(pred_mean.index) + list(pred_mean.index[::-1]),
        y=list(ci_95.iloc[:, 1]) + list(ci_95.iloc[:, 0][::-1]),
        fill="toself", fillcolor="rgba(240, 136, 62, 0.15)", line=dict(color="rgba(255,255,255,0)"), name="IC 95%",
    ))
    fig.add_trace(go.Scatter(
        x=list(pred_mean.index) + list(pred_mean.index[::-1]),
        y=list(ci_80.iloc[:, 1]) + list(ci_80.iloc[:, 0][::-1]),
        fill="toself", fillcolor="rgba(240, 136, 62, 0.30)", line=dict(color="rgba(255,255,255,0)"), name="IC 80%",
    ))
    fig.add_trace(go.Scatter(x=pred_mean.index, y=pred_mean, mode="lines+markers", name="Predicción SARIMAX", line=dict(color="#f0883e", width=2.5)))
    fig.add_trace(go.Scatter(x=real_val.index, y=real_val, mode="markers", name="Anclas Reales Validación", marker=dict(color="#3fb950", size=10, symbol="star")))

    fig.update_layout(
        template="plotly_dark", paper_bgcolor="#161b22", plot_bgcolor="#0d1117",
        title="Proyección SARIMAX(1,1,1) y Simulación de Escenarios Macroeconómicos",
        yaxis_title="lrscale (0=Izquierda, 10=Derecha)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=30, t=60, b=40),
    )
    return fig, metrics_ui


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8050)