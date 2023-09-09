import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from fastapi import FastAPI
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse, Response
from fastapi import Form, Request, Depends, HTTPException

from starlette.responses import HTMLResponse

"""import os
os.system("cls")"""



# uvicorn main:app --reload

app = FastAPI()


#---------------------------------------------------------------------------------------------------------------------------
df = pd.read_csv('final2.csv', low_memory=True)
#-----------------------------------------------------------------------------------------------------------------

# Variable para almacenar la primera parte del endpoint
selected_option = None

@app.post("/select_first_part")
async def select_first_part(opcion: str = Form(...)):
    global selected_option
    selected_option = opcion
    return {}

  
    
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
 inicio="""
<!DOCTYPE html>
                <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Título de tu página</title>
                            <style>
                                /* Establecer el tamaño de la fuente en todo el documento */
                                body {
                                    font-size: 16px; /* Ajusta este valor según lo que necesites */
                                    }
                            </style>
                        </head>
                <body>
                            <h2 style="color: red;">BIENVENIDOS! A LA API DE CONSULTA</h2>
                            
                            <script>
                                function redirectToEndpoint() {
                                    var antePrimeraParte = "https://proyecto-individual-henry.onrender.com"
                                    var primeraParte = document.getElementById("opcion").value;
                                    var segundaParte = document.getElementById("segundaParte").value;

                                    if (segundaParte.trim() !== "") {
                                        if (primeraParte !== "/data/") {
                                            // Convertir a títulos
                                            var words = segundaParte.split(' ');
                                            for (var i = 0; i < words.length; i++) {
                                                words[i] = words[i].charAt(0) + words[i].slice(1);
                                            }
                                            segundaParte = words.join(' ');
                                                                       }

                                    var endpoint = antePrimeraParte + primeraParte + segundaParte;
                                    window.location.href = endpoint;
                                    }
                                }
                            </script>



                            
                            <h3>Redirigir a un Endpoint</h3>
                            <form method="post" action="/select-first-part">
                                <label for="opciones">Selecciona una opción de la primera parte:</label>
                                <select name="opcion" id="opcion">
                
                                    <option value="/peliculas_idioma/">/peliculas_idioma/</option>
                                    <option value="/peliculas_duracion/">/peliculas_duracion/</option>
                                    <option value="/franquicia/">/franquicia/</option>
                                    <option value="/peliculas_pais/">/peliculas_pais/</option>
                                    <option value="/productora_existosas/">/productora_existosas/</option>
                                    <option value="/data/">/data/</option>
                                    <option value="/get_director/">/get_director/</option>
                                    <option value="/actor_principal/">/actor_principal/</option>
                                    <option value="/recomendacion/">/recomendacion/</option>

                                </select>
                            </form>
                            <br>
                            <form method="post" action="/redirigir">
                                <label for="segundaParte">Escribe la segunda parte del endpoint:</label>
                                <input type="text" name="segundaParte" id="segundaParte">
                                <button type="button" onclick="redirectToEndpoint()">Ir al Endpoint</button>
                            </form><br>
                                                

                            1-Para consultar cantidad de peliculas por idioma, ejemplo /en (ingles) escriba el endpoint /peliculas_idioma/idioma<br><br>\
                            2-Para traer toda la data de la columna elegida del dataframe, escriba /data/column_name<br><br>\
                            3-Para saber duracion, y año de lanzamiento de una pelicula, escriba el endpoint /peliculas_duracion/pelicula<br><br>\
                            4-Si ingresa una franquicia, retorna la cantidad de peliculas que contiene la franquicia, ganancia total y ganancia promedio, escriba /franquicia/franquicia<br><br>\
                            5-Si ingresas un pais en ingles, retorna la cantidad de peliculas producidas en el mismo, escribis /peliculas_pais/pais<br><br>\
                            6-Si ingresas la productora, muestra ganancia(revenue) total y la cantidad de peliculas que realizo, escribis /productoras_exitosas/productora<br><br>\
                            7-Si ingresa el nombre de un director que se encuentre dentro de un dataset, muestra el éxito del mismo medido a través del retorno que obtuvo.<br><br>\
                            Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual de la pelicula, costo y ganancia de la misma, se escribe /get_director/nombre_director<br><br>\
                            8-Ingresas a este link y puedes ver el idioma que representa cada abreviatura de idioma para utilizar en la funcion 1 <br><br>
                            9-Si ingresas un nombre de una pelicula respetando mayusculas y el titulo en ingles, te recomienda peliculas, escribes el titulo de la pelicula asi: /recomendacion/Titulo<br>
                            
                            <h3 style="color: red;">EJEMPLOS:</h3>
                            
                            "<strong>/data" devuelve una columna con todos los valores únicos de esa columna elegida sea de numeros enteros, palabras, o floats</strong><br>
                            <strong>y los devuelve de forma alfabética, o bien de menor a mayor, vamos a dar tres ejemplos con estos casos:</strong><br><br>
                            1-A- <a href="https://proyecto-individual-henry.onrender.com/data/director">https://proyecto-individual-henry.onrender.com/data/director</a>      (PALABRAS)<br>\
                            1-B- <a href="https://proyecto-individual-henry.onrender.com/data/revenue">https://proyecto-individual-henry.onrender.com/data/revenue</a>      (NUMEROS ENTEROS)<br>\
                            1-C- <a href="https://proyecto-individual-henry.onrender.com/data/vote_average">https://proyecto-individual-henry.onrender.com/data/vote_average</a>  (NUMEROS CON DECIMALES,FLOATS)<br><br>\
                            2-<a href="https://proyecto-individual-henry.onrender.com/peliculas_idioma/en">https://proyecto-individual-henry.onrender.com/peliculas_idioma/en</a><br><br>\
                            3-<a href="https://proyecto-individual-henry.onrender.com/peliculas_duracion/Toy Story">https://proyecto-individual-henry.onrender.com/peliculas_duracion/Toy Story</a><br><br>\
                            4-<a href="https://proyecto-individual-henry.onrender.com/franquicia/Toy Story Collection">https://proyecto-individual-henry.onrender.com/franquicia/Toy Story Collection</a><br><br>\
                            5-<a href="https://proyecto-individual-henry.onrender.com/peliculas_pais/France">https://proyecto-individual-henry.onrender.com/peliculas_pais/France</a><br><br>\
                            6-<a href="https://proyecto-individual-henry.onrender.com/productoras_exitosas/Pixar Animation Studios">https://proyecto-individual-henry.onrender.com/productoras_exitosas/Pixar Animation Studios</a><br><br>\
                            7-<a href="https://proyecto-individual-henry.onrender.com/get_director/James Cameron">https://proyecto-individual-henry.onrender.com/get_director/James Cameron</a><br><br>\
                            8-<a href="https://proyecto-individual-henry.onrender.com/idioma_abreviaturas/">https://proyecto-individual-henry.onrender.com/idioma_abreviaturas</a><br><br>\
                            9-<a href="https://proyecto-individual-henry.onrender.com/peliculas_actor/Robin Williams">https://proyecto-individual-henry.onrender.com/peliculas_actor/Robin Williams</a><br><br>\
                            10-<a href="https://proyecto-individual-henry.onrender.com/recomendacion/Toy Story">https://proyecto-individual-henry.onrender.com/recomendacion/Toy Story</a><br>\
                            <strong>este ultimo tardara aproximadamente 1 minuto exacto ya que utiliza mucha memoria y divide los procesos, en varios procesos, por los pocos recursos de RAM que disponemos en RENDER, a tener paciencia!"</strong>
                            
                        
                            
                </body>
            </html>
"""
 return HTMLResponse(content=inicio)

#----------------------------------------------------------------------------------------------------------------


@app.get('/peliculas_idioma/{idioma}')
def peliculas_idioma(idioma:str):
    
    global df
    '''Ingresas el idioma abreviado, puedes consultar la abreviatura en nuestro link debajo, retornando la cantidad de peliculas producidas en el mismo'''
    
    if any(idioma.lower() == idiom.lower() for idiom in df['original_language'].str.lower().values):
        
        recuento = df['original_language'].value_counts().get(idioma, 0)
        return {"mensaje": f"Hay {int(recuento)} peliculas en {idioma}"}
    else:
        return {"mensaje":"No existe pelicula en esa abreviatura del idioma, o no existe esa abreviatura del idioma"}



@app.get('/idioma_abreviaturas/')
def abreviaturas_paises():
    df_abreviaturas = pd.read_csv('abreviaturas_de_paises.csv', dtype=str)

    # Convertir el DataFrame a una cadena de texto con formato
    texto = '\n'.join([f"{row[0]:5} ---> {row[1]:>20}" for row in df_abreviaturas.values])

    # Agregar estilos CSS para el espaciado lateral
    estilos_css = """
    <style>
        pre {
            margin-left: 100px;
            text-align: left;
            margin-right: 100px;
        }
    </style>
    """

    # Combinar estilos CSS y el texto formateado
    html_content = f'<html><head>{estilos_css}</head><body><pre>{texto}</pre></body></html>'
    return HTMLResponse(content=html_content)


@app.get('/peliculas_duracion/{pelicula}')
def peliculas_duracion(pelicula:str):
       
    global df
       

    if any(pelicula.lower() == peli.lower() for peli in df['title'].str.lower().values):
        
        duracion = df.loc[df['title'] == pelicula, 'runtime'].values[0]
        anio = df.loc[df['title'] == pelicula, 'release_year'].values[0]
        return {"mensaje": f"La Pelicula {pelicula} tiene una duracion de {duracion} minutos, y fue lanzada en el anio: {anio}"}
    else:
        return {"mensaje":"No existe esa pelicula"}



@app.get('/franquicia/{franquicia}')
def franquicia(franquicia:str):
    
    global df

    if any(franquicia.lower() == franq.lower() for franq in df['belongs_to_collection'].str.lower().values):
        peliculas = df['belongs_to_collection'].value_counts()
        '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio'''
        # Crear una máscara booleana para el valor específico
        mask = df['belongs_to_collection'] == franquicia
        # Aplicar la máscara al DataFrame para ver sólo las filas con ese valor específico
        df_especifico = df[mask]

        ganancia=df_especifico['revenue'].sum()
        promedio=df_especifico['revenue'].mean()
        ganancia_formateada = "{:,}".format(int(ganancia)).replace(",", "x").replace(".", ",").replace("x", ".")
        promedio_formateado = "{:,}".format(int(promedio)).replace(",", "x").replace(".", ",").replace("x", ".")

        return {'mensaje':f'la franquicia: {franquicia}, posee {len(df_especifico)} peliculas, tine una ganancia_total: {ganancia_formateada}$ y una ganancia promedio de: {promedio_formateado}$'}
    else:
        return {"mensaje":"No existe esa franquicia"}




@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais:str):
    
    global df
    
    '''Ingresas el pais, retornando la cantidad de peliculas producidas en el mismo'''

    if any(pais.lower() == pais1.lower() for pais1 in df['production_countries'].str.lower().values):
        mask = df['production_countries'] == pais
        # Aplicar la máscara al DataFrame para ver sólo las filas con ese valor específico
        df_especifico2 = df[mask]
        recuento2 = df['production_countries'].value_counts().get(pais)
        return {'pais':f'{pais}, cantidad:{recuento2}'}
    else:
        return {"ese pais no tiene producciones"}



@app.get('/productoras_exitosas/{productora}')
def productoras_exitosas(productora:str):
    
    global df
    
    '''Ingresas la productora, entregandote el revunue total y la cantidad de peliculas que realizo '''

    if any(productora.lower() == product.lower() for product in df['production_companies'].str.lower().values):
        mask = df['production_companies'].str.lower() == productora.lower()
        # Aplicar la máscara al DataFrame para ver sólo las filas con ese valor específico
        df_especifico3 = df[mask]
        ganancia=df_especifico3['revenue'].sum()
        formated_num = "{:,}".format(int(ganancia)).replace(",", "x").replace(".", ",").replace("x", ".")
        recuento3 = df['production_companies'].value_counts().get(productora)
        #value counts cuenta la cantidad de veces que se repite una productora en la columna production_companies
        #eso significa que por cada vez que se repite es una pelicula diferente por cada productora
        #y .get(productora) suma y retorna la cantidad de veces que se repitio la productora con la variable productora
        #que es la productora que ingrese a la funcion principal, dando entonces la cantidad de peliculas que produjo 
        #que coincide con las filas sumadas donde aparece la productora indicada en la variable ingresada "productora a la funcion"

        return {f'La productora: {productora} produjo: {recuento3} peliculas, y ha tenido un revenue total de: {formated_num} $'}
    else:
        return {"no existe esa productora"}


#------------------------------------------------------------------------------------------------

def custom_sort(data):
    # Limpia los datos quitando caracteres de control y espacios en blanco (solo si son cadenas)
    cleaned_data = [str(item).strip() if isinstance(item, str) else item for item in data]

    # Filtrar NaNs (Not a Number, un tipo especial de float en pandas)
    cleaned_data = [item for item in cleaned_data if item == item]

    # Dividir los datos en números y cadenas
    numbers = [item for item in cleaned_data if isinstance(item, (int, float))]
    strings = [item for item in cleaned_data if isinstance(item, str)]

    # Obtener valores únicos
    numbers = list(set(numbers))
    strings = list(set(strings))

    # Ordenar por separado
    numbers_sorted = sorted(numbers)
    strings_sorted = sorted(strings)

    # Combinar y devolver
    return numbers_sorted + strings_sorted

#-------------

@app.get("/data/{column_name}", response_class=HTMLResponse)
def count_values(column_name: str):
    
    global df
    
    if column_name in df.columns:
            column_values = df[column_name].dropna()

            if pd.api.types.is_numeric_dtype(column_values):
                sorted_values = column_values.sort_values().unique()
                
                value_counts = column_values.value_counts()
                
                # Convertir a HTML
                html_output = "<ul>"
                
                for value in sorted_values:
                    count = value_counts.get(value, 0)
                    html_output += f"<li>{value} - Aparece {count} veces</li>"
                html_output += "</ul>"
                
                return  f"<h3>Conteo de valores para la columna '{column_name}'</h3>{html_output}"
            
            else:
                sorted_values = column_values.astype(str).str.strip().unique()
                sorted_values = sorted(sorted_values)
                
            value_counts = column_values.value_counts()

            # Convertir a HTML
            html_output = "<ul>"
            
            for value in sorted_values:
                count = value_counts.get(value, 0)
                html_output += f"<li>{value}</li>"
            html_output += "</ul>"
            
            return  f"<h3>Valores para la columna '{column_name}'</h3>{html_output}"
                    
    else:
            return "Columna no encontrada"





#----------------------------------------------------------------------------------------------------------------------------

@app.get('/get_director/{nombre_director}',response_class=HTMLResponse)
def get_director(nombre_director:str):
    
    global df
    
    """ 
    Se ingresa el nombre de un director que se encuentre dentro de un dataset 
    debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento,
    retorno individual, costo y ganancia de la misma. 
    En formato lista.
    """
    
    if any(nombre_director.lower() == director.lower() for director in df['director'].str.lower().values):
        # Filtrar el DataFrame para ver sólo las filas con ese valor específico
        df_director = df[df['director'] == nombre_director]

        # Crear una lista de diccionarios, donde cada diccionario contiene la información de una película
        
        pelicula = " Director: " + nombre_director + ", retorno total: " + str(df_director['return'].sum())+ "<br><br>"

        peliculas=[]
        peliculas.append(pelicula)
        for index, row in df_director.iterrows():

            revenue_formateada = "{:,}".format(int(row['revenue'])).replace(",", "x").replace(".", ",").replace("x", ".")
            budget_formateada = "{:,}".format(int(row['revenue'])).replace(",", "x").replace(".", ",").replace("x", ".")
            peliculas.append({
                
                'Pelicula': row['title'], # Asegúrate de reemplazar estos nombres de columnas por los correctos
                'fecha_lanzamiento': row['release_date'],
                'retorno': row["return"],
                'costo': budget_formateada + " $",
                'ganancia': revenue_formateada+ " $"
                
            })
        resultado=""    
        for elemento in peliculas:
            resultado = resultado + (str(elemento))[1:-1] + "<br><br>"
            resultado = resultado.replace("'","")

        return  resultado
    else:
        return {"mensaje": "No existe ese director en la base de datos."}
    
#------------------------------------------------------------------------------------------------------

@app.get('/actor_principal/{nombre_actor}',response_class=HTMLResponse)
def get_actor(nombre_actor:str):
    
    global df
    if any(nombre_actor.lower() == actor.lower() for actor in df['actor_principal'].str.lower().values):
    # Your code here if the condition is met

        # Filtrar el DataFrame para ver sólo las filas con ese valor específico
        df_actor = df[df['actor_principal'].str.lower() == nombre_actor.lower()]

        # Crear una lista de diccionarios, donde cada diccionario contiene la información de una película
        
        pelicula = " Actor Principal: " + nombre_actor.title() + " "

        peliculas=[]
        peliculas.append(pelicula)
        cantidad=0
        for index, row in df_actor.iterrows():
            peliculas.append({
                'Pelicula': row['title'], 
                'fecha_lanzamiento': row['release_date'],            
                'Director': row['director']
                             })
            
        if len(peliculas) > 1:
            primer_pelicula = peliculas.pop(0)
            peliculas = [primer_pelicula] + sorted(peliculas, key=lambda x: x['fecha_lanzamiento'])

        
        resultado="" 
        cantidad=0
        
        for elemento in peliculas:
            
            if cantidad == 0:
                  resultado = resultado + (str(elemento))[1:-1] + "<br><br>"
            else: 
                  resultado = resultado + str(cantidad) + "- " + (str(elemento))[1:-1] + "<br>"
                  
            resultado = resultado.replace("'","")
            cantidad+=1
        

        return  resultado
    else:
        return {"mensaje": "No existe ese Actor en la base de datos."}


#-------------------------------------------------------------------------

# Definir el tamaño del lote para el cálculo de la similitud de coseno


@app.get('/recomendacion/{titulo}',response_class=HTMLResponse)
def calcular_recomendacion(titulo: str):
    
        global df
        df_total = df

        ganadores=pd.DataFrame()
        # Extraer el contenido (filas) del título del DataFrame completo
        df_total['content'] =\
        df_total['title'].fillna('') + \
        df_total['genres'].fillna('') + df_total['genres'].fillna('') + df_total['genres'].fillna('') + df_total['genres'].fillna('') + \
        df_total['belongs_to_collection'].fillna('') + df_total['belongs_to_collection'].fillna('') + \
        df_total['belongs_to_collection'].fillna('') + df_total['belongs_to_collection'].fillna('') + df_total['belongs_to_collection'].fillna('') + \
        df_total['production_companies'] + df_total['production_companies'] #+ \
        #df_total['actor'] + \
        #df_total['director'] + \
        #str(df_total['vote_average']) + str(df_total['vote_average'])

        columnas_a_mantener = ['title','content']
        # Obtener la lista de las columnas que deseas borrar
        columnas_a_borrar = [col for col in df_total.columns if col not in columnas_a_mantener]
        # Borrar las columnas no deseadas del DataFrame
        df_total = df_total.drop(columns=columnas_a_borrar)
        #if titulo in df_total['title']: (es menos eficiente)

        if titulo.lower() in df_total['title'].str.lower().values:
  
                        fila_titulo = df_total[df_total['title'] == titulo]
                        
                        

                        tamanio_del_lote=1000
                        indice_inicial = 0  #al principio sera siempre cero, luego sera el indice proximo al indice final recien utilizado
                        indice_final = tamanio_del_lote #al principio es el tamaño del lote, luego ira subiendo
                        tamanio_total_del_csv=len(df_total)
                        datos_restantes_a_evaluar=len(df_total)
                        ganadores_de_cada_competencia=33 #a prueba y error 40 fue el menor numero con buen resultado final de recomendacion
                                
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
                                ganadores = df_a_competir.iloc[recommendation_indices].head(5)
                        
                        # Obtener los títulos de recomendaciones_totales
                        ganadores = ganadores['title'].values.tolist()

                        # Unir los títulos con saltos de línea
                        text = "<br>".join(ganadores) + "<br>" 
                        

                        return(text)
    

        else:
                        return "La pelicula no se encuentra en esta base de datos, o no existe, o esta mal escrita"