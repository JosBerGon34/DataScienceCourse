

🟢 < Module 2.1 > Calculus & Linear Algebra for Machine Learning

## 🎯 Context & Objectives
In quantitative sociology and comparative political economy, country profiles are represented as continuous feature vectors derived from aggregated survey microdata (e.g., European Social Survey). Distance metrics determine cluster membership (e.g., $k$-means), while orthogonal projections isolate specific sub-dimensional influences.

In this exercise, you will build a modular, vectorized geometric analysis engine using NumPy to perform vector operations, distance calculations, and feature projections[cite: 21].

---

## 📑 Exercise Instructions

### 1. Vector Specification & Algebraic Operations
Construct two 1D NumPy arrays with `dtype=np.float64`[cite: 21]:
* $\mathbf{u} = [180.0, 7.0, 2.0, 4.0]^T$ (Country A)[cite: 21]
* $\mathbf{v} = [210.0, 5.0, 6.0, 3.0]^T$ (Country B)[cite: 21]

### 2. Function Implementation
Write a Python function `compute_vector_metrics(u: np.ndarray, v: np.ndarray) -> dict` that computes and returns a dictionary containing[cite: 21]:
* `'dot_product'`: $\mathbf{u}^T \mathbf{v}$[cite: 21]
* `'l2_norm_u'`: $\Vert\mathbf{u}\Vert_2$[cite: 21]
* `'l2_norm_v'`: $\Vert\mathbf{v}\Vert_2$[cite: 21]
* `'euclidean_distance'`: $\Vert\mathbf{u} - \mathbf{v}\Vert_2$[cite: 21]
* `'cosine_similarity'`: $\frac{\mathbf{u}^T \mathbf{v}}{\Vert\mathbf{u}\Vert_2 \Vert\mathbf{v}\Vert_2}$[cite: 21]
* `'projection_u_on_v'`: $\text{proj}_{\mathbf{v}}(\mathbf{u}) = \left(\frac{\mathbf{u}^T \mathbf{v}}{\mathbf{v}^T \mathbf{v}}\right)\mathbf{v}$[cite: 21]

---

## 🌐 Official References & Documentation
* **NumPy Linear Algebra Routines**: [NumPy linalg Documentation](https://numpy.org/doc/stable/reference/routines.linalg.html)[cite: 21]
* **Scikit-Learn Distance Metrics**: [Scikit-Learn Distance Metrics Specification](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.euclidean_distances.html)[cite: 21]

---
> 💻 **Your Challenge:** Implement the script locally, compute the geometric metrics, and verify your vector projections before moving on to Module 2.2! 🚀📊

