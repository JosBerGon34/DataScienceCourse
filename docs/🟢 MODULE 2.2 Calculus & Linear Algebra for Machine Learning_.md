### 📘 Lesson 2.2: Partial Derivatives, Loss Functions & Gradient Optimization
  
### 📐 1. Syntactic-Algebraic Foundation
  
In Machine Learning, optimization consists of finding a set of parameters <img src="https://latex.codecogs.com/gif.latex?\mathbf{w}%20\in%20\mathbb{R}^d"/> that minimizes a scalar Loss Function <img src="https://latex.codecogs.com/gif.latex?\mathcal{L}(\mathbf{w})"/>.
  
#### A. Mean Squared Error (MSE) Loss Function
  
For a set of <img src="https://latex.codecogs.com/gif.latex?n"/> observations with target values <img src="https://latex.codecogs.com/gif.latex?y_i"/> and predictions <img src="https://latex.codecogs.com/gif.latex?\hat{y}_i%20=%20\mathbf{w}^T%20\mathbf{x}_i"/>, the Mean Squared Error is defined as:
  
<p align="center"><img src="https://latex.codecogs.com/gif.latex?\mathcal{L}(\mathbf{w})%20=%20\frac{1}{n}%20\sum_{i=1}^{n}%20\left(%20\mathbf{w}^T%20\mathbf{x}_i%20-%20y_i%20\right)^2"/></p>  
  
  
#### B. Gradient Vector (<img src="https://latex.codecogs.com/gif.latex?\nabla%20\mathcal{L}"/>)
  
The gradient of <img src="https://latex.codecogs.com/gif.latex?\mathcal{L}"/> with respect to the weight vector <img src="https://latex.codecogs.com/gif.latex?\mathbf{w}"/> is the vector of all its partial derivatives:
  
<p align="center"><img src="https://latex.codecogs.com/gif.latex?\nabla%20\mathcal{L}(\mathbf{w})%20=%20\begin{bmatrix}%20\frac{\partial%20\mathcal{L}}{\partial%20w_1}%20\\%20\frac{\partial%20\mathcal{L}}{\partial%20w_2}%20\\%20\vdots%20\\%20\frac{\partial%20\mathcal{L}}{\partial%20w_d}%20\end{bmatrix}%20=%20\frac{2}{n}%20\mathbf{X}^T%20\left(%20\mathbf{X}\mathbf{w}%20-%20\mathbf{y}%20\right)"/></p>  
  
  
where <img src="https://latex.codecogs.com/gif.latex?\mathbf{X}%20\in%20\mathbb{R}^{n%20\times%20d}"/> is the feature matrix and <img src="https://latex.codecogs.com/gif.latex?\mathbf{y}%20\in%20\mathbb{R}^n"/> is the target vector.
  
#### C. Gradient Descent Update Rule
  
To minimize <img src="https://latex.codecogs.com/gif.latex?\mathcal{L}(\mathbf{w})"/>, we iteratively update the weight vector in the direction opposite to the gradient with a learning rate <img src="https://latex.codecogs.com/gif.latex?\eta%20&gt;%200"/>:
  
<p align="center"><img src="https://latex.codecogs.com/gif.latex?\mathbf{w}^{(t+1)}%20=%20\mathbf{w}^{(t)}%20-%20\eta%20\nabla%20\mathcal{L}\left(\mathbf{w}^{(t)}\right)"/></p>  
  
### 📚 Official Documentation & Resources
  
- **NumPy Matrix Multiplication**: [numpy.matmul / @ operator](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html )
  
- **Scikit-Learn Linear Models**: [sklearn.linear_model.LinearRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html )
  
- **CheatSheet**: [Linear Algebra & Calculus for ML (DataCamp)](https://www.datacamp.com/cheat-sheet/numpy-cheat-sheet-data-analysis-in-python )
  
  
### 💻 2. Applied Context & Dataset Setup
  
Imagine we want to model how socio-economic satisfaction depends on GDP growth rate (<img src="https://latex.codecogs.com/gif.latex?x_1"/>) and Social Trust (<img src="https://latex.codecogs.com/gif.latex?x_2"/>).
  
We will build a simple linear regression model <img src="https://latex.codecogs.com/gif.latex?\hat{y}%20=%20w_1%20x_1%20+%20w_2%20x_2"/> using synthetic data based on European Social Survey (ESS) and Eurostat metrics:
  
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
  
2. **Implement Gradient Calculation**: Create a function `compute_gradient(X, y, w)` that computes and returns the analytical gradient vector <img src="https://latex.codecogs.com/gif.latex?\nabla%20\mathcal{L}(\mathbf{w})"/>.
  
3. **Gradient Descent Loop**: Write an optimization loop `fit_gradient_descent(X, y, lr=0.01, epochs=100)` that:
  
    - Initializes weights <img src="https://latex.codecogs.com/gif.latex?\mathbf{w}^{(0)}%20=%20[0.0,%200.0]"/>.
  
    - Iteratively updates weights using <img src="https://latex.codecogs.com/gif.latex?\mathbf{w}^{(t+1)}%20=%20\mathbf{w}^{(t)}%20-%20\eta%20\nabla%20\mathcal{L}(\mathbf{w}^{(t)})"/>.
  
    - Tracks and prints the loss every 20 epochs.
  
    - Returns the optimized weights <img src="https://latex.codecogs.com/gif.latex?\mathbf{w}^*"/> and the loss history.
  
  