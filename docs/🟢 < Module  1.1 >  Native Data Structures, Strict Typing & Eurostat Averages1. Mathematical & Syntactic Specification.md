Given a finite tabular dataset represented as a sequence $D = \{r_1, r_2, \dots, r_n\}$, where each record $r_i$ is a key-value mapping (dictionary):

$$r_i = \{ k_1: v_{i,1}, k_2: v_{i,2}, \dots, k_m: v_{i,m} \}$$

Let $g(r_i, k)$ be an extraction function returning the value associated with key $k$. The arithmetic mean $\bar{x}$ over a target numerical key $k_{\text{target}}$ is defined as:

$$\bar{x} = \frac{1}{\vert{}D'\vert{}} \sum_{r_i \in D'} g(r_i, k_{\text{target}})$$

where $D' = \{ r_i \in D \mid g(r_i, k_{\text{target}}) \in \mathbb{R} \}$ is the valid subset excluding null (`None`) or non-numeric values to prevent runtime type errors (`TypeError`).

#### **2. Practical Task**

1. **Synthetic Dataset Construction**: Create a list of dictionaries named `registros_desempleo` with Eurostat-based microdata:
    
    - `{"geo": "ES", "TIME_PERIOD": 2025, "age": "Y25-54", "sex": "T", "OBS_VALUE": 11.5}`
        
    - `{"geo": "DE", "TIME_PERIOD": 2025, "age": "Y25-54", "sex": "T", "OBS_VALUE": 3.8}`
        
    - `{"geo": "FR", "TIME_PERIOD": 2025, "age": "Y25-54", "sex": "T", "OBS_VALUE": 7.2}`
        
    - `{"geo": "IT", "TIME_PERIOD": 2025, "age": "Y25-54", "sex": "T", "OBS_VALUE": None}` _(Corrupted record)_
        
2. **Function Implementation with Strict Validation**: Write a function `calcular_desempleo_promedio(registros: list) -> str` that:
    
    - Iterates through `registros` and verifies whether `OBS_VALUE` is a valid number (`int` or `float`) using `isinstance()`.
        
    - Prints a console warning identifying discarded invalid/missing records (e.g., country code `"IT"`).
        
    - Returns the mean value formatted as an f-string rounded to 2 decimal places.