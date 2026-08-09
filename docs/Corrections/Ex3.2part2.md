3. Applied Data Science Level (Country Metadata Extraction)
Extract demographic/cultural metadata for European countries to enrich our core project pipeline:

Target Data Source:

Scrape tabular data from an open web source containing European nation details (e.g., Wikipedia/EU portal tables).

Extract at least 3 structural variables per country:

Country Name / ISO Code (e.g., ES, DE, FR).

Primary Official Language or Capital City.

Geographic / Cultural Region (e.g., Western Europe, Southern Europe, Nordic).

Data Cleaning & Export:

Strip reference markers (e.g., [1], [note A]) using regular expressions (re.sub(r'\[.*?\]', '', text)).

Align country names or codes to match the standard geo / CNTRY keys used in Eurostat and ESS microdata.

Export the cleaned DataFrame to data/processed/scraped_country_metadata.csv./

3.2) Data Cleaning & Export:


```python

import duckdb
from pathlib import Path
import os
import pandas as pd
import random
#PATHING SCRIPT FOR EVERY EXCERSISE - PROJECT - WORKSPACE
# 1.Literal definition of route pathings(Every user of remote repository must config this pathing in order to find the local repository of his computer)
# My case:
ROOT = Path("/home/josu/Documentos/DataScienceCourse")

# We verify the existence before continue
if not ROOT.exists():
    raise FileNotFoundError(f"❌ The route {ROOT} doesn't exist. Check it.")

# 2. Fix the workspace
os.chdir(ROOT)
print(f"✅ Worskspace enabled!: {os.getcwd()}")

# 3. Define relative pathings to work properly
DATA_TABLES = ROOT / "data" / "raw" / "Tables"

# Let's verify our table folder:
if not DATA_TABLES.exists():
    # If it fails, monitorize the issue: 
    data_dir = ROOT / "data"
    if data_dir.exists():
        print(f"⚠️ the folder 'data' exists but it doesn't have any 'Tables'. 'data' content: {os.listdir(data_dir)}")
    else:
        print(f"⚠️ The folder 'data' doesn't exist on ROOT workspace: {os.listdir(ROOT)}")
    raise FileNotFoundError(f"❌ The tables route {DATA_TABLES} is missing.")

print(f"📂 Tables route detected: {DATA_TABLES}")

```

    ✅ Worskspace enabled!: /home/josu/Documentos/DataScienceCourse
    📂 Tables route detected: /home/josu/Documentos/DataScienceCourse/data/raw/Tables



```python
#Lets filter our main global csv data block to get solo the lines that pass our boolean mask , comparing it with
#An ISO-2 european country list:
#We will make an easy filter, instead to load 2 dataframes with this mask filter
#We force on csv reading, via duckdb the cols we want and lines with exact values we need.
#Duckdb is not only a DB manipulator, it gives us some tricks on csv or other tables reading.

'''
europe_iso2 = [
    'AL', 'AD', 'AT', 'BY', 'BE', 'BA', 'BG', 'HR', 'CY', 'CZ', 
    'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IS', 'IE', 'IT', 
    'XK', 'LV', 'LI', 'LT', 'LU', 'MT', 'MD', 'MC', 'ME', 'NL', 
    'MK', 'NO', 'PL', 'PT', 'RO', 'RU', 'SM', 'RS', 'SK', 'SI', 
    'ES', 'SE', 'CH', 'UA', 'GB', 'VA'
]
'''

dfEu = duckdb.sql("""
SELECT *
FROM read_csv('data/raw/Tables/GlobalCountriesLang.csv',
    header = true,
    delim = ','
)
WHERE Código IN (
    'AL','AD','AT','BY','BE','BA','BG','HR','CY','CZ',
    'DK','EE','FI','FR','DE','GR','HU','IS','IE','IT',
    'XK','LV','LI','LT','LU','MT','MD','MC','ME','NL',
    'MK','NO','PL','PT','RO','RU','SM','RS','SK','SI',
    'ES','SE','CH','UA','GB','VA'
)
""").df()
dfEu.head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>column0</th>
      <th>Código</th>
      <th>Nombre del país</th>
      <th>Countries</th>
      <th>Official language(s)</th>
      <th>National language(s)</th>
      <th>Regional language(s)</th>
      <th>Minority language(s)</th>
      <th>Widely spoken</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>AD</td>
      <td>Andorra</td>
      <td>Andorra</td>
      <td>Catalan[6]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Spanish French Portuguese</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4</td>
      <td>AL</td>
      <td>Albania</td>
      <td>Albania</td>
      <td>Albanian</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Greek Macedonian Aromanian</td>
      <td>Italian</td>
    </tr>
    <tr>
      <th>2</th>
      <td>8</td>
      <td>AT</td>
      <td>Austria</td>
      <td>Austria</td>
      <td>German</td>
      <td>German (state language)</td>
      <td>Burgenland Croatian (parts of Burgenland) Hung...</td>
      <td>Slovene Czech Hungarian Slovak Romani Serbian</td>
      <td>English</td>
    </tr>
    <tr>
      <th>3</th>
      <td>11</td>
      <td>BA</td>
      <td>Bosnia y Herzegovina</td>
      <td>Bosnia and Herzegovina</td>
      <td>None (Bosnian, Croatian and Serbian all have d...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>14</td>
      <td>BE</td>
      <td>Bélgica</td>
      <td>Belgium</td>
      <td>Dutch French German</td>
      <td>NaN</td>
      <td>Dutch (Flanders, Brussels)[16] French (Brussel...</td>
      <td>NaN</td>
      <td>English</td>
    </tr>
  </tbody>
</table>
</div>




```python
#As we can see, line 7 is incorrect(index positon = 8), 
#the text parser failed due to some unconventional html structure, 
#we have to delete that row but first adding the item value of line 7 to Description of line 6, 
#after that we will reset the index and we will devise a logical mask to mix the dataframes 
#and have valuable and compact information about European countries.
#Load EuRegions.csv to DataCleaning and prepare its data for merge with the dfEu dataframe.
dfRegions = pd.read_csv(DATA_TABLES / 'EuRegions.csv', index_col=False)
# Add row 8 item into row 7 description
dfRegions.loc[6, "Description"] = dfRegions.loc[7, "Item"]
# Delete row 8
dfRegions = dfRegions.drop(index=7).reset_index(drop=True)
# Reset index
dfRegions = dfRegions.reset_index(drop=True)
#Lets introduce manually the countries of mediterranean, macaronesia, and black sea region.
#The parser is not perfect.
macaronesia= 'Portugal and Spain'
black_sea= 'Bulgaria, Georgia, Romania, Russia, Turkey and Ukraine'
mediterranean = 'Albania, Bosnia and Herzegovina, Croatia, Cyprus, France, Greece, Italy, Malta, Monaco, Montenegro, Slovenia, Spain, Vatican City'
dfRegions.loc[18, "Description"] = macaronesia,
dfRegions.loc[19, "Description"] = mediterranean,
dfRegions.loc[20, "Description"] = black_sea,
dfRegions.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Unnamed: 0</th>
      <th>Section</th>
      <th>Category</th>
      <th>Item</th>
      <th>Description</th>
      <th>Parent_item</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>Geographical</td>
      <td>Peninsulas</td>
      <td>Apennine Peninsula (Italian Peninsula)</td>
      <td>Located in the south of Europe, the Apennine P...</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>Geographical</td>
      <td>Peninsulas</td>
      <td>Balkan Peninsula</td>
      <td>The Balkan Peninsula is located in Southeaster...</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>Geographical</td>
      <td>Peninsulas</td>
      <td>Fennoscandian Peninsula</td>
      <td>Located in the north of Europe, including Finl...</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>Geographical</td>
      <td>Peninsulas</td>
      <td>Iberian Peninsula</td>
      <td>Located in Southwestern Europe, this peninsula...</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>Geographical</td>
      <td>Peninsulas</td>
      <td>Jutland Peninsula</td>
      <td>Jutland of Denmark (main part of the country e...</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>5</th>
      <td>5</td>
      <td>Geographical</td>
      <td>Peninsulas</td>
      <td>Scandinavian Peninsula</td>
      <td>Located in the north of Europe, including Norw...</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>6</th>
      <td>6</td>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Atlantic Europe</td>
      <td>United Kingdom , Ireland , Iceland , Belgium ,...</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>7</th>
      <td>8</td>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Alpine countries</td>
      <td>Austria , Switzerland , Liechtenstein , Sloven...</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>8</th>
      <td>9</td>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Balkans region</td>
      <td>In its broadest sense, encompasses Albania , B...</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>9</th>
      <td>10</td>
      <td>Geographical</td>
      <td>Regional</td>
      <td>Baltic Rim region</td>
      <td>Denmark , Estonia , Finland , Germany , Latvia...</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Lets create  a column called 'Regions' in our dfEu dataframe for organize the geographical information (Peninsula info+ Region info)
#The objective is to summ in one columm the peninsula and regional item information for every Europe Country

dfEu['Regions'] = None
```


```python
#Logic implementation:
#Si la columna  dfRegions[['Description']] tiene en su string.values de la columna dfEu[['Countries']]
#Se añade el valor de value de dfRegions[['Item']] al slot de columna dfEu[['Regions']]
#Una fila de un pais en dfEu puede tener mas de una string de Regiones en df[['Regions']].
#El formato de suma de strings debe ser 'Value string1' & 'Value string2'
import re
import pandas as pd

def find_regions_for_country(country, df_regions, desc_col="Description", item_col="Item"):
    """
    Busca en df_regions[desc_col] todas las filas cuya descripción menciona
    `country` (como palabra completa, insensible a mayúsculas), y devuelve
    los valores de df_regions[item_col] concatenados como:
        "'Region1' & 'Region2'"
    Si no hay coincidencias, devuelve None (queda como NaN en el dataframe).
    """
    if not isinstance(country, str) or not country.strip():
        return None

    pattern = re.compile(r"\b" + re.escape(country.strip()) + r"\b", flags=re.IGNORECASE)

    mask = df_regions[desc_col].astype(str).str.contains(pattern, na=False)
    matched_items = list(dict.fromkeys(df_regions.loc[mask, item_col].dropna()))

    if not matched_items:
        return None

    return " & ".join(f"'{item}'" for item in matched_items)

```


```python
dfEu["Regions"] = dfEu["Countries"].apply(
    lambda c: find_regions_for_country(c, dfRegions)
)
```


```python
dfEu.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>column0</th>
      <th>Código</th>
      <th>Nombre del país</th>
      <th>Countries</th>
      <th>Official language(s)</th>
      <th>National language(s)</th>
      <th>Regional language(s)</th>
      <th>Minority language(s)</th>
      <th>Widely spoken</th>
      <th>Regions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>AD</td>
      <td>Andorra</td>
      <td>Andorra</td>
      <td>Catalan[6]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Spanish French Portuguese</td>
      <td>NaN</td>
      <td>'Iberian Peninsula'</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4</td>
      <td>AL</td>
      <td>Albania</td>
      <td>Albania</td>
      <td>Albanian</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Greek Macedonian Aromanian</td>
      <td>Italian</td>
      <td>'Balkans region' &amp; 'Dinaric Alps' &amp; 'Mediterra...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>8</td>
      <td>AT</td>
      <td>Austria</td>
      <td>Austria</td>
      <td>German</td>
      <td>German (state language)</td>
      <td>Burgenland Croatian (parts of Burgenland) Hung...</td>
      <td>Slovene Czech Hungarian Slovak Romani Serbian</td>
      <td>English</td>
      <td>'Alpine countries'</td>
    </tr>
    <tr>
      <th>3</th>
      <td>11</td>
      <td>BA</td>
      <td>Bosnia y Herzegovina</td>
      <td>Bosnia and Herzegovina</td>
      <td>None (Bosnian, Croatian and Serbian all have d...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>'Dinaric Alps' &amp; 'Mediterranean countries'</td>
    </tr>
    <tr>
      <th>4</th>
      <td>14</td>
      <td>BE</td>
      <td>Bélgica</td>
      <td>Belgium</td>
      <td>Dutch French German</td>
      <td>NaN</td>
      <td>Dutch (Flanders, Brussels)[16] French (Brussel...</td>
      <td>NaN</td>
      <td>English</td>
      <td>'Atlantic Europe' &amp; 'Low Countries'</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Now we checked all our Regional information is stored we can end the
#Exercise and store the result as a csv for working with it in next
#Projects.
del dfEu['column0']
```


```python
dfEu.to_csv(DATA_TABLES / 'EuInfo.csv', index=False)
```
