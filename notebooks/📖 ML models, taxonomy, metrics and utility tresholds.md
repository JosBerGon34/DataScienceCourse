# ML Models: Taxonomy, Metrics, and Utility Thresholds

> Reference document for the course. It's not a tutorial: it's a "cheat sheet".
> to know which model to use, which metric to interpret, and when to use the model
> It really adds something to the basic imputation.

---

## 1. Taxonomy of Models

### 1.1 Supervised (have target) `y`)

| Type | Objective | Examples |
|---|---|---|
| **Regression** | Predict a continuous value | Ridge, Lasso, ElasticNet, HistGradientBoostingRegressor, RandomForestRegressor, SVR, KNN Regressor |
| **Binary Classification** | Predict 1 of 2 classes | Logistic Regression, Hist Gradient Boosting Classifier, Random Forest Classifier, SVC, Gaussian NB, KNN Classifier |
| **Multi-class classification** | Predict 1 of N classes | Same as binary + softmax (NeuralNet), One-vs-Rest |

### 1.2 Unsupervised (no target)

| Type | Objective | Examples |
|---|---|---|
| **Clustering** | Grouping points by similarity | KMeans, DBSCAN, Agglomerative, GMM, HDBSCAN |
| **Dimensionality Reduction** | Compress features while maintaining variance | PCA, t-SNE, UMAP, LDA (supervised) |
| **Anomaly Detection** | Identify outliers | IsolationForest, LocalOutlierFactor, One-Class SVM |
| **Rule Learning** | Discovering Associations | Apriori, FP-Growth |

### 1.3 Semi-supervised / Self-supervised

| Type | Objective | Examples |
|---|---|---|
| **Transductive** | Leveraging unlabeled and minimally labeled data | Label Spreading, Manifold Regularization |
| **Autoencoder** | Reconstruction → latent features | AE, VAE, Denoising AE |
| **Contrastive** | Learning representations by similarity | SimCLR, MoCo, BYOL |

---

## 2. Metrics by Type

### 2.1 Regression

| Metric | Formula / Range | Interpretation | Baseline (basic imputation) |
|---|---|---|---|
| **MAE** | 0 to ∞ | Mean absolute error in target units | `MAE_baseline = mean(|y - mean(y)|)` ≈ 0.8 × SD(y) |
| **RMSE** | 0 to ∞ | Mean squared error (penalizes outliers) | `RMSE_baseline = SD(y)` |
| **R²** | -∞ to 1 | Fraction of variance explained vs. mean | R² = 0 → same as predicting the mean |
| **Adjusted R²** | -∞ to 1 | R² penalized by number of features | Same |
| **MAPE** | 0 to ∞ | Mean percentage error | `mean(|y - mean(y)| / |y|)` |
| **SMAPE** | 0 to 200% | Symmetric MAPE (avoid division by zero) | Same |

#### When is a regression model "useful"?

| Condition | Meaning |
|---|---|
| **R² > 0** | The model reduces the error compared to predicting the mean. It is the absolute minimum. |
| **R² > 0.10** | Explains >10% of the variance. In social sciences (welfare, education, epidemiology) this is already a publishable finding.
| **R² > 0.30** | Moderate signal. The model provides realistic information. |
| **R² > 0.50** | Strong. Excellent in most applied domains. |
| **R² > 0.70** | Very strong. In physics/engineering it's normal; in human data it's exceptional. |
| **R² < 0 (in test)** | The model is **worse** than predicting the mean. Severe overfitting or features that are purely noise. |
| **MAE < 0.5 × SD(y)** | The mean error is less than half the standard deviation of the target. Useful for decision-making. |
| **RMSE < SD(y)** | The model reduces the error vs. the mean. Same threshold as R² > 0. |

> **Rule of thumb:** if your R² in the test is < 0.05 and your MAE is > 0.8 × SD(y),
> the model doesn't contribute anything about `y_pred = mean(y)`Don't use it.

---

### 2.2 Classification

| Metric | Range | Interpretation | Baseline (basic imputation) |
|---|---|---|---|
| **Accuracy** | 0 to 1 | Fraction of correct predictions | `max(prior_pos, prior_neg)` (always the majority class) |
| **Precision** | 0 to 1 | Of those I predicted positive, % that were | `prior_pos` (base rate) |
| **Recall** | 0 to 1 | Of the actual positives, % that I captured | `prior_pos` |
| **F1** | 0 to 1 | Precision harmonic mean and recall | `2 × prior × prior / (prior + prior)` = `prior` |
| **ROC-AUC** | 0 to 1 | Probability that a random positive score > a random negative score | 0.5 (random) |
| **PR-AUC** | 0 to 1 | Area under the Precision-Recall curve | `prior_pos` (base rate) |
| **MCC (Matthews)** | -1 to 1 | Correlation between prediction and reality | 0 (random) |
| **Log Loss** | 0 to ∞ | Calibrated confidence of probabilities | `-mean(p·log(p) + (1-p)·log(1-p))` with p = prior |
| **Brier Score** | 0 to 1 | Squared error of probability | `prior × (1 - prior)` |

#### When is a classification model "useful"?

| Condition | Meaning |
|---|---|
| **AUC > 0.5** | Better than random. Absolute minimum. |
| **AUC > 0.60** | Weak but real signal. Clinically relevant in medical diagnosis.
| **AUC > 0.70** | Moderate signal. Useful for triage/ranking. |
| **AUC > 0.80** | Strong. In most applications it's "good". |
| **AUC > 0.90** | Excellent. Check leakage. |
| **Accuracy > baseline (majority)** | The model classifies better than "always predicting the majority class". |
| **F1 > 2×prior²/(prior+prior)** | Better than the baseline. |
| **MCC > 0.10** | Weak but real correlation between prediction and reality. |
| **MCC > 0.30** | Moderate. The model provides a signal. |
| **MCC > 0.50** | Strong. |

> **Rule of thumb:** if your AUC is < 0.55 and your F1 is < 1.1× the baseline,
> the model doesn't contribute anything about `y_pred = majority_class`Don't use it.

---

### 2.3 Clustering (unsupervised)

| Metric | Range | Interpretation | Baseline |
|---|---|---|---|
| **Silhouette Score** | -1 to 1 | Intra-cluster cohesion vs. inter-cluster separation | 0 = random clusters; -1 = poor |
| **Davies-Bouldin Index** | 0 to ∞ | Inter-cluster separation / intra-cluster size | Lower = better; ~1 = acceptable |
| **Calinski-Harabasz** | 0 to ∞ | Inter-to-intra variance ratio | Higher = better |
| **Inertia (WCSS)** | 0 to ∞ | Sum of distances to centroids | Smaller = more compact (but not comparable between k) |
| **Gap Statistic** | -∞ to ∞ | Difference between observed and expected WCSS under null | Positive = clustering is "real" |

#### When is clustering "useful"?

| Condition | Meaning |
|---|---|
| **Silhouette > 0.10** | Clusters are slightly more compact than random. Minimum. |
| **Silhouette > 0.25** | Moderate structure. Acceptable. |
| **Silhouette > 0.50** | Strong structure. The clusters are "real". |
| **Davies-Bouldin < 1.0** | The clusters are well separated. |
| **Gap Statistic > 0** | Clustering is better than a null random data set. |

> **Rule of thumb:** If your Silhouette is < 0.05, the "clusters" are noise.
> Do not use them as a feature or for segmentation.

---

### 2.4 Dimensionality reduction

| Metrics | Interpretation |
|---|---|
| **PCA Explained Variance** | Fraction of total variance captured by the components. > 0.80 with 2-3 components = good compression. |
| **Error Reconstruction (Autoencoder)** | MSE between input and output. Lower = better. Compare with "predict the mean" (baseline). |
| **Trustworthiness / Contiguity (t-SNE, UMAP)** | 0 to 1. > 0.80 = the 2D/3D structure reflects the original structure. |

---

## 3. The Baseline Hierarchy

Before you can say "my model is good", you must overcome this pyramid:

Level 4: Literature Reference Model  
(the best one published for this type of problem)  
↑  
Level 3: Simple Model (Logistic Regression / Ridge / 1 Tree)  
with the same features  
↑  
Level 2: Business rule / heuristic  
(e.g., "if age > 60 and country = southern → happy = 7")  
↑  
Level 1: Basic arithmetic/statistical imputation  
(mean, median, mode, hot-deck, k-NN imputer)  
↑  
Level 0: Random / constant  
(always predict the same value)


**Your model must exceed at least Level 1 to be "useful".**
If it does not exceed Level 2, the complexity is not justified.
If it surpasses Level 3, it's a good candidate for production.

---

## 4. Summary Table: "Does my model work?"

| Task | Key metric | Baseline (Level 1) | Minimum useful threshold | "Good" threshold |
|---|---|---|---|---|
| Regression | R² (test) | 0 (mean) | > 0.05 | > 0.30 |
| Regression | MAE (test) | 0.8 × SD(y) | < 0.7 × SD(y) | < 0.4 × SD(y) |
| Binary classification | AUC (test) | 0.5 (random) | > 0.55 | > 0.70 |
| Binary classification | F1 (test) | prior | > 1.1 × prior | > 1.5 × prior |
| Multi-classification | Macro F1 (test) | max(prior_i) | > 1.1 × max(prior) | > 1.5 × max(prior) |
| Clustering | Silhouette | 0 (random) | > 0.10 | > 0.25 |
| Clustering | Davies-Bouldin | ~2-3 (random) | < 1.5 | < 1.0 |

---

## 5. Common Interpretation Errors

| Error | Why is it an error? |
|---|---|
| "R² = 0.07 is bad" | In social sciences (welfare, education) 0.05-0.15 is the normal range for a real finding. |
| "Accuracy = 0.95 is excellent" | If the majority class is 95%, a dummy classifier gives 0.95. |
| "AUC = 0.72 is mediocre" | In medical diagnosis, 0.70-0.80 already changes clinical decisions. |
"Silhouette = 0.20 is good" | It depends on the domain. In image data it can be bad; in socioeconomic data it is acceptable.
"The model has R² = 0.95 in training and 0.05 in test." | Extreme overfitting. The model memorized, it didn't learn.
| "RMSE = 2.3 is bad" | Without the target's standard deviation (SD), it cannot be interpreted. If SD = 2.5, it's almost as good as the average. |

---

## 6. References

- [scikit-learn: Model Evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [Chip Huyen, *Designing ML Systems*, Ch. 7](https://d2ml.io)
- [Branco et al. 2016, "A Survey of Predictions with Uncertainty for Imbalanced Data"](https://link.springer.com/article/10.1007/s10994-020-05900-9)
- [NVIDIA: Regression Evaluation Metrics](https://developer.nvidia.com/blog/a-comprehensive-overview-of-regression-evaluation-metrics/)
- [Statistics Fundamentals: What is a Good R²?](https://statisticsfundamentals.com/simple-linear-regression/what-is-a-good-r-squared-value/)   