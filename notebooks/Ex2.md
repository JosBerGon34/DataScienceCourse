You are reviewing a legacy script designed to process an integer list, filter specific elements, compute their total sum, and check if the result is a prime number:


```
# Inefficient original script
numeros = [12, 15, 7, 22, 19, 30, 11, 4, 8, 17]

# 1. Filter even numbers
pares = []
for n in numeros:
    if n % 2 == 0:
        pares.append(n)

# 2. Manual summation
suma_total = 0
for p in pares:
    suma_total = suma_total + p

# 3. Inefficient primality test
def es_primo(numero):
    if numero < 2:
        return False
    for i in range(2, numero):
        if numero % i == 0:
            return False
    return True

print(f"Resultado: {suma_total}, ¿Primo? {'Sí' if es_primo(suma_total) else 'No'}")
```


#### **2. Refactoring Directives**

1. **Eliminate Redundant Iterations**: Avoid multiple manual `for` loops by unifying filtering and summation into built-in Python expressions (e.g., generator expressions with `sum()`).
    
2. **Mathematical Primality Optimization**: Reduce time complexity of the prime test from $O(N)$ to $O(\sqrt{N})$ by evaluating odd factors only up to $\lfloor\sqrt{N}\rfloor$.
    
3. **Software Design & Modularity**: Encapsulate the refactored pipeline into modular, type-hinted functions with clean docstrings.


```python

```
