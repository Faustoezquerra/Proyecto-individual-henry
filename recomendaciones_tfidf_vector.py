import pandas as pd
from fastapi.responses import HTMLResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI
import os



import os
os.system("cls")

lote = 1000
titulo="Toy Story"

df_total = pd.read_csv('final2.csv',low_memory=True)

ganadores=pd.DataFrame()
# Extraer el contenido (filas) del título del DataFrame completo
df_total['content'] =\
df_total['title'].fillna('') + \
df_total['genres'].fillna('') + df_total['genres'].fillna('') + df_total['genres'].fillna('') + df_total['genres'].fillna('') + \
df_total['belongs_to_collection'].fillna('') + df_total['belongs_to_collection'].fillna('') + \
df_total['belongs_to_collection'].fillna('') + df_total['belongs_to_collection'].fillna('') + df_total['belongs_to_collection'].fillna('') + \
df_total['production_companies'] + df_total['production_companies'] + \
str(df_total['vote_average']) 

columnas_a_mantener = ['title', 'content']
# Obtener la lista de las columnas que deseas borrar
columnas_a_borrar = [col for col in df_total.columns if col not in columnas_a_mantener]
# Borrar las columnas no deseadas del DataFrame
df_total = df_total.drop(columns=columnas_a_borrar)
fila_titulo = df_total[df_total['title'] == titulo]

tamanio_del_lote=lote
indice_inicial = 0  #al principio sera siempre cero, luego sera el indice proximo al indice final recien utilizado
indice_final = tamanio_del_lote #al principio es el tamaño del lote, luego ira subiendo
tamanio_total_del_csv=len(df_total)
datos_restantes_a_evaluar=len(df_total)
ganadores_de_cada_competencia=5
        
while datos_restantes_a_evaluar >= tamanio_del_lote:    
        df_a_competir = df_total.iloc[indice_inicial:indice_final]
        df_a_competir = pd.concat([df_a_competir,ganadores],ignore_index=True)
        
        if titulo not in df_a_competir['title'].values:
                df_a_competir = pd.concat([df_a_competir, fila_titulo], ignore_index=True)


        # Crear el vectorizador de conteo
        vectorizer = TfidfVectorizer(stop_words='english')
        # Obtener la matriz de conteo
        tf_matrix = vectorizer.fit_transform(df_a_competir['content'])
        # Encontrar el índice del título ingresado en el DataFrame
        idx = df_a_competir.index[df_a_competir['title'] == titulo].tolist()[0]
        # Calcular las similitudes coseno con la matriz de conteo
        cosine_similarities = cosine_similarity(tf_matrix)
        # Obtener los índices de las películas recomendadas (excluyendo el título ingresado)
        recommendation_indices = cosine_similarities[idx].argsort()[::-1][1:]
        # Agregar las recomendaciones al DataFrame para las recomendaciones totales
        ganadores = df_a_competir.iloc[recommendation_indices].head(ganadores_de_cada_competencia)

        datos_restantes_a_evaluar=datos_restantes_a_evaluar-tamanio_del_lote
        indice_inicial=indice_final
        indice_final=indice_final+tamanio_del_lote
else:
        
        indice_inicial=indice_final
        indice_final=tamanio_total_del_csv
        df_a_competir = df_total.iloc[indice_inicial:indice_final]
        df_a_competir = pd.concat([df_a_competir,ganadores],ignore_index=True)
        
        if titulo not in df_a_competir['title'].values:
                df_a_competir = pd.concat([df_a_competir, fila_titulo], ignore_index=True)


        # Crear el vectorizador de conteo
        vectorizer = TfidfVectorizer(stop_words='english')
        # Obtener la matriz de conteo
        tf_matrix = vectorizer.fit_transform(df_a_competir['content'])
        # Encontrar el índice del título ingresado en el DataFrame
        idx = df_a_competir.index[df_a_competir['title'] == titulo].tolist()[0]
        # Calcular las similitudes coseno con la matriz de conteo
        cosine_similarities = cosine_similarity(tf_matrix)
        # Obtener los índices de las películas recomendadas (excluyendo el título ingresado)
        recommendation_indices = cosine_similarities[idx].argsort()[::-1][1:]
        # Agregar las recomendaciones al DataFrame para las recomendaciones totales
        ganadores = df_a_competir.iloc[recommendation_indices].head(ganadores_de_cada_competencia)



pd.options.display.max_columns = None
pd.options.display.expand_frame_repr = False
pd.set_option('display.max_colwidth', None)


pd.options.display.max_columns = None
pd.options.display.expand_frame_repr = False
pd.set_option('display.max_colwidth', None)

# print los ganadores de recomendacion
titles = ganadores['title'].tolist()
df_filtered = df_total[df_total['title'].isin(titles)]
df_filtered['title']

print(titles)



