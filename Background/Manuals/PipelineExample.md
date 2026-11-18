# Diseño pipeline de  feature engineering: Preparacion columnas y clusterizacion + pipeline imblearn clasico

# Capa 1 custom:
#
#         A) Seleccion de dataframes, pudiendo ser uno o varios, indicando las variable/columnas nexo y restrictivas, por ejemplo si tengo un panel economico con datos de diferentes años donde year es una columna y cada fila  tiene unos datos para ese valor concreto, se podra indicar que filas son validas.
#         Ademas podremos escoger la variable nexo , independientemente del nombre, no tienen porque coincidir, el input de esta parte de la funcion dejara introducir el numero de dataframes, los valores unicos de columna que restringiran que filas usar y los valores unicos de la  columna nexo por el cual #
#         se hara el  merge o concat.
#         B) Asignacion de variables predictoras "X" y variable target 'y', con su columna dummy flag is_test = 1, identificando naturaleza de variable.  Y grupo de control "cntry", "cluster1economico", "Cluster2regional"(['eastern','western','northern','Southern',]), etc.
#         C) Cebado de clases minoritarias en el grupo de entreno X e Y, y flaggeadas como is_synth = 1, usando SMOTE o SMOTENC en funcion de lo detectado en el paso B
#         D) Generacion de columnas cluster factorizadas introduciendo las columnas que han de crear esta clasificacion. Parametrizando la naturaleza de los numeros en funcion de su significado
#         por ejemplo estipularemos en el input de estas columnas mediante  la inversa, si las columnas negativas estan en negativo se considerara un numero positivo  y ademas cuanto mas grande sea el numero positivo al dividir 1 entre ese numero se contara como un indicador clave en la clusterizacion
#         Ejemplo de input: EcoCluster = ['PIB',1/'inflation',1/'unemployment'] # En este caso al hacer el valor inverso ajustamos la direccion y formato  de numeros para que cuadren con un numero grande con las columnas positivas.
#
# Capa 2 imblearn pipeline  anidado :
#         A) Tipo  de  data transform,
#         B) Modelo de regresion/classificacion usado,
#         C) Split train test configurado en la capa 1 en funcion de las flags y columnas seleccionadas,
#         D) Uso de groupkfold con elgrupo de control,D) parrila de hiperparametrizacion si el usuario estipula True en el input.
#         E) Prints devueltos de scores relacionados.

df91 (virgen)
  │
  ▼
prepare_features(df91, spec_91)     ← Capa 1
  ├── Invierte inflation, unemployment
  ├── Máscara is_test / is_synthetic
  ├── MinMax 0-10 + round
  ├── KMeans → macro_cluster
  ├── SMOTENC → filas sintéticas + tag
  └── Devuelve PipelineOutput (df91 intacto)
  │
  ▼
run_model(result, "logistic")       ← Capa 2
  ├── ImbPipeline([model])
  ├── GroupKFold (si grid_search=True)
  └── Devuelve pipe + scores   

# ============================================================
# CAPA 1: Feature Engineering Pipeline (custom)
# ============================================================

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE, SMOTENC
from sklearn.cluster import KMeans

class VarType(Enum):
    DISCRETE = "discrete"
    CONTINUOUS = "continuous"
    CATEGORICAL = "categorical"
    FLAG = "flag"

class Transform(Enum):
    IDENTITY = "identity"
    INVERSE = "inverse"       # 1/x (ajusta dirección)
    REVERSE = "reverse"       # max - x

@dataclass(frozen=True)
class ColumnSpec:
    name: str
    vtype: VarType
    transform: Transform = Transform.IDENTITY
    range: tuple = (0, 10)

@dataclass(frozen=True)
class DatasetSpec:
    columns: list[ColumnSpec]
    target: str
    group: str
    cluster_cols: list[str] = field(default_factory=list)
    n_clusters: int = 3

    @property
    def feature_cols(self) -> list[str]:
        return [c.name for c in self.columns if c.vtype in (VarType.DISCRETE, VarType.CONTINUOUS)]

    @property
    def discrete_cols(self) -> list[str]:
        return [c.name for c in self.columns if c.vtype == VarType.DISCRETE]

    @property
    def categorical_cols(self) -> list[str]:
        return [c.name for c in self.columns if c.vtype == VarType.CATEGORICAL]

@dataclass
class PipelineOutput:
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series
    groups_train: pd.Series
    groups_test: pd.Series
    cluster_labels: pd.Series
    spec: DatasetSpec


def prepare_features(
    df: pd.DataFrame,
    spec: DatasetSpec,
    n_neighbors_smote: int = 5,
    seed: int = 42,
) -> PipelineOutput:
    """
    Capa 1: Ajusta dirección, escala, clusteriza, aplica SMOTE al vuelo,
    taggea sintéticas. NO muta el DataFrame original.
    """
    rng = np.random.default_rng(seed)
    df_work = df.copy()

    # --- A) Ajuste de dirección (inverse / reverse) ---
    for col_spec in spec.columns:
        if col_spec.name not in df_work.columns:
            continue
        if col_spec.transform == Transform.INVERSE:
            # (max + 1) / (x + 1) → evita división por cero
            df_work[col_spec.name] = (df_work[col_spec.name].max() + 1) / (df_work[col_spec.name] + 1)
        elif col_spec.transform == Transform.REVERSE:
            df_work[col_spec.name] = df_work[col_spec.name].max() - df_work[col_spec.name]

    # --- B) Máscara train/test (flags) ---
    mask_test  = (df_work["is_test"] == 1) & (df_work["is_synthetic"] == 0)
    mask_train = (df_work["is_test"] == 0)

    feat = spec.feature_cols
    X_train = df_work.loc[mask_train, feat].copy()
    y_train = df_work.loc[mask_train, spec.target].copy()
    X_test  = df_work.loc[mask_test,  feat].copy()
    y_test  = df_work.loc[mask_test,  spec.target].copy()

    groups_train = df_work.loc[mask_train, spec.group].copy()
    groups_test  = df_work.loc[mask_test,  spec.group].copy()

    # --- C) MinMax 0-10 + round (solo DISCRETE) ---
    scaler = MinMaxScaler(feature_range=(0, 10))
    X_train[feat] = scaler.fit_transform(X_train[feat])
    X_test[feat]  = scaler.transform(X_test[feat])

    for col in spec.discrete_cols:
        X_train[col] = X_train[col].round().clip(0, 10).astype(int)
        X_test[col]  = X_test[col].round().clip(0, 10).astype(int)

    # --- D) Clusterización (solo si se especifican cluster_cols) ---
    cluster_labels = pd.Series(index=df_work.index, dtype=object)
    if spec.cluster_cols:
        # Re-adjuntar cntry para SMOTENC
        X_train_cntry = X_train.copy()
        X_train_cntry["cntry"] = groups_train.values
        X_test_cntry  = X_test.copy()
        X_test_cntry["cntry"]  = groups_test.values

        # KMeans sobre cluster_cols (ya alineadas por direction)
        km = KMeans(n_clusters=spec.n_clusters, random_state=seed, n_init=10)
        cluster_labels.loc[mask_train] = km.fit_predict(X_train_cntry[spec.cluster_cols])
        cluster_labels.loc[mask_test]  = km.predict(X_test_cntry[spec.cluster_cols])

        # Factorizar como columna
        X_train_cntry["macro_cluster"] = cluster_labels.loc[mask_train].values
        X_test_cntry["macro_cluster"]  = cluster_labels.loc[mask_test].values

        # --- E) SMOTE / SMOTENC al vuelo (solo sobre originales) ---
        # Detectar si ya hay sintéticas en train
        if "is_synthetic" in X_train_cntry.columns:
            mask_orig = X_train_cntry["is_synthetic"] == 0
        else:
            mask_orig = pd.Series(True, index=X_train_cntry.index)

        X_train_orig = X_train_cntry.loc[mask_orig].copy()
        y_train_orig = y_train.loc[mask_orig].copy()

        # ¿Necesita resampling? (solo si hay desbalance en originales)
        class_counts = y_train_orig.value_counts()
        needs_smote = (class_counts.min() / class_counts.max()) < 0.5

        if needs_smote:
            cat_idx = [i for i, c in enumerate(X_train_orig.columns) if c in spec.categorical_cols]
            if cat_idx:
                smote = SMOTENC(categorical_features=cat_idx, k_neighbors=n_neighbors_smote, random_state=seed)
            else:
                smote = SMOTE(k_neighbors=n_neighbors_smote, random_state=seed)

            X_res, y_res = smote.fit_resample(X_train_orig, y_train_orig)

            # Rounding post-SMOTE en discretas
            for col in spec.discrete_cols:
                X_res[col] = X_res[col].round().clip(0, 10).astype(int)

            n_new_synth = len(X_res) - len(X_train_orig)

            # Unir: originales + sintéticas nuevas + sintéticas previas (si las había)
            X_new_synth = X_res.iloc[len(X_train_orig):]
            X_prev_synth = X_train_cntry.loc[~mask_orig].copy() if (~mask_orig).any() else pd.DataFrame()

            X_train_final = pd.concat([X_train_orig, X_new_synth, X_prev_synth], ignore_index=True)
            y_train_final = pd.concat([y_train_orig, y_res.iloc[len(X_train_orig):],
                                        y_train.loc[~mask_orig].reset_index(drop=True) if (~mask_orig).any() else pd.Series()],
                                       ignore_index=True)

            # Tags: 0 = original, 1 = sintética (nueva o previa)
            n_orig_total = len(X_train_orig)
            n_synth_total = len(X_train_final) - n_orig_total
            X_train_final["is_synthetic"] = [0] * n_orig_total + [1] * n_synth_total

            # groups con sintéticas
            groups_train_final = pd.Series(
                list(groups_train.loc[mask_orig].values) +
                list(X_res["cntry"].iloc[len(X_train_orig):].values) +
                list(groups_train.loc[~mask_orig].values) if (~mask_orig).any() else []
            ).reset_index(drop=True)

        else:
            # Ya está balanceado, no tocar
            X_train_final = X_train_cntry
            y_train_final = y_train
            groups_train_final = groups_train

    else:
        X_train_final = X_train
        y_train_final = y_train
        groups_train_final = groups_train     
# ============================================================
# CAPA 2: Pipeline imblearn (consume PipelineOutput, NO toca df91)
# ============================================================

from sklearn.model_selection import GroupKFold
from sklearn.linear_model import LogisticRegression
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.metrics import classification_report, f1_score

def run_model(
    output: PipelineOutput,
    model_type: str = "logistic",
    n_splits: int = 5,
    grid_search: bool = False,
    seed: int = 42,
):
    """
    Capa 2: Pipeline de imblearn anidado.
    Recibe PipelineOutput, no el DataFrame original.
    """
    MODEL_REGISTRY = {
        "logistic": LogisticRegression,
        # "rf": RandomForestClassifier,
        # "xgb": XGBClassifier,
    }
    PARAM_GRIDS = {
        "logistic": {"C": [0.01, 0.1, 1, 10], "penalty": ["l1", "l2"]},
    }

    feat = output.spec.feature_cols
    X_train, X_test = output.X_train[feat], output.X_test[feat]
    y_train, y_test = output.y_train, output.y_test
    groups = output.groups_train

    # Pipeline
    steps = []
    model_cls = MODEL_REGISTRY[model_type]

    if grid_search:
        from sklearn.model_selection import GridSearchCV
        gkf = GroupKFold(n_splits=n_splits)
        gs = GridSearchCV(
            model_cls(random_state=seed),
            PARAM_GRIDS[model_type],
            cv=gkf,
            scoring="f1",
            n_jobs=-1,
        )
        steps.append(("model", gs))
    else:
        steps.append(("model", model_cls(random_state=seed)))

    pipe = ImbPipeline(steps)

    # Fit
    pipe.fit(X_train, y_train)

    # Predict + Scores
    y_pred = pipe.predict(X_test)
    print(f"\n{'='*50}")
    print(f"Modelo: {model_type} | Grid: {grid_search}")
    print(f"{'='*50}")
    print(f"F1 (test): {f1_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred, target_names=["happy_low", "happy_high"]))

    if grid_search:
        print(f"Best params: {pipe.named_steps['model'].best_params_}")
        print(f"Best CV F1:  {pipe.named_steps['model'].best_score_:.4f}")

    return pipe   

# ============================================================
# LLAMADA: Spec + Ejecución
# ============================================================

spec_91 = DatasetSpec(
    columns=[
        ColumnSpec("lrscale",      VarType.DISCRETE,   transform=Transform.IDENTITY),
        ColumnSpec("trust",        VarType.DISCRETE,   transform=Transform.IDENTITY),
        ColumnSpec("n_nonresp",    VarType.DISCRETE,   transform=Transform.IDENTITY),
        ColumnSpec("has_nonresp",  VarType.DISCRETE,   transform=Transform.IDENTITY),
        ColumnSpec("gdp_growth",   VarType.CONTINUOUS, transform=Transform.IDENTITY),
        ColumnSpec("inflation",    VarType.CONTINUOUS, transform=Transform.INVERSE),
        ColumnSpec("unemployment", VarType.CONTINUOUS, transform=Transform.INVERSE),
        ColumnSpec("cntry",        VarType.CATEGORICAL),
        ColumnSpec("is_test",      VarType.FLAG),
        ColumnSpec("is_synthetic", VarType.FLAG),
    ],
    target="happy_high",
    group="cntry",
    cluster_cols=["gdp_growth", "inflation", "unemployment"],
    n_clusters=3,
)

# Capa 1: preparar datos (df91 queda intacto)
result = prepare_features(df91, spec_91, n_neighbors_smote=5, seed=42)

print(f"Train: {result.X_train.shape} | Test: {result.X_test.shape}")
print(f"Clusters: {result.cluster_labels.value_counts().to_dict()}")
print(f"Sintéticas en train: {result.X_train['is_synthetic'].sum() if 'is_synthetic' in result.X_train.columns else 'N/A'}")

# Capa 2: entrenar y evaluar
pipe = run_model(result, model_type="logistic", n_splits=5, grid_search=False, seed=42)   lse, seed=42)
