# 🖨️ Print Structure — Python

Manual rápido para construir salidas de consola claras y combinar
texto, variables, separadores y formatos mediante `print()`.

---

## 1. Print básico


nombre = "España"
valor = 11.53

print(nombre, valor)

#Salida:

España 11.53
## ----------------

## 2. Separar variables con sep

#sep determina qué se introduce entre los elementos enviados a print().

pais = "ES"
valor = 11.53

print(pais, valor, sep=" | ")

#Salida:

ES | 11.53

## ---------------

## 3. Saltos de línea con \n


pais = "España"
valor = 11.53

print("País:", pais, "\nDesempleo:", valor)

#Salida

País: España
Desempleo: 11.53

## ------------------

## 4. F-strings.

#La forma más cómoda de mezclar texto y variables:

pais = "España"
valor = 11.53456

print(f"País: {pais} | Desempleo: {valor}")

#Salida:

País: España
Desempleo: 11.53%
Año: 2025

## -----------

## 5. Ejemplo Superior:

#Lets check all de dataframe info, and its content:
dfESPDEf1.info()

print(
    f"\n| DF content:\n{dfESPDEf1.head()}"
    f"\n\n| Var Description:\n{dfESPDEf1.describe()}"
)
#Salida
<class 'pandas.DataFrame'>
RangeIndex: 4264 entries, 1594 to 5857
Data columns (total 5 columns):
 #   Column   Non-Null Count  Dtype  
---  ------   --------------  -----  
 0   netustm  4264 non-null   float64
 1   ppltrst  4264 non-null   float64
 2   rlgdgr   4264 non-null   float64
 3   ccnthum  4264 non-null   float64
 4   cntry    4264 non-null   str    
dtypes: float64(4), str(1)
memory usage: 166.7 KB

| DF content:
       netustm   ppltrst    rlgdgr   ccnthum cntry
1594  0.060756  0.000000  0.113636  0.022989    DE
1595  0.020252  0.090909  0.022727  0.034483    DE
1596  0.020252  0.056818  0.113636  0.022989    DE
1597  0.033753  0.056818  0.034091  0.011494    DE
1598  0.074257  0.090909  0.000000  0.034483    DE

| Var Description:
           netustm      ppltrst       rlgdgr      ccnthum
count  4264.000000  4264.000000  4264.000000  4264.000000
mean      0.148111     0.060360     0.047696     0.041726
std       0.270897     0.037590     0.056463     0.104970
min       0.000000     0.000000     0.000000     0.000000
25%       0.013501     0.045455     0.011364     0.022989
50%       0.027003     0.056818     0.045455     0.034483
75%       0.067507     0.079545     0.079545     0.034483
max       1.000000     1.000000     1.000000     1.000000

## --------