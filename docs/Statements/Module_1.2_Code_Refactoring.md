# 🟢 < Module  1.2 > Code Refactoring, Pipeline Optimization & Primality Testing1. Context & Problem Statement

## 🎯 Context & Objectives
In professional Data Science and software engineering, writing functional code is only the first step. Code must be clean, modular, highly performant, and compliant with PEP 8 standards. 

In this exercise, you will refactor legacy procedural scripts into modular Python functions, optimize pipeline execution speeds using generators and efficient looping structures, and implement an optimized primality testing algorithm to filter mathematical properties in numerical datasets.

---

## 📑 Exercise Instructions

### 1. Mathematical & Syntactic Specification
Let $N$ be a set of integers. A primality test function $isPrime(n)$ determines whether an integer $n > 1$ is a prime number by checking divisibility up to $\lfloor\sqrt{n}\rfloor$:

$$\forall d \in \{2, 3, \dots, \lfloor\sqrt{n}\rfloor\}, \quad n \pmod{d} \neq 0$$

To optimize pipeline performance for large data streams, memory-efficient generators (`yield`) should be preferred over static list allocations when processing sequences of numbers.

---

### 2. Practical Task

1. **Refactoring Legacy Code**: Take a procedural script containing repetitive loops and global variables, and refactor it into pure, modular functions with type hints (`int`, `float`, `list`) and docstrings.
2. **Optimized Primality Function**: Write an efficient Python function `es_primo(n: int) -> bool` that implements the square-root trial division check.
3. **Pipeline Stream Processing**: Create a generator function `generador_primos(n: int)` that yields prime numbers up to $n$, ensuring minimal memory footprint.

---

## 🌐 Official References & Documentation
* **Python PEP 8 Style Guide**: [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
* **Python Efficiency & Generators**: [Python Iterators & Generators Guide](https://docs.python.org/3/tutorial/classes.html#iterators)

---
> 💻 **Your Challenge:** Refactor your local script, implement strict type checking, and test your optimization before moving on to Module 2.1! 🚀📊

