### 🟢 `< Module 10.2 >` Interactive Time Series EDA & Forecasting Dashboard (Plotly Dash)

#### 🎯 Context & Objectives

While Module 10.1 demonstrated decoupled client-server REST inference on cross-sectional tabular data, real-world Data Science teams frequently need self-contained, reactive analytical dashboards to explore temporal dynamics without writing separate HTML/JavaScript frontends.

In this module, you will build a reactive multi-tab web application using **Plotly Dash** (`src/dash_timeseries.py`). Because the European Social Survey (ESS) biennial waves (~11 time steps) and annual Eurostat series (~10–13 observations) lack the temporal resolution required for intra-annual seasonality modeling, you will work with a classic high-frequency benchmark dataset (e.g., _Monthly Airline Passengers_ or _Mauna Loa Atmospheric CO2_) to perform statistical stationarity diagnostics, seasonal decomposition, and multi-step forecasting.

#### 📑 Exercise Instructions

##### 1. Environment & Data Ingestion (`notebooks/Ex10.2_ts_exploration.ipynb` & `src/dash_timeseries.py`)

- **Dependency Verification:** Ensure `dash` and `statsmodels` are available inside your isolated environment (`.venv-core` / `ReqJupML.txt`).
    
- **High-Frequency Dataset Loading:** Load a univariate monthly time series dataset (`statsmodels.datasets.co2` or classic _AirPassengers_ CSV) with a clean `DatetimeIndex` and explicit frequency (`MS` or `M`), handling any missing timestamps deterministically via linear interpolation before modeling.
    
- **Train / Validation Temporal Split:** Partition the series chronologically (never randomly, to prevent look-ahead leakage)—for example, holding out the last 24 months as the validation window.
    

##### 2. Reactive Dash Architecture (`dcc.Tabs` & `@callback`)

Structure `src/dash_timeseries.py` into **three reactive tabs** driven by Dash callbacks (`@app.callback`):

1. **Tab 1 — Temporal EDA & Stationarity Diagnostics:**
    
    - Render an interactive Plotly time series chart equipped with a `dcc.RangeSlider` (or Plotly rangeslider) and a rolling-window slider ($k \in [3, 24]$ months) to overlay the **Rolling Mean** and **Rolling Standard Deviation** dynamically.
        
    - Implement a toggle (`dcc.RadioItems`) to switch between the **Original Series** and **First-Order Differencing** ($\Delta y_t = y_t - y_{t-1}$).
        
    - Compute and display in real time the **Augmented Dickey-Fuller (ADF) Test** (`statsmodels.tsa.stattools.adfuller`), reporting the ADF statistic, $p$-value, critical values, and an automated stationarity verdict ($p < 0.05$).
        
2. **Tab 2 — Seasonal Decomposition:**
    
    - Apply `statsmodels.tsa.seasonal.seasonal_decompose` and render a synchronized 4-panel subplot (**Observed**, **Trend**, **Seasonal**, **Residual**).
        
    - Connect a `dcc.RadioItems` selector allowing the user to switch between **Additive** ($Y_t = T_t + S_t + R_t$) and **Multiplicative** ($Y_t = T_t \times S_t \times R_t$) models on the fly.
        
3. **Tab 3 — Interactive Forecasting & Error Evaluation:**
    
    - Fit a seasonal forecasting model (`SARIMAX` or `ExponentialSmoothing` with Holt-Winters additive/multiplicative seasonality) strictly on the historical training split.
        
    - Provide a forecast horizon slider ($h \in [6, 48]$ months) that projects future values along with **80% and 95% confidence intervals** (`get_forecast().conf_int()`), overlaying the held-out validation ground truth.
        
    - Render a live metrics card computing **RMSE**, **MAE**, **MAPE**, and **AIC** over the overlapping validation window.
        

#### 📚 Official Documentation & Reference Sheets

- **Plotly Dash Core Components & Callbacks:** [https://dash.plotly.com/basic-callbacks](https://dash.plotly.com/basic-callbacks)
    
- **Statsmodels Time Series Analysis (`tsa`):** [https://www.statsmodels.org/stable/tsa.html](https://www.statsmodels.org/stable/tsa.html)
    
- **Augmented Dickey-Fuller (`adfuller`) & Seasonal Decompose:** [https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.adfuller.html](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.adfuller.html)
    
- **SARIMAX Forecasting & Confidence Intervals:** [https://www.statsmodels.org/stable/generated/statsmodels.tsa.statespace.sarimax.SARIMAXResults.get_forecast.html](https://www.statsmodels.org/stable/generated/statsmodels.tsa.statespace.sarimax.SARIMAXResults.get_forecast.html)
    

#### ✅ Deliverables Checklist

1. `notebooks/Ex10.2_ts_exploration.ipynb` (prototyping ADF tests, ACF/PACF inspection, and model order selection before moving logic to the Dash script).
    
2. `src/dash_timeseries.py` (standalone Dash server running cleanly on `[http://127.0.0.1:8050](http://127.0.0.1:8050)`).
    
3. Rendered Markdown summary in `docs/Corrections/Ex10.2.md` linked from `docs/index.md`.