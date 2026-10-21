## 📘 Lesson 2.1: Vector Spaces, Distance Metrics & Feature Projections

### 📐 1. Syntactic-Algebraic Foundation

In Data Science and Machine Learning, an observation with $d$ numerical attributes is modeled as a vector in a $d$-dimensional real vector space $\mathbb{R}^d$:

$$\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_d \end{bmatrix} \in \mathbb{R}^d$$

#### **A. Inner Product (Dot Product)**

The canonical inner product between two column vectors $\mathbf{u}, \mathbf{v} \in \mathbb{R}^d$ maps two vectors to a scalar field $\mathbb{R}$:

$$\langle \mathbf{u}, \mathbf{v} \rangle = \mathbf{u}^T \mathbf{v} = \sum_{i=1}^{d} u_i v_i = u_1 v_1 + u_2 v_2 + \dots + u_d v_d$$

_Properties_:

1. **Symmetry**: $\mathbf{u}^T \mathbf{v} = \mathbf{v}^T \mathbf{u}$
    
2. **Linearity**: $(a\mathbf{u} + b\mathbf{w})^T \mathbf{v} = a(\mathbf{u}^T \mathbf{v}) + b(\mathbf{w}^T \mathbf{v}), \quad \forall a,b \in \mathbb{R}$
    
3. **Positive-Definiteness**: $\mathbf{u}^T \mathbf{u} \ge 0$, and $\mathbf{u}^T \mathbf{u} = 0 \iff \mathbf{u} = \mathbf{0}$
    

#### **B. Vector Norms & Euclidean Distance**

The $L_2$ norm (Euclidean length) of a vector is derived directly from the inner product:

$$\Vert{}\mathbf{u}\Vert{}_2 = \sqrt{\langle \mathbf{u}, \mathbf{u} \rangle} = \sqrt{\mathbf{u}^T \mathbf{u}} = \sqrt{\sum_{i=1}^{d} u_i^2}$$

The **Euclidean Distance** $d_E(\mathbf{u}, \mathbf{v})$ measures the geometric separation between two points in $\mathbb{R}^d$:

$$d_E(\mathbf{u}, \mathbf{v}) = \Vert{}\mathbf{u} - \mathbf{v}\Vert{}_2 = \sqrt{\sum_{i=1}^{d} (u_i - v_i)^2}$$

#### **C. Cosine Similarity & Angle Between Vectors**

By the Cauchy-Schwarz Inequality ($\vert{}\mathbf{u}^T \mathbf{v}\vert{} \le \Vert{}\mathbf{u}\Vert{}_2 \Vert{}\mathbf{v}\Vert{}_2$), the geometric angle $\theta \in [0, \pi]$ between non-zero vectors satisfies:

$$\cos(\theta) = \frac{\mathbf{u}^T \mathbf{v}}{\Vert{}\mathbf{u}\Vert{}_2 \Vert{}\mathbf{v}\Vert{}_2}$$

- **Cosine Similarity** ($\text{Sim}_{\cos} \in [-1, 1]$): Measures directional alignment independent of vector magnitude.
    
- **Cosine Distance**: $d_{\cos}(\mathbf{u}, \mathbf{v}) = 1 - \text{Sim}_{\cos}(\mathbf{u}, \mathbf{v})$.
    

#### **D. Orthogonal Vector Projection**

The orthogonal projection of vector $\mathbf{u}$ onto vector $\mathbf{v}$ decomposes $\mathbf{u}$ into a component parallel to $\mathbf{v}$ and an orthogonal error component $\mathbf{e} = \mathbf{u} - \text{proj}_{\mathbf{v}}(\mathbf{u})$ where $\mathbf{e} \perp \mathbf{v}$:

$$\text{proj}_{\mathbf{v}}(\mathbf{u}) = \left( \frac{\mathbf{u}^T \mathbf{v}}{\Vert{}\mathbf{v}\Vert{}_2^2} \right) \mathbf{v} = \left( \frac{\mathbf{u}^T \mathbf{v}}{\mathbf{v}^T \mathbf{v}} \right) \mathbf{v}$$

#### **E. Sensitivity to Feature Scaling (Min-Max Scaling)**

When feature dimensions operate on different scale magnitudes (e.g., income in thousands vs. age in years), unscaled $L_2$ distance is dominated by high-variance attributes.

Given bounding vectors $\mathbf{x}_{\min}, \mathbf{x}_{\max} \in \mathbb{R}^d$, the Min-Max Transformation maps each feature component $x_i$ to the unit interval $[0, 1]$:

$$x'_i = \frac{x_i - x_{\min, i}}{x_{\max, i} - x_{\min, i}}$$

### 💻 2. Applied Theory: Reference Implementation in Python / NumPy

```
import numpy as np

def compute_vector_geometry_demo():
    # 1. Feature Representation (Unscaled)
    # Dimension 0: netustm (0-300 minutes)
    # Dimension 1: ppltrst (0-10 social trust)
    # Dimension 2: rlgdgr  (0-10 religiosity)
    # Dimension 3: ccnthum (1-5 climate perception)
    
    u = np.array([180.0, 7.0, 2.0, 4.0], dtype=np.float64)  # Country A
    v = np.array([210.0, 5.0, 6.0, 3.0], dtype=np.float64)  # Country B

    # 2. Dot Product
    dot_prod = np.dot(u, v)

    # 3. L2 Norms & Euclidean Distance
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)
    raw_euclidean_dist = np.linalg.norm(u - v)

    # 4. Cosine Similarity
    cosine_sim = dot_prod / (norm_u * norm_v)

    # 5. Orthogonal Projection of u onto v
    proj_u_onto_v = (dot_prod / np.dot(v, v)) * v

    # 6. Min-Max Feature Scaling
    feat_min = np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float64)
    feat_max = np.array([300.0, 10.0, 10.0, 5.0], dtype=np.float64)

    u_scaled = (u - feat_min) / (feat_max - feat_min)
    v_scaled = (v - feat_min) / (feat_max - feat_min)

    scaled_euclidean_dist = np.linalg.norm(u_scaled - v_scaled)

    # Print Results
    print(f"Raw Euclidean Distance: {raw_euclidean_dist:.4f}")
    print(f"Scaled Euclidean Distance: {scaled_euclidean_dist:.4f}")
    print(f"Dot Product: {dot_prod:.4f}")
    print(f"Cosine Similarity: {cosine_sim:.4f}")
    print(f"Projection Vector proj_v(u): {proj_u_onto_v}")

if __name__ == "__main__":
    compute_vector_geometry_demo()
```
### 📚 Official Documentation & CheatSheet References

- **NumPy Linear Algebra Routines**: [https://numpy.org/doc/stable/reference/routines.linalg.html](https://numpy.org/doc/stable/reference/routines.linalg.html)
    
- **Scikit-Learn Distance Metrics Specification**: [https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.euclidean_distances.html](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.euclidean_distances.html)
    
- **Recommended CheatSheet**: DataCamp / SciPy NumPy Linear Algebra Cheat Sheet ([Download PDF Reference](https://s3.amazonaws.com/assets.datacamp.com/blog_assets/Numpy_Python_Cheat_Sheet.pdf))

## 🎯 ASSIGNMENT STATEMENT: Exercise 2.1

### **Vector Operations, Distance Metrics & Feature Projections in Socio-Economic Microdata**

#### **Context & Goal**

In quantitative sociology and comparative political economy, country profiles are represented as continuous feature vectors derived from aggregated survey microdata (e.g., European Social Survey). Distance metrics determine cluster membership (e.g., $k$-means), while orthogonal projections isolate specific sub-dimensional influences.

You are tasked with building a modular, vectorized geometric analysis engine using `NumPy`.

#### **Tasks & Requirements**

1. **Vector Specification**:
    
    Construct two 1D NumPy arrays with `dtype=np.float64`:
    
    - $\mathbf{u} = [180.0, 7.0, 2.0, 4.0]^T$ (Country A)
        
    - $\mathbf{v} = [210.0, 5.0, 6.0, 3.0]^T$ (Country B)
        
2. **Function Implementation**:
    
    Write a Python function `compute_vector_metrics(u: np.ndarray, v: np.ndarray) -> dict` that computes and returns a dictionary containing:
    
    - `'dot_product'`: $\mathbf{u}^T \mathbf{v}$
        
    - `'l2_norm_u'`: $\Vert{}\mathbf{u}\Vert{}_2$
        
    - `'l2_norm_v'`: $\Vert{}\mathbf{v}\Vert{}_2$
        
    - `'euclidean_distance'`: $\Vert{}\mathbf{u} - \mathbf{v}\Vert{}_2$
        
    - `'cosine_similarity'`: $\frac{\mathbf{u}^T \mathbf{v}}{\Vert{}\mathbf{u}\Vert{}_2 \Vert{}\mathbf{v}\Vert{}_2}$
        
    - `'projection_u_on_v'`: $\text{proj}_{\mathbf{v}}(\mathbf{u}) = \left(\frac{\mathbf{u}^T \mathbf{v}}{\mathbf{v}^T \mathbf{v}}\right)\mathbf{v}$
        
3. **Normalization Analysis**:
    
    Given feature domain bounds:
    
    $$\mathbf{x}_{\min} = [0.0, 0.0, 0.0, 1.0]^T, \quad \mathbf{x}_{\max} = [300.0, 10.0, 10.0, 5.0]^T$$
    
    - Transform $\mathbf{u}$ and $\mathbf{v}$ into $\mathbf{u}_{\text{scaled}}$ and $\mathbf{v}_{\text{scaled}}$ using Min-Max scaling.
        
    - Compute `'scaled_euclidean_distance'`.
        
    - In a docstring/markdown comment, explain why the raw Euclidean distance ($\approx 30.33$) was heavily dominated by the `netustm` feature (dimension 0), and how Min-Max scaling balances feature weight distribution across dimensions.