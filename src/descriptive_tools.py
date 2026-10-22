import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew, kurtosis, shapiro, probplot
import warnings

# Suprimir warnings comunes de seaborn/matplotlib que ensucian el output
warnings.filterwarnings('ignore', category=UserWarning, module='seaborn')
warnings.filterwarnings('ignore', category=FutureWarning, module='seaborn')


# ═══════════════════════════════════════════════════════════════════════
# 1. VARTYPE — Clasificación
# ═══════════════════════════════════════════════════════════════════════
def vartype(df):
    """
    Clasifica cada columna en un tipo estadístico.
    Retorna un dict: {columna: (familia, sub_tipo, descripción)}
    """
    result = {}
    
    for col in df.columns:
        s = df[col].dropna()
        
        # Si la columna está vacía tras quitar nulos
        if len(s) == 0:
            result[col] = ('unknown', 'empty', 'No non-null data')
            continue

        if s.dtype in ['object', 'category'] or (s.nunique() <= 5 and pd.api.types.is_integer_dtype(s)):
            if s.nunique() <= 10:
                result[col] = ('categorical', 'nominal', f'{s.nunique()} categories')
            else:
                result[col] = ('categorical', 'nominal', f'{s.nunique()} categories')
        
        elif pd.api.types.is_numeric_dtype(s):
            n_unique = s.nunique()
            vmin, vmax = s.min(), s.max()
            is_int = s.apply(lambda x: float(x).is_integer()).all()
            
            if is_int and 0 <= vmin and vmax <= 10 and n_unique <= 11:
                result[col] = ('numeric', 'ordinal_bounded', f'range {vmin:.0f}-{vmax:.0f}, {n_unique} values')
            elif is_int and vmin >= 0 and n_unique > 11:
                result[col] = ('numeric', 'discrete_count', f'range {vmin:.0f}-{vmax:.0f}, {n_unique} values')
            elif is_int and n_unique <= 8:
                result[col] = ('numeric', 'ordinal_bounded', f'{n_unique} codes')
            else:
                result[col] = ('numeric', 'continuous', f'range {vmin:.1f}-{vmax:.1f}')
        
        else:
            result[col] = ('unknown', 'unknown', f'dtype={s.dtype}')
    
    return result


def print_vartype(df):
    """Imprime de forma bonita la clasificación de vartype."""
    types = vartype(df)
    print(f"{'='*65}")
    print(f"  TYPOLOGÍA DE VARIABLES  (n={len(df)} filas, {len(df.columns)} cols)")
    print(f"{'='*65}")
    print(f"{'Columna':<15} {'Familia':<12} {'Sub-tipo':<18} {'Detalle'}")
    print(f"{'-'*65}")
    for col, (fam, sub, desc) in types.items():
        print(f"{col:<15} {fam:<12} {sub:<18} {desc}")
    print(f"{'='*65}\n")
    return types


# ═══════════════════════════════════════════════════════════════════════
# 2. STATSGROUP — Perfilado consciente del tipo
# ═══════════════════════════════════════════════════════════════════════
def statsgroup(df, col, var_types=None):
    """
    Imprime un perfil estadístico adaptado al tipo de variable, 
    incluyendo advertencias de diagnóstico.
    """
    if var_types is None:
        var_types = vartype(df[[col]]) # Evaluamos solo la columna necesaria
    
    if col not in var_types:
        print(f"Error: La columna '{col}' no existe en el DataFrame.")
        return

    family, sub_type, desc = var_types[col]
    s = df[col].dropna()
    n = len(s)
    n_null = df[col].isna().sum()
    
    print(f"\n  [{family}/{sub_type}]  (n={n}, nulls={n_null})")
    
    if len(s) == 0:
        print("  ⚠️  WARNING: Columna vacía o solo contiene nulos.")
        return

    # ─── CATEGORICAL / NOMINAL ───────────────────────────────────────────
    if family == 'categorical':
        print(f"\n  Top Valores:")
        vc = s.value_counts()
        for val, cnt in vc.head(5).items():
            bar = '█' * int(cnt / max(1, vc.max()) * 30)
            print(f"    {str(val):<15} {cnt:>6}  ({cnt/n*100:5.1f}%)  {bar}")
        print(f"  Únicos: {s.nunique()}")
        if vc.iloc[0] / n > 0.5:
             print(f"  ⚠️  WARNING: La categoría dominante supera el 50% de los datos.")

    # ─── NUMERIC / ORDINAL BOUNDED ──────────────────────────────────────
    elif sub_type == 'ordinal_bounded':
        print(f"  Media: {s.mean():.4f} | Mediana: {s.median():.4f}")
        moda = s.mode()
        if not moda.empty:
            print(f"  Moda: {moda.iloc[0]:.4f} (freq: {s.value_counts().iloc[0]})")
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        print(f"  Q1/Q3: {q1:.4f} / {q3:.4f} | IQR: {q3-q1:.4f}")
        print(f"  Std: {s.std():.4f}")
        
        sk, ku = skew(s), kurtosis(s)
        print(f"  Skewness: {sk:.4f} | Kurtosis (exceso): {ku:.4f}")
        _diagnostics_ordinal(s, sk, ku)

    # ─── NUMERIC / DISCRETE COUNT ───────────────────────────────────────
    elif sub_type == 'discrete_count':
        print(f"  Media: {s.mean():.4f} | Mediana: {s.median():.4f}")
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        print(f"  Q1/Q3: {q1:.4f} / {q3:.4f} | IQR: {iqr:.4f}")
        print(f"  Min/Max: {s.min():.4f} / {s.max():.4f}")
        
        pct_zero = (s == 0).mean() * 100
        print(f"  % ceros (masa puntual): {pct_zero:.2f}%")
        if pct_zero > 50:
            print(f"  ⚠️  WARNING: >50% de los valores son 0. Considera transformación log1p() si usas modelos lineales.")

    # ─── NUMERIC / CONTINUOUS ───────────────────────────────────────────
    elif sub_type == 'continuous':
        print(f"  Media: {s.mean():.4f} | Mediana: {s.median():.4f}")
        print(f"  Std: {s.std():.4f}")
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        cv = s.std() / s.mean() if s.mean() != 0 else np.nan
        print(f"  Q1/Q3: {q1:.4f} / {q3:.4f} | IQR: {iqr:.4f} | CV: {cv:.4f}")
        
        sk, ku = skew(s), kurtosis(s)
        print(f"  Skewness: {sk:.4f} | Kurtosis: {ku:.4f}")
        
        if n >= 3 and n <= 5000:
            stat, p = shapiro(s)
            verdict = "NO es normal" if p < 0.05 else "No hay evidencia contra la normalidad"
            print(f"  Shapiro-Wilk: p={p:.2e} → {verdict}")
        elif n > 5000:
            stat, p = shapiro(s.sample(5000, random_state=42))
            verdict = "NO es normal" if p < 0.05 else "No hay evidencia contra la normalidad"
            print(f"  Shapiro-Wilk (muestra 5k): p={p:.2e} → {verdict}")
            
        _diagnostics_continuous(s, sk, ku)


def _diagnostics_ordinal(s, sk, ku):
    """Imprime advertencias para variables ordinales (escalas likert)."""
    print(f"  ── Diagnóstico ──")
    if abs(sk) > 0.5:
        dir_str = "derecha" if sk > 0 else "izquierda"
        print(f"  ⚠️  Asimetría {dir_str} (Skewness = {sk:.2f}). La media es arrastrada, prefiere la mediana.")
    if ku < -0.5:
        print(f"  ℹ️  Platicúrtica (Kurtosis = {ku:.2f}). Típico de escalas acotadas (0-10) con datos distribuidos en el centro.")

def _diagnostics_continuous(s, sk, ku):
    """Imprime advertencias para variables continuas."""
    print(f"  ── Diagnóstico ──")
    if abs(sk) > 1:
        print(f"  ⚠️  Fuerte asimetría (Skewness = {sk:.2f}). Recomendable transformar (Box-Cox o log1p).")
    if ku > 2:
        print(f"  ⚠️  Colas pesadas (Kurtosis = {ku:.2f}). Precaución con outliers.")


# ═══════════════════════════════════════════════════════════════════════
# 3. VISUALIZADOR ADAPTATIVO
# ═══════════════════════════════════════════════════════════════════════
def plot_variable(df, col, var_types=None):
    """
    Genera un par de gráficos adaptativos según la tipología detectada por vartype().
    Requiere que matplotlib.pyplot y seaborn estén instalados e importados[cite: 11, 12].
    """
    if var_types is None:
        var_types = vartype(df[[col]])
        
    if col not in var_types:
        return

    family, sub_type, desc = var_types[col]
    s = df[col].dropna()
    
    if len(s) == 0:
        print("No hay datos válidos para graficar.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    if family == 'categorical' or sub_type == 'nominal':
        # Countplot y Pie chart para categóricas
        vc = s.value_counts().head(10)
        sns.barplot(x=vc.values, y=vc.index.astype(str), ax=axes[0], palette='Blues_r')
        axes[0].set_title(f'Top 10 Categorías: {col}')
        axes[0].set_xlabel('Frecuencia')
        
        axes[1].pie(vc.head(5), labels=vc.head(5).index, autopct='%1.1f%%', colors=sns.color_palette('Set2'))
        axes[1].set_title('Proporción Top 5')

    elif sub_type == 'ordinal_bounded':
        # Countplot y Boxplot para escalas Likert acotadas (0-10)
        sns.countplot(x=s, ax=axes[0], palette='Blues')
        axes[0].set_title(f'Distribución Escala Acotada: {col}')
        
        sns.boxplot(x=s, ax=axes[1], color='skyblue')
        axes[1].set_title(f'Boxplot: {col}')

    elif sub_type in ['continuous', 'discrete_count']:
        # Histograma con KDE y QQ-plot para variables numéricas continuas/de conteo
        sns.histplot(s, kde=True, ax=axes[0], color='steelblue', bins='auto')
        axes[0].set_title(f'Histograma + KDE: {col}')
        
        probplot(s, dist="norm", plot=axes[1])
        axes[1].set_title(f'QQ-Plot Normalidad: {col}')
        
    plt.tight_layout()
    plt.show()


# ═══════════════════════════════════════════════════════════════════════
# 4. FUNCIÓN UNIFICADA (ds3on1)
# ═══════════════════════════════════════════════════════════════════════
def ds3on1(df, col, Desc=True, Stat=True, Graph=True):
    """
    Cierra el círculo del análisis univariable en un solo comando.
    Evalúa, diagnostica y grafica dinámicamente una variable.
    
    Parámetros:
    - df: DataFrame completo.
    - col: String con el nombre de la columna (ej: 'happy').
    - Desc (bool): Imprime la clasificación tipológica de la variable.
    - Stat (bool): Imprime las métricas estadísticas y alertas diagnósticas.
    - Graph (bool): Dibuja los gráficos adaptativos según el tipo de dato.
    """
    # Verificación de existencia de columna
    if col not in df.columns:
        print(f"❌ Error: La columna '{col}' no se encuentra en el DataFrame.")
        return

    # 1. MOTOR INTERNO: Clasificamos la variable aislada
    tipologia = vartype(df[[col]]) 
    fam, sub, det = tipologia[col]
    
    print(f"🌟 ANÁLISIS 3-EN-1: [{col.upper()}] 🌟")
    
    # 2. BLOQUE DESCRIPTIVO
    if Desc:
        print(f"\n{'-'*50}")
        print(f"📖 1. DESCRIPCIÓN")
        print(f"{'-'*50}")
        print(f"  Familia estadística : {fam.upper()}")
        print(f"  Subtipo detectado   : {sub.upper()}")
        print(f"  Detalle             : {det}")
    
    # 3. BLOQUE ESTADÍSTICO
    if Stat:
        print(f"\n{'-'*50}")
        print(f"🧮 2. ESTADÍSTICAS Y DIAGNÓSTICO")
        print(f"{'-'*50}")
        statsgroup(df, col, var_types=tipologia)
        
    # 4. BLOQUE GRÁFICO
    if Graph:
        print(f"\n{'-'*50}")
        print(f"📊 3. VISUALIZACIÓN ADAPTATIVA")
        print(f"{'-'*50}")
        plot_variable(df, col, var_types=tipologia)