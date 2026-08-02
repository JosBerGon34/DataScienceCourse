### 📘 Lesson 2.2: Partial Derivatives, Loss Functions & Gradient Optimization

### 📐 1. Syntactic-Algebraic Foundation

In Machine Learning, optimization consists of finding a set of parameters $\mathbf{w} \in \mathbb{R}^d$ that minimizes a scalar Loss Function $\mathcal{L}(\mathbf{w})$.

#### A. Mean Squared Error (MSE) Loss Function

For a set of $n$ observations with target values $y_i$ and predictions $\hat{y}_i = \mathbf{w}^T \mathbf{x}_i$, the Mean Squared Error is defined as:

$$\mathcal{L}(\mathbf{w}) = \frac{1}{n} \sum_{i=1}^{n} \left( \mathbf{w}^T \mathbf{x}_i - y_i \right)^2$$

#### B. Gradient Vector ($\nabla \mathcal{L}$)

The gradient of $\mathcal{L}$ with respect to the weight vector $\mathbf{w}$ is the vector of all its partial derivatives:

$$\nabla \mathcal{L}(\mathbf{w}) = \begin{bmatrix} \frac{\partial \mathcal{L}}{\partial w_1} \\ \frac{\partial \mathcal{L}}{\partial w_2} \\ \vdots \\ \frac{\partial \mathcal{L}}{\partial w_d} \end{bmatrix} = \frac{2}{n} \mathbf{X}^T \left( \mathbf{X}\mathbf{w} - \mathbf{y} \right)$$

where $\mathbf{X} \in \mathbb{R}^{n \times d}$ is the feature matrix and $\mathbf{y} \in \mathbb{R}^n$ is the target vector.

#### C. Gradient Descent Update Rule

To minimize $\mathcal{L}(\mathbf{w})$, we iteratively update the weight vector in the direction opposite to the gradient with a learning rate $\eta > 0$:

$$\mathbf{w}^{(t+1)} = \mathbf{w}^{(t)} - \eta \nabla \mathcal{L}\left(\mathbf{w}^{(t)}\right)$$
### 📚 Official Documentation & Resources

- **NumPy Matrix Multiplication**: [numpy.matmul / @ operator](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html)
    
- **Scikit-Learn Linear Models**: [sklearn.linear_model.LinearRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)
    
- **CheatSheet**: [Linear Algebra & Calculus for ML (DataCamp)](https://www.datacamp.com/cheat-sheet/numpy-cheat-sheet-data-analysis-in-python)


### 💻 2. Applied Context & Dataset Setup

Imagine we want to model how socio-economic satisfaction depends on GDP growth rate ($x_1$) and Social Trust ($x_2$).

We will build a simple linear regression model $\hat{y} = w_1 x_1 + w_2 x_2$ using synthetic data based on European Social Survey (ESS) and Eurostat metrics:

```
import numpy as np

# Synthetic Dataset: 4 Countries [x1: GDP Growth %, x2: Social Trust (0-10)]
X = np.array([
    [1.5, 7.0],  # Country A
    [3.0, 5.0],  # Country B
    [0.5, 8.5],  # Country C
    [2.0, 4.0]   # Country D
], dtype=np.float64)

# Target: Overall Life Satisfaction (0-10 scale)
y = np.array([7.2, 6.1, 8.0, 5.0], dtype=np.float64)
```

### 💻 3. Your Challenge: Exercise 2.2

Write a Python script using NumPy that performs the following tasks:

1. **Implement MSE Loss**: Create a function `compute_mse(X, y, w)` that returns the scalar MSE loss for given weights `w`.
    
2. **Implement Gradient Calculation**: Create a function `compute_gradient(X, y, w)` that computes and returns the analytical gradient vector $\nabla \mathcal{L}(\mathbf{w})$.
    
3. **Gradient Descent Loop**: Write an optimization loop `fit_gradient_descent(X, y, lr=0.01, epochs=100)` that:
    
    - Initializes weights $\mathbf{w}^{(0)} = [0.0, 0.0]$.
        
    - Iteratively updates weights using $\mathbf{w}^{(t+1)} = \mathbf{w}^{(t)} - \eta \nabla \mathcal{L}(\mathbf{w}^{(t)})$.
        
    - Tracks and prints the loss every 20 epochs.
        
    - Returns the optimized weights $\mathbf{w}^*$ and the loss history.

