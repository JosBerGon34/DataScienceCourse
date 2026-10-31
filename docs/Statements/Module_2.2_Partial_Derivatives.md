# 🟢 < Module 2.2 > Partial Derivatives & Gradient Optimization

## 🎯 Context & Objectives
In Machine Learning, optimization consists of finding a set of parameters $\mathbf{w} \in \mathbb{R}^d$ that minimizes a scalar Loss Function $\mathcal{L}(\mathbf{w})$. 

In this exercise, you will implement analytical gradient calculations and train a linear regression model from scratch using Gradient Descent optimization in NumPy, modeling how socio-economic satisfaction depends on economic indicators.

---

## 📑 Exercise Instructions

### 1. Mathematical & Syntactic Specification
For a set of $n$ observations with target values $y_i$ and predictions $\hat{y}_i = \mathbf{w}^T \mathbf{x}_i$, the Mean Squared Error (MSE) loss function is defined as:

$$\mathcal{L}(\mathbf{w}) = \frac{1}{n} \sum_{i=1}^{n} \left( \mathbf{w}^T \mathbf{x}_i - y_i \right)^2$$

To minimize $\mathcal{L}(\mathbf{w})$, we iteratively update the weight vector in the direction opposite to the analytical gradient $\nabla \mathcal{L}(\mathbf{w})$ using a learning rate $\eta > 0$:

$$\mathbf{w}^{(t+1)} = \mathbf{w}^{(t)} - \eta \nabla \mathcal{L}\left(\mathbf{w}^{(t)}\right)$$

---

### 2. Practical Task

Write a Python script using NumPy that performs the following tasks[cite: 20]:

1. **Implement MSE Loss**: Create a function `compute_mse(X, y, w)` that returns the scalar MSE loss for given weights $\mathbf{w}$.
2. **Implement Gradient Calculation**: Create a function `compute_gradient(X, y, w)` that computes and returns the analytical gradient vector $\nabla \mathcal{L}(\mathbf{w})$.
3. **Gradient Descent Loop**: Write an optimization loop `fit_gradient_descent(X, y, lr=0.01, epochs=100)` that:
   * Initializes weights $\mathbf{w}^{(0)} = [0.0, 0.0]$.
   * Iteratively updates weights using the update rule.
   * Tracks and prints the loss every 20 epochs.
   * Returns the optimized weights $\mathbf{w}^*$ and the loss history.

---

## 🌐 Official References & Documentation
* **NumPy Matrix Multiplication**: [NumPy matmul / @ operator Documentation](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html)
* **Scikit-Learn Linear Models**: [scikit-learn Linear Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)

---
> 💻 **Your Challenge:** Implement the gradient descent optimization engine locally, track your loss reduction across epochs, and verify your optimized weights before moving on to Module 3.1! 🚀📊

