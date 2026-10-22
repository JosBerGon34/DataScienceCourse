import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew, kurtosis, shapiro, probplot
import warnings

# Suppress common seaborn/matplotlib warnings to keep output clean
warnings.filterwarnings('ignore', category=UserWarning, module='seaborn')
warnings.filterwarnings('ignore', category=FutureWarning, module='seaborn')


# ═══════════════════════════════════════════════════════════════════════
# 1. VARTYPE — Classification
# ═══════════════════════════════════════════════════════════════════════
def vartype(df):
    """
    Classifies each column into a statistical type.
    Returns a dict: {column: (family, sub_type, description)}
    """
    result = {}
    
    for col in df.columns:
        s = df[col].dropna()
        
        # If the column is empty after dropping nulls
        if len(s) == 0:
            result[col] = ('unknown', 'empty', 'No non-null data')
            continue

        # Categorical check
        if s.dtype in ['object', 'category'] or (s.nunique() <= 5 and pd.api.types.is_integer_dtype(s)):
            if s.nunique() <= 10:
                result[col] = ('categorical', 'nominal', f'{s.nunique()} categories')
            else:
                result[col] = ('categorical', 'nominal', f'{s.nunique()} categories')
        
        # Numeric check
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
    """Pretty-prints the vartype classification."""
    types = vartype(df)
    print(f"{'='*65}")
    print(f"  VARIABLE TYPOLOGY  (n={len(df)} rows, {len(df.columns)} cols)")
    print(f"{'='*65}")
    print(f"{'Column':<15} {'Family':<12} {'Sub-type':<18} {'Detail'}")
    print(f"{'-'*65}")
    for col, (fam, sub, desc) in types.items():
        print(f"{col:<15} {fam:<12} {sub:<18} {desc}")
    print(f"{'='*65}\n")
    return types


# ═══════════════════════════════════════════════════════════════════════
# 2. STATSGROUP — Type-aware profiling
# ═══════════════════════════════════════════════════════════════════════
def statsgroup(df, col, var_types=None):
    """
    Prints a statistical profile adapted to the variable type, 
    including diagnostic warnings.
    """
    if var_types is None:
        var_types = vartype(df[[col]]) # Evaluate only the required column
    
    if col not in var_types:
        print(f"Error: Column '{col}' does not exist in the DataFrame.")
        return

    family, sub_type, desc = var_types[col]
    s = df[col].dropna()
    n = len(s)
    n_null = df[col].isna().sum()
    
    print(f"\n  [{family}/{sub_type}]  (n={n}, nulls={n_null})")
    
    if len(s) == 0:
        print("  ⚠️  WARNING: Empty column or contains only nulls.")
        return

    # ─── CATEGORICAL / NOMINAL ───────────────────────────────────────────
    if family == 'categorical':
        print(f"\n  Top Values:")
        vc = s.value_counts()
        for val, cnt in vc.head(5).items():
            bar = '█' * int(cnt / max(1, vc.max()) * 30)
            print(f"    {str(val):<15} {cnt:>6}  ({cnt/n*100:5.1f}%)  {bar}")
        print(f"  Unique: {s.nunique()}")
        if vc.iloc[0] / n > 0.5:
             print(f"  ⚠️  WARNING: The dominant category exceeds 50% of the data.")

    # ─── NUMERIC / ORDINAL BOUNDED ──────────────────────────────────────
    elif sub_type == 'ordinal_bounded':
        print(f"  Mean: {s.mean():.4f} | Median: {s.median():.4f}")
        moda = s.mode()
        if not moda.empty:
            print(f"  Mode: {moda.iloc[0]:.4f} (freq: {s.value_counts().iloc[0]})")
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        print(f"  Q1/Q3: {q1:.4f} / {q3:.4f} | IQR: {q3-q1:.4f}")
        print(f"  Std: {s.std():.4f}")
        
        sk, ku = skew(s), kurtosis(s)
        print(f"  Skewness: {sk:.4f} | Kurtosis (excess): {ku:.4f}")
        _diagnostics_ordinal(s, sk, ku)

    # ─── NUMERIC / DISCRETE COUNT ───────────────────────────────────────
    elif sub_type == 'discrete_count':
        print(f"  Mean: {s.mean():.4f} | Median: {s.median():.4f}")
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        print(f"  Q1/Q3: {q1:.4f} / {q3:.4f} | IQR: {iqr:.4f}")
        print(f"  Min/Max: {s.min():.4f} / {s.max():.4f}")
        
        pct_zero = (s == 0).mean() * 100
        print(f"  % zeros (point mass): {pct_zero:.2f}%")
        if pct_zero > 50:
            print(f"  ⚠️  WARNING: >50% of values are 0. Consider log1p() transformation if using linear models.")

    # ─── NUMERIC / CONTINUOUS ───────────────────────────────────────────
    elif sub_type == 'continuous':
        print(f"  Mean: {s.mean():.4f} | Median: {s.median():.4f}")
        print(f"  Std: {s.std():.4f}")
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        cv = s.std() / s.mean() if s.mean() != 0 else np.nan
        print(f"  Q1/Q3: {q1:.4f} / {q3:.4f} | IQR: {iqr:.4f} | CV: {cv:.4f}")
        
        sk, ku = skew(s), kurtosis(s)
        print(f"  Skewness: {sk:.4f} | Kurtosis: {ku:.4f}")
        
        if n >= 3 and n <= 5000:
            stat, p = shapiro(s)
            verdict = "NOT normal" if p < 0.05 else "No evidence against normality"
            print(f"  Shapiro-Wilk: p={p:.2e} → {verdict}")
        elif n > 5000:
            stat, p = shapiro(s.sample(5000, random_state=42))
            verdict = "NOT normal" if p < 0.05 else "No evidence against normality"
            print(f"  Shapiro-Wilk (5k sample): p={p:.2e} → {verdict}")
            
        _diagnostics_continuous(s, sk, ku)


def _diagnostics_ordinal(s, sk, ku):
    """Prints warnings for ordinal (Likert scale) variables."""
    print(f"  ── Diagnostics ──")
    if abs(sk) > 0.5:
        dir_str = "right" if sk > 0 else "left"
        print(f"  ⚠️  {dir_str.capitalize()} skew (Skewness = {sk:.2f}). Mean is pulled, prefer median.")
    if ku < -0.5:
        print(f"  ℹ️  Platykurtic (Kurtosis = {ku:.2f}). Typical of bounded scales (0-10) with centered data.")

def _diagnostics_continuous(s, sk, ku):
    """Prints warnings for continuous variables."""
    print(f"  ── Diagnostics ──")
    if abs(sk) > 1:
        print(f"  ⚠️  Heavy skew (Skewness = {sk:.2f}). Transformation recommended (Box-Cox or log1p).")
    if ku > 2:
        print(f"  ⚠️  Heavy tails (Kurtosis = {ku:.2f}). Caution with outliers.")


# ═══════════════════════════════════════════════════════════════════════
# 3. ADAPTIVE VISUALIZER
# ═══════════════════════════════════════════════════════════════════════
def plot_variable(df, col, var_types=None):
    """
    Generates a pair of adaptive plots based on the typology detected by vartype().
    Requires matplotlib.pyplot and seaborn to be installed and imported.
    """
    if var_types is None:
        var_types = vartype(df[[col]])
        
    if col not in var_types:
        return

    family, sub_type, desc = var_types[col]
    s = df[col].dropna()
    
    if len(s) == 0:
        print("No valid data to plot.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    if family == 'categorical' or sub_type == 'nominal':
        # Countplot and Pie chart for categorical data
        vc = s.value_counts().head(10)
        sns.barplot(x=vc.values, y=vc.index.astype(str), ax=axes[0], palette='Blues_r')
        axes[0].set_title(f'Top 10 Categories: {col}')
        axes[0].set_xlabel('Frequency')
        
        axes[1].pie(vc.head(5), labels=vc.head(5).index, autopct='%1.1f%%', colors=sns.color_palette('Set2'))
        axes[1].set_title('Top 5 Proportion')

    elif sub_type == 'ordinal_bounded':
        # Countplot and Boxplot for bounded Likert scales (0-10)
        sns.countplot(x=s, ax=axes[0], palette='Blues')
        axes[0].set_title(f'Bounded Scale Distribution: {col}')
        
        sns.boxplot(x=s, ax=axes[1], color='skyblue')
        axes[1].set_title(f'Boxplot: {col}')

    elif sub_type in ['continuous', 'discrete_count']:
        # Histogram with KDE and QQ-plot for continuous/count numerical variables
        sns.histplot(s, kde=True, ax=axes[0], color='steelblue', bins='auto')
        axes[0].set_title(f'Histogram + KDE: {col}')
        
        probplot(s, dist="norm", plot=axes[1])
        axes[1].set_title(f'QQ-Plot Normality: {col}')
        
    plt.tight_layout()
    plt.show()


# ═══════════════════════════════════════════════════════════════════════
# 4. UNIFIED FUNCTION (ds3on1)
# ═══════════════════════════════════════════════════════════════════════
def ds3on1(df, col, Desc=True, Stat=True, Graph=True):
    """
    Closes the univariate analysis loop in a single command.
    Dynamically evaluates, diagnoses, and plots a variable.
    
    Parameters:
    - df: Complete DataFrame.
    - col: String with the column name (e.g., 'happy').
    - Desc (bool): Prints the typological classification of the variable.
    - Stat (bool): Prints statistical metrics and diagnostic alerts.
    - Graph (bool): Draws adaptive plots based on the data type.
    """
    # Verify column existence
    if col not in df.columns:
        print(f"❌ Error: Column '{col}' not found in DataFrame.")
        return

    # 1. INTERNAL ENGINE: Classify the isolated variable
    tipologia = vartype(df[[col]]) 
    fam, sub, det = tipologia[col]
    
    print(f"🌟 3-IN-1 ANALYSIS: [{col.upper()}] 🌟")
    
    # 2. DESCRIPTIVE BLOCK
    if Desc:
        print(f"\n{'-'*50}")
        print(f"📖 1. DESCRIPTION")
        print(f"{'-'*50}")
        print(f"  Statistical family  : {fam.upper()}")
        print(f"  Detected sub-type   : {sub.upper()}")
        print(f"  Detail              : {det}")
    
    # 3. STATISTICAL BLOCK
    if Stat:
        print(f"\n{'-'*50}")
        print(f"🧮 2. STATISTICS & DIAGNOSTICS")
        print(f"{'-'*50}")
        statsgroup(df, col, var_types=tipologia)
        
    # 4. GRAPHICAL BLOCK
    if Graph:
        print(f"\n{'-'*50}")
        print(f"📊 3. ADAPTIVE VISUALIZATION")
        print(f"{'-'*50}")
        plot_variable(df, col, var_types=tipologia)