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
import numpy as np
import pandas as pd
```


```python
#Lets load the original list, then trasnform to array.




Numberlist: list[int]=[12, 15, 7, 22, 19, 30, 11, 4, 8, 17]

```


```python
#Lets check what we got.


print(f"List: {Numberlist} | Estructure Type: {type(Numberlist)} | 1st element type: {type(Numberlist[0])}")
```

    List: [12, 15, 7, 22, 19, 30, 11, 4, 8, 17] | Estructure Type: <class 'list'> | 1st element type: <class 'int'>



```python
#This way provide us to apply a logic or boolean filter(mask) to the whole block of data,
#instead to making a iteration or loop, like for or while. Lets make 2 functions, one for return a variable related
#to primary numbers detection in to the array.
#The next function pipelines with basic inputs.

def vectorized_primality(n: int) -> bool:
    f"""
    
    Verify optimized primality  0(sqrt(n))
    We use a mask to operate in the whole numbers of the variable.
    """
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    #We check the impairty until it arrives clean to the squared number
    limit = int(np.sqrt(n)) + 1
    return not np.any(n % np.arange(3, limit, 2) == 0)

def number_filtering(numbers: list[int]) -> tuple[int, bool]:
    """
    Vectorized pipeline
    1. Numpy array conversion.
    2. Boolean(logic) filter (masking).
    3. Vectorized sum.
    4. Primality verification.
    """
    # 1. Data vectorize
    arr = np.array(numbers)
    
    # 2. Vector filtering
    # Boolean mask.
    pair_mask = arr % 2 == 0
    
    # 3. Vectorized summ in all data through the mask
    total_sum = np.sum(arr[pair_mask])
    
    # 4. Primality check
    prime_result = vectorized_primality(total_sum)
    
    return total_sum, prime_result



```


```python
# --- Runtime ---
#lets check the vectorized functions applying via inputs and declarations out of the function codeblock.
sum, prime = number_filtering(Numberlist)
print(f"Result: {sum}, ¿Prime? {'yes' if prime else 'No'}")  

```

    Result: 76, ¿Prime? No

