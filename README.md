PROYECTO INDIVIDUAL:

--------------------------------------------------------------
Archivos:
#--

Los Datasets provistos sin modificacion alguna esta dentro de la carpeta /Datasets, ellos son:
    -movies_dataset.csv
    -movies_dataset.xlsx
    -movies_dataset(1).xlsx (renombrado a movies_dataset_1.xlsx) para evitar conflitos por los parentesis

Los creados dentro de la carpeta Dataset, para 
poder comparar los .csv con el xlsx se crean archivos adicionales:

    -movies_dataset_antes_xlsx.csv(convertido a csv)
    -movies_dataset_antes_xlsx_cleaned.csv(transformado solo a fines de comparacion si son iguales)
    -movies_dataset_cleaned.csv(transformado solo a fines de comparacion si son iguales)

dentro de el REPO PRINCIPAL: PROYECTO INDIVIDUAL encontramos los archivos:
        
    -abreviaturas_de_paises.csv - (contiene las abreviaturas de los paises y nombre del pais por fila)

    -actor_principal_y_id.csv - (contiene indice, actor principal e ID de la peli que corresponde)

    -actores_principales.csv - (contiene todos los actores principales por fila, y cada fila representa la pelicula que         corresponde a ese actor en orden segun el id, del dataset final2.csv)

    -COMANDOS RENDER_FASTAPI_GITHUB.txt - (con algunos comandos para copiar y pegar en la terminal fácilmente)

    -credits_csv_a_parquet.py - (archivo que se uso previamente con credits.csv antes de crear el repo en git, estava credits.csv como archivo provisto, pero era muy pesado para subir a github directamente, entonces para no tener que instalar large file system de github, se paso a parquet, ya que con parquet se puede subir normalmente al repo de github por su peso)

    credits.parquet - (representa a credits.csv tiene tres columnas, cast, crew, y id, cast es de donde extraigo actor principal, crew es de donde extraigo director de la pelicula, y ID es el ID compartido con movies_dataset que corresponde a la fila de la pelicula)

    Diccionario de Datos - Movies - Hoja1.csv - (descripcion de las columnas de movies_dataset.csv)

    director_y_id_de_credits - (contiene indice, director e ID de la peli a la que corresponde)

    directores_listado.csv - (archivo que solo contiene todo el listado de directores)

    EDA.ipynb - (archivo para realizar el análisis de datos exploratorio, "EDA")

    final.csv - (archivo resultante luego de ejecutar el archivo Transformaciones y unificacion de los 3 datsets.ipynb, tomando como base al archivo movies_dataset.csv ,con algunas transformaciones no pedidas, pero indefectiblemente necesarias para que no hayan ERRORES luego en la limpieza de datos solicitada)

    final2.csv - (archivo totalmente limpio, con cada transformacion solicitada, eliminacion de datos, reemplazos, y creacion de nuevas columnas)

    pruebas.ipynb - (archivo para realizar pruebas aisaladas, no es importante en el repo)

    pruebas.py - (archivo para realizar pruebas aisaladas con uso de terinal, no es importante en el repo)

    Este mismo archivo README.md - (para entender el repo, lo que se hizo paso a paso y lo que hace el archivo main.py, entre otros archivos importntes del repo)

    recomendaciones_tfidf_vector.py - (archivo para probar el modelo de recomendacion de peliculas)

    requirements.txt - (archivo para que RENDER sepa que librerias uso y va a tener que disponibilizar en el web service)

    Transformaciones y unificacion de los 3 datsets.ipynb (archivo donde inicio a analizar los datasets crudos que nos dieron, y me quedo con uno solo, viendo que los datos sean consistntes, y comparando los tres archivos que PARECIERAN tener la misma informacion, sin discrepancias, pero eso no fue asi, luego del proceso termino creando el archivo final.csv para seguir trabajando solo con ese dataset de los tres unificando todo en ese archivo)

    Transformaciones2.ipynb - (en este archivo termino de  hacer la ETL solicitada, creando columnas, eliminando columnas, limpiando datos, analizando outliers, y doy por finalizada la ETL)

------------------------------------------------------------------------------------------------------------------------

1)Transformaciones y unificacion de los 3 datsets 

Primero tenemos que unificar, transformando si es necesario, los tres archivos de dataset que nos dieron:
1-Ver si son iguales, para descartar alguno, o analizar las diferencias que pudiesen existir
2-ver si las cantidades de filas son iguales en los tres archivos
3-ver si hay columnas faltantes, repetidas, o de igual nombre pero con diferentes campos
empezamos por ver si son diferentes los dataset movies_dataset.xlsx, movies_dataset(1).xlsx,y movies_dataset.csv:

1-Descarto el archivo duplicado movies_dataset(1).xlsx ya que es igual al original
2-Investigo esas diferencias entre los dos archivos restantes .XLSX y .CSV:

Veo sus columnas y tipos de datos que contienen:
primero el dataframe del archivo CSV:


Función para eliminar todas las comas consecutivas al final de una línea si hay 3 o más:

porque cuando lee EXCEL Files, las celdas del excel vacias en columnas ultimas que no tienen dato, pero
si en esa columna de las miles de filas hay aunque sea un dato en esa columna en una fila, al leer el archivo 
agrega esa columna al CSV como par de comas, representando la columna y campo vaciio para las miles de filas
restantes solo por esa fila que si tiene un dato, las toma como dato.
ENTONCES: hacemos un codigo que si encuentra comas al final de cada fila las elimine
las filas deben terminar con un dato sin coma final, en el caso hipotetico de tener un caso que termine con ,,
seria campo vacio en el CSV, este codigo daria error ya que tmb lo que hago en este codigo es unir saltos de linea
incorrectos, que el excel interpreto como campos vacios los restantes de la linea, en vez de quitar automaticamente
el salto de linea, y colocar en la linea actual la linea siguiente, al hacer la union, y al final hacer la conversion 
de CSV a DataFrame deberia darme error si elimine un campo que terminaba en ,, , ya que en ese caso la extension de
columnas no seria la misma para la totalidad de las filas, pero medio bien, asi que ningun problema


Abro los dos archivos movies_dataset_cleaned.csv, y movies_dataset_antes_xlsx_cleaned.csv, y convierto todos sus campos a strings para poder luego trabajarlos comodamente:

cambiar valores erroneos, columnas mal situadas en el orden de los dos dataframe tanto del archivo movies_dataset_cleaned.csv como del archivo movies_dataset_antes_xlsx.csv , todo esto luego de la lectura de los dataframe

Ahora nuevamente trato de Encontrar las filas y columnas donde los dataframes de cadena difieren, a traves del metodo ".ne" luego de las previas trasnformaciones, por si quedaron datos que no concuerdan entre dataframes

<h3>Finalmente ya unificamos los datasets, y creamos un único dataset final.csv para seguir con las transformaciones pedidas</h3>

-----------------------------------------------------------------------------------------------------------------

Cargo dataset final.csv como dataframe Y seteo los tipo de datos a los que corresponden cada columna:

Transformaciones solicitadas por el cliente:

Desanidando belongs_to_collection

Desanidando production_companies:

Desanidando production_countries

Agrego Desanidar spoken_language, para saber a que idioma pertenece la abreviatura: NO PUEDO SABERLO SOLO CON ORIGINAL_LANGUAGE PORQUE NO INCLUYE LOS NOMBRES DE LOS IDIOMAS, SPOKEN LANGUAGES SI LOS INCLUYE

Ahora si desanidando Spoken_Languages para limpiar la columna:

Para nulos de los campos de las columnas: revenue y budget, deben ser rellenados por el número 0.

Los valores nulos del campo release date deben eliminarse. 

De haber fechas, deberán tener el formato AAAA-mm-dd, además deberán crear la columna release_year doncrearde extraerán el año de la fecha de estreno.

Extracción del año de estreno de release_date:

Crear la columna con el retorno de inversión, llamada return con los campos revenue y budget, dividiendo estas dos últimas revenue / budget, cuando no hay datos disponibles para calcularlo, deberá tomar el valor 0.

Eliminar las columnas que no serán utilizadas, video,imdb_id,adult,original_title,poster_path y homepage.

Desanido Genres(A criterio mio, para que quede menos data que no sirve y ocupa espacio):

Extraigo director de credits.parquet, y lo agrego como columna:

Extraigo actor principal para adicionar como molumna a final2.csv dataset principal

<h5>Ahora joiniamos Actores principales y directores al dataframe final2.csv con el que finalmente vamos a trabajar:</h5>

----------------------------------------------------------------------------------------------------------------------------

EDA:

concluciones:
-el 75% de los votantes votaron de 6.8 para abajo, pocas son las votaciones muy positivas por lo visto

-el lapso temporal que manejamos en el datasetva del año 1874 al 2020

-vemos que hay outliers en la columna popularity valor 547 contra valores muy bajos de 3.69 del 75% de las peliculas

-vemos que los datos no estan escalados por los outliers y datos no validos, o no completados correctamente de columnas como budget, revenue, return dadas las columnas budget y revenue


-obviamente  vemos como la correlatividad es alta con budget y revenue, ya que a mayor inversion, se espera mayor retorno de ganancia la correlatividad es 0.76

-luego le sigue con 0.47 la popularidad con el revenue, se entiende que si la pelicula tuvo mucha popularidad es porque fue buena, y eso claramente dio mas revenue a la productora

lo mismo sucede pero en un poco menor medida con el budget teniendo una correlatividad positiva de 0.45 con la popularidad, porque a mayor inversion, mayor publicidad, mejores actores, mayor difusion, y a veces en general resulta un pelicula con recursos interesantes ya que hay presupuesto.

Podemos observar que la gran mayoria de las peliculas 

podemos apreciar que mas de la mitad de las peliculas se han hecho a un muy bajo budget, mas del 75% de todo el dataset se han hecho con 3.000.000 usd aprox por lo que se puede apreciar del grafico

seguirian las mejoras del mvp, mejorando el heatmap de palabras dentro de los titulos, para generar titulos convincentes, y atractivos para crear nuevas peliculas a futuro



    


















<h3>Primero tenemos que unificar, transformando si es necesario, los tres archivos de dataset que nos dieron:</h3>
1-Ver si son iguales, para descartar alguno, o analizar las diferencias que pudiesen existir<br>
2-ver si las cantidades de filas son iguales en los tres archivos<br>
3-ver si hay columnas faltantes, repetidas, o de igual nombre pero con diferentes campos<br><br>
empezamos por ver si son diferentes los dataset movies_dataset.xlsx, movies_dataset(1).xlsx,y movies_dataset.csv:

1-Descarto el archivo duplicado movies_dataset(1).xlsx ya que es igual al original<br><br>
2-Investigo esas diferencias entre los dos archivos restantes .XLSX y .CSV:

Veo sus columnas y tipos de datos que contienen:<br>
-primero el dataframe del archivo CSV:

   Función para eliminar todas las comas consecutivas al final de una línea si hay 3 o más.<br>



    porque cuando lee EXCEL Files, las celdas del excel vacias en columnas ultimas que no tienen dato, pero
    si en esa columna de las miles de filas hay aunque sea un dato en esa columna en una fila, al leer el archivo 
    agrega esa columna al CSV como par de comas, representando la columna y campo vaciio para las miles de filas
    restantes solo por esa fila que si tiene un dato, las toma como dato.
    ENTONCES: hacemos un codigo que si encuentra comas al final de cada fila las elimine
    las filas deben terminar con un dato sin coma final, en el caso hipotetico de tener un caso que termine con ,,
    seria campo vacio en el CSV, este codigo daria error ya que tmb lo que hago en este codigo es unir saltos de linea
    incorrectos, que el excel interpreto como campos vacios los restantes de la linea, en vez de quitar automaticamente
    el salto de linea, y colocar en la linea actual la linea siguiente, al hacer la union, y al final hacer la conversion 
    de CSV a DataFrame deberia darme error si elimine un campo que terminaba en ,, , ya que en ese caso la extension de
    columnas no seria la misma para la totalidad de las filas, pero medio bien, asi que ningun problema


Abro los dos archivos movies_dataset_cleaned.csv, y movies_dataset_antes_xlsx_cleaned.csv, y convierto todos sus campos a strings para poder luego trabajarlos comodamente:

cambiar valores erroneos, columnas mal situadas en el orden de los dos dataframe tanto del archivo movies_dataset_cleaned.csv como del archivo movies_dataset_antes_xlsx.csv , todo esto luego de la lectura de los dataframe:

Ahora nuevamente trato de Encontrar las filas y columnas donde los dataframes de cadena difieren, a traves del metodo ".ne" luego de las previas trasnformaciones, por si quedaron datos que no concuerdan entre dataframes:

<h4>Finalmente ya unificamos los datasets, y creamos un único dataset final.csv para seguir con las transformaciones pedidas</h4>





