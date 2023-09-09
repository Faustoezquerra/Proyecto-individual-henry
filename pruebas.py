import pandas as pd

import os

os.system("cls")

df = pd.read_csv('final2.csv')

column_name='revenue'

"""
if column_name in df.columns:
    if pd.api.types.is_numeric_dtype(df[column_name]):
        sorted_values = df[column_name].dropna().sort_values().unique()
    else:
        sorted_values = sorted(df[column_name].dropna().unique())
    
    counts = []

    for value in sorted_values:
        count = df[column_name].value_counts()[value]
        counts.append((value, count))
    

  
    for value, count in counts:
        print(f"{value} - Aparece {count} veces")

else:
    print("Columna no encontrada")"""
    

if column_name in df.columns:
    column_values = df[column_name].dropna()

    if pd.api.types.is_numeric_dtype(column_values):
        sorted_values = column_values.sort_values().unique()
    else:
        sorted_values = sorted(column_values.unique())
    
    value_counts = column_values.value_counts()

    for value in sorted_values:
        count = value_counts.get(value, 0)
        print(f"{value} - Aparece {count} veces")

else:
    print("Columna no encontrada")
