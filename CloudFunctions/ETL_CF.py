from datetime import datetime
from google.cloud.storage import Blob
from google.cloud import storage
import numpy as np
import string as string
import pandas as pd
import os
import gcsfs
from io import BytesIO
from deep_translator import GoogleTranslator
from googletrans import Translator
import re
from google.cloud import bigquery
import db_dtypes
from textblob import TextBlob
import googlemaps
import json
import ast 

project_name = 'pure-hue-399113'
datawarehouse = 'restaurant_staging_dataset'

def etl(event, context):
    
    file = event
    source_file_name=file['name']   #nombre del archivo nuevo en el bucket
    print(source_file_name)
    print(event)
    source_bucket_name = file['bucket'] #nombre del bucket donde esta el archivo
    print(f"Se detectó que se subió el archivo {source_file_name} al bucket {source_bucket_name}.")
    client = storage.Client(project="ProyectoGrupal")   #declara proyecto

    destination_bucket_name = 'restaurantes100'  # bucket de destino
    destination_file_name=file['name']  # nombre del archivo destino

    #Para el etl

    # Obtiene los buckets
    source_bucket = client.get_bucket(source_bucket_name)
    destination_bucket = client.get_bucket(destination_bucket_name)

    # Obtiene el objeto del archivo a extraer
    source_blob = source_bucket.get_blob(source_file_name)

    # Crea un objeto blob para el archivo de destino
    destination_blob = destination_bucket.blob(destination_file_name)
    blop=source_bucket.blob(source_file_name)
    data=blop.download_as_string()

    print(source_file_name)
    # se evalua el nombre del archivo
    if "metadato_sitio.json" in source_file_name:
        #cargamos dataset
        sitios= pd.read_json(BytesIO(data),lines=True)

        # Limpiar los valores faltantes en la columna "categories"
        # Elimando duplicados
        sitios.drop_duplicates(subset='gmap_id',inplace=True)
        sitios.rename(columns={'gmap_id': 'business_id'}, inplace=True)
        sitios.reset_index(drop=True, inplace=True)

        
        #Borramos la columnas que no usamos
        sitios.drop(columns=['price','state','relative_results', 'url','avg_rating','num_of_reviews'],inplace=True)

         #Cateogorizando Final
        def extract_restaurant_category(row):
            matches = re.findall(r"'([^']*\brestaurant\b[^']*)'", row)
            return ', '.join(matches)

        #Algunos archivos no funcionan con nuestra funcion extract_restaurant_category por lo que hay que hacer una adecuación
        def convertir_lista_a_cadena(lista):
            cadena_formateada = str(lista)
            return cadena_formateada
        
        sitios['category'] = sitios['category'].apply(convertir_lista_a_cadena)
        sitios['category'] = sitios['category'].apply(extract_restaurant_category)
        
        #Con la transformación anterior se eliminar los que tiene únicamente la palabra Restaurant
        sitios['category']=sitios['category'].replace('','Restaurant')
        sitios = sitios[~sitios['category'].str.strip().str.lower().eq('restaurant')]

        categorias=['Fast food restaurant', 'Pizza restaurant', 'Mexican restaurant',
       'Chinese restaurant', 'American restaurant', 'Breakfast restaurant',
       'Italian restaurant', 'Barbecue restaurant', 'Seafood restaurant',
       'Health food restaurant', 'Thai restaurant', 'Japanese restaurant',
       'Hamburger restaurant', 'Family restaurant', 'Indian restaurant',
       'Chicken restaurant', 'Dessert restaurant', 'Vietnamese restaurant',
       'Sushi restaurant', 'Mediterranean restaurant',
       'Chicken wings restaurant', 'Taco restaurant', 'Asian restaurant',
       'Jamaican restaurant', 'Korean restaurant', 'Soul food restaurant',
       'Latin American restaurant', 'Dominican restaurant',
       'Fine dining restaurant', 'Salvadoran restaurant',
       'Caribbean restaurant', 'Vegan restaurant', 'Hot dog restaurant',
       'Peruvian restaurant', 'New American restaurant', 'Greek restaurant']

        sitios = sitios[sitios['category'].isin(categorias)]
       
        sitios.reset_index(drop=True, inplace=True)
        print(sitios.shape)
       #Consulta de BigQuary para evitar ID repetidos:
    
        #cargamos dataset de review bigquery
        client = bigquery.Client(project=project_name)
        sql_query = ('''SELECT DISTINCT business_id
                FROM pure-hue-399113.restaurant_staging_dataset.restaurants_dim
                ''')
        sitios_dw = client.query(sql_query).to_dataframe()
        sitios_id = sitios_dw['business_id']

        # Filtrar el DataFrame para que no se repitan los sitios
        sitios = sitios[-sitios['business_id'].isin(sitios_id)]

        print(f"Después de la filtración, quedan {len(sitios)} filas en el DataFrame.")
        
        if sitios.shape[0] != 0:

            #Tabla_Category
            Category_df = pd.pivot_table(sitios, index='business_id', columns='category', aggfunc=lambda x: 1, fill_value=0)


            Datos_Geograficos=sitios[['business_id','address','latitude','longitude']].copy()
            MISC_copy=sitios[['business_id','MISC']].copy()
            Horarios=sitios[['business_id','hours']].copy()
            sitios.drop(columns=['latitude','longitude','address','MISC'],inplace=True)
            
            
            #DatosGeograficos
            #Relleno nulls
            Datos_Geograficos["address"].fillna("dato desconocido", inplace=True)

            #armo lista con listas para cada columna
            nombre_local, direccion, ciudad, codigo_postal = [], [], [], []

            for i in Datos_Geograficos["address"]:
                #separo cada string despues de la coma
                parts = i.split(',')

                if len(parts) >= 4:
                    nombre_local.append(parts[0].strip()) 
                    direccion.append(parts[1].strip())
                    ciudad.append(parts[2].strip())
                    codigo_postal.append(parts[3].strip())
                else:
                    nombre_local.append('')
                    direccion.append('')
                    ciudad.append('')
                    codigo_postal.append('')

            df_address = pd.DataFrame({'Name': nombre_local, 'Address': direccion, 'City': ciudad, 'Postal Code': codigo_postal})

            # separo la columna postal code en estado y codigo postal
            df_address[['Postal Code', 'State']] = df_address['Postal Code'].str.split(n=1, expand=True)

            # renombro
            df_address.columns = ['Nombre', 'Direccion', 'city', 'state', 'postal_code']
            
            counter = 0
            for i in df_address:
                Datos_Geograficos.insert(counter, i, df_address[i])
                counter += 1
            
            Datos_Geograficos.drop(columns=['address','Nombre'],inplace=True)
            Datos_Geograficos.fillna("dato desconocido", inplace=True)
            Datos_Geograficos.rename(columns={'Direccion': 'address'}, inplace=True)
            States = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'Ml', 'MN', 'MO', 'MS', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
            Datos_Geograficos=Datos_Geograficos[Datos_Geograficos['state'].isin(States)]

            #Horarios
            Horarios['hours'].fillna("[['Thursday', 'Sin Dato'], ['Friday', 'Sin Dato'], ['Saturday', 'Sin Dato'], ['Sunday', 'Sin Dato'], ['Monday', 'Sin Dato'],['Tuesday', 'Sin Dato'], ['Wednesday', 'Sin Dato']]", inplace=True)
            dataframes_individuales = []

            for _, row in Horarios.iterrows():
                try:
                    lista_horarios = ast.literal_eval(row['hours'])
                    df = pd.DataFrame(lista_horarios, columns=['Dia', 'Horario'])
                    df['business_id'] = row['business_id']
                    dataframes_individuales.append(df)
                except (ValueError, SyntaxError):
                    pass  # Ignora las filas con valores NaN o cadenas mal formadas.

            # Concatena todos los DataFrames individuales en uno solo.
            tabla_pivot_total = pd.concat(dataframes_individuales)

            # Pivotea la tabla.
            Tabla_Horarios = tabla_pivot_total.pivot(index='business_id', columns='Dia', values='Horario')
            Tabla_Horarios=Tabla_Horarios.reset_index()

            #MISC (atributos):
            MISC_copy = MISC_copy.replace('null', np.nan)
            MISC_copy['MISC'] = MISC_copy['MISC'].fillna('{}')
            MISC_copy['MISC'] = MISC_copy['MISC'].apply(lambda x: json.dumps(x))
            MISC_copy['MISC'] = MISC_copy['MISC'].apply(ast.literal_eval)
            df_expanded = pd.json_normalize(MISC_copy['MISC'].tolist())
            MISC_df = pd.concat([MISC_copy.drop('MISC', axis=1), df_expanded], axis=1)
            MISC_df=MISC_df.set_index('business_id')
            # Función para extraer el texto de una lista de cadenas
            def extraer_texto(lista):
                if isinstance(lista, list):
                    return ', '.join([item for item in lista if isinstance(item, str)])
                return np.NaN
            MISC_df = MISC_df.applymap(extraer_texto)
            MISC_df.reset_index(inplace=True)
            MISC_df.rename(columns={'index': 'business_id'}, inplace=True)

            #Guardamos Restaurantes
            source_file_name_sitios = source_file_name.replace('.json', '.parquet')
            sitios.to_parquet(f'gs://{destination_bucket_name}/{source_file_name_sitios}')

            #Guardamos Category
            source_file_name_category = source_file_name.replace('.json', '_categ.parquet')
            Category_df.to_parquet(f'gs://{destination_bucket_name}/{source_file_name_category}')

            #Guardemos el dataset Datos Geograficos
            source_file_name_geo = source_file_name.replace('.json', '_geo.parquet')
            Datos_Geograficos.to_parquet(f'gs://{destination_bucket_name}/{source_file_name_geo}')

            #Guardemos el dataset Datos Horarios
            source_file_name_hrs = source_file_name.replace('.json', '_horarios.parquet')
            Tabla_Horarios.to_parquet(f'gs://{destination_bucket_name}/{source_file_name_hrs}')

            #Guardemos el dataset Atributos
            source_file_name_misc = source_file_name.replace('.json', '_misc.parquet')
            MISC_df.to_parquet(f'gs://{destination_bucket_name}/{source_file_name_misc}')
        else:
            print('No se agrego ningún nuevo establecimiento')
        

    elif "reviews_estados" in source_file_name:
        #cargamos dataset
        review = pd.read_json(BytesIO(data), lines = True)

        # Damos formato a la columna 'time'
        review['date']=pd.to_datetime(review['time'], unit='ms')

        # filtrando año mayor
        review = review[review['date'].dt.year > 2005]
        review['date']=review['date'].dt.date        
        
        #cargamos dataset de review bigquery
        client = bigquery.Client(project=project_name)
        sql_query = ('''SELECT DISTINCT business_id
                FROM pure-hue-399113.restaurant_staging_dataset.Restaurantes
                ''')
        sitios = client.query(sql_query).to_dataframe()
        sitios_id = sitios['business_id']

        # Filtrar el DataFrame review para que solo contenga los sitios_id filtrados
        review_filtrado = review[review['business_id'].isin(sitios_id)]

        print('review >>>', review.shape)
        print('review_filtrado >>>', review_filtrado.shape)

        # Limpiar los valores faltantes en la columna "text"
        review_filtrado['text'] = review_filtrado['text'].astype(str)
        review_filtrado['text'] = review_filtrado['text'].fillna('')


        #Guardemos el dataset filtrado
        source_file_name = source_file_name.replace('.json', '.parquet')
        review_filtrado.to_parquet(r'gs://' + destination_bucket_name + '/' + source_file_name)


    elif "yelps_business_sample" in source_file_name:
        
        #cargamos dataset
        business_Yelp = pd.read_csv(BytesIO(data))
        
        #Eliminando Columnas Duplicadas
        business_Yelp = business_Yelp.loc[:, ~business_Yelp.columns.duplicated()]

        #Eliminar columnas que no utilizamos
        business_Yelp.drop(columns=['is_open','review_count','stars'],inplace=True)
        # Rellena los valores nulos con una cadena vacía
        business_Yelp['categories'].fillna('', inplace=True)
        # Dividir la columna "categories" en listas de categorías
        categories_lists = business_Yelp['categories'].str.split(', ')
        # Unir todas las listas en una única lista
        all_categories = [category for categories_list in categories_lists for category in categories_list]
        # Convertir el conjunto de nuevo en una lista si es necesario
        unique_categories = set(all_categories)
        unique_categories_list = list(unique_categories)
        df_business_Yelp = business_Yelp
        # Primero, dividimos los valores de 'categories' en listas de strings
        df_business_Yelp['categories'] = df_business_Yelp['categories'].str.split(',')
        df_business_Yelp = df_business_Yelp.dropna(subset=['categories'])
        #Filtrar por categoría "Restaurantes"
        df_business_Yelp = df_business_Yelp[df_business_Yelp['categories'].apply(lambda categories: 'Restaurants' in categories or 'Pop-Up Restaurants' in categories)]
        # Unir los valores de la lista en categorías en un solo string separado por comas
        df_business_Yelp['categories'] = df_business_Yelp['categories'].apply(lambda x: ','.join(x))
        # Recetar el Indice
        df_business_Yelp.reset_index(inplace=True, drop=True)

        #ESTAS SON LAS TRANSFORMACIONES FINALES PARA QUE COINCIDAN CON LOS DATOS DEL SCHEMA EN BIGQUERY 
        df_business=df_business_Yelp[['business_id','name']].copy()
        df_business_Yelp_datos_geograficos=df_business_Yelp[['business_id','address','city','state','postal_code','latitude','longitude']].copy()
        Horarios=df_business_Yelp[['business_id','hours']].copy()
        df_attributes = df_business_Yelp[['business_id','attributes']].copy()

        #Horarios:
        Horarios['hours'].fillna("{'Monday': 'Sin info', 'Tuesday': 'Sin info', 'Wednesday': 'Sin info', 'Thursday': 'Sin info', 'Friday': 'Sin info', 'Saturday': 'Sin info', 'Sunday': 'Sin info'}", inplace=True)
        dataframes_individuales = []

        for _, row in Horarios.iterrows():
            try:
                lista_horarios = ast.literal_eval(row['hours'])
                df = pd.DataFrame(list(lista_horarios.items()), columns=['Dia', 'Horario'])
                df['business_id'] = row['business_id']
                #df.replace('NaN', np.nan, inplace=True)
                dataframes_individuales.append(df)
            except (ValueError, SyntaxError):
                pass  # Ignora las filas con valores NaN o cadenas mal formadas.

        # Concatena todos los DataFrames individuales en uno solo.
        tabla_pivot_total = pd.concat(dataframes_individuales)

        # Pivotea la tabla.
        Tabla_Horarios = tabla_pivot_total.pivot(index='business_id', columns='Dia', values='Horario')
        Tabla_Horarios.replace(np.nan, 'Sin info', inplace=True)
        # Se asume que cuando hay un '0:0-0:0' es porque pueda estar cerrado.
        Tabla_Horarios.replace('0:0-0:0', 'Cerrado', inplace=True)


        #ATTRIBUTES TRANSFORMACIONES
        

        #desanido attributes:

        #Completamos los valores faltantes en esta columna con '{}'
        df_attributes['attributes'] = df_attributes['attributes'].fillna('{}').apply(ast.literal_eval) 

        def convert_to_dict(val):
            # Transformamos en diccionarios reales los strings que parecen diccionarios
            if isinstance(val, str) and val.startswith("{") and val.endswith("}"):
                return ast.literal_eval(val)
            return val

        df_attributes['attributes'] = df_attributes['attributes'].apply(convert_to_dict)

        #Combierte la columna en una lista de diccionarios y json_normalize pasa los valores a columnas
        df_expanded = pd.json_normalize(df_attributes['attributes'].tolist()) 

        #Combinamos el df original con el nuevo que tiene las columnas separadas
        result_df = pd.concat([df_attributes.drop('attributes', axis=1), df_expanded], axis=1) 

        result_df.drop(columns=["BusinessParking", "WiFi", "ByAppointmentOnly", "AcceptsInsurance",
                        "RestaurantsCounterService", "HappyHour",  "BikeParking",
                        "BusinessAcceptsBitcoin", "DietaryRestrictions", "AgesAllowed",
                        "Open24Hours", "Corkage", "WheelchairAccessible", "DogsAllowed",
                        "RestaurantsTableService", "GoodForMeal","Ambience","Alcohol", 
                        "BYOBCorkage","Smoking", "Music", "DriveThru", "BYOB",
                        "BestNights","CoatCheck", "GoodForDancing", "BikeParking"], inplace=True)

        result_df=result_df.fillna("sin datos")

        result_df.loc[result_df['NoiseLevel'].str.contains('quiet').fillna(False), 'NoiseLevel'] = 1
        result_df.loc[result_df['NoiseLevel'].str.contains('average').fillna(False), 'NoiseLevel'] = 2
        result_df.loc[result_df['NoiseLevel'].str.contains('loud').fillna(False), 'NoiseLevel'] = 3


        df_attributes=result_df.replace("None", "sin datos")

        #Guardemos el dataset filtrado
        source_file_business = source_file_name.replace('.csv', '_business.parquet')
        df_business.to_parquet(r'gs://' + destination_bucket_name + '/' + source_file_business)

        #Guardemos el dataset filtrado
        source_file_geograficos = source_file_name.replace('.csv', '_geograficos.parquet')
        df_business_Yelp_datos_geograficos.to_parquet(r'gs://' + destination_bucket_name + '/' + source_file_geograficos)

        #Guardamos el dataset filtrado
        source_file_horarios = source_file_name.replace('.csv', '_horarios.parquet')
        Tabla_Horarios.to_parquet(r'gs://' + destination_bucket_name + '/' + source_file_horarios)

        #Guardamos el dataset filtrado
        source_file_attributes = source_file_name.replace('.csv', '_attributes.parquet')
        df_attributes.to_parquet(r'gs://' + destination_bucket_name + '/' + source_file_attributes)

    elif "yelps_reviews_sample.csv" in source_file_name:
        print('Entre a la función review yelp')
        df_review_dividido =pd.read_csv(BytesIO(data))


        # Initialize the BigQuery client
        client = bigquery.Client(project=project_name)

        # Define your BigQuery SQL query to fetch the data you need
        sql_query = """ select business_id from pure-hue-399113.datos_crudos_yelp.restaurantes_yelp_crudo """

        print(sql_query)
        

        # Execute the query
        df_ids = client.query(sql_query).to_dataframe()

        print(df_ids)

        # Crear una lista de IDs a partir de df1
        lista_de_ids = df_ids["business_id"].tolist()

        # Filtrar df2 basándose en la lista de IDs de df1
        df_reviews_res = df_review_dividido[df_review_dividido['business_id'].isin(lista_de_ids)].copy()

        #Dejar la fecha en formato año/mes/día: 
        df_reviews_res['date'] = pd.to_datetime(df_reviews_res['date']).dt.date

        print("PARA DEBUGUEAR !!!!!!!!!!!!!!!!!!!!")
        
        print(lista_de_ids)
        

        #Guardemos el dataset filtrado
        source_file_name = source_file_name.replace('.csv', '.parquet')
        df_reviews_res.to_parquet(r'gs://' + destination_bucket_name + '/' + source_file_name)


    elif "user_sample.csv" in source_file_name:
        print('Entre a la función')
        df_user_sample = pd.read_csv(BytesIO(data))

        #Eliminar duplicados:
        df_user_sample = df_user_sample.drop_duplicates(subset='user_id')


        #elimino columna elite
        df_user_sample.drop(columns= 'elite',inplace=True)

        #cargamos dataset bigquery
        client = bigquery.Client(project=project_name)

        sql_query = """ select user_id from pure-hue-399113.datos_crudos_yelp.users_yelp_crudo """

        print(sql_query)

        df_user_id = client.query(sql_query).to_dataframe()

        print(df_user_id)

        # Crear una lista de IDs a partir de df1
        lista_de_user_id = df_user_id["user_id"].tolist()        

        # Filtrar basándose en la lista de IDs que aparecen en Restaurant 
        df_user_review_r = df_user_sample[df_user_sample['user_id'].isin(lista_de_user_id)].copy()

        #Dejar la fecha en formato año/mes/día: 
        df_user_review_r['yelping_since'] = pd.to_datetime(df_user_review_r['yelping_since']).dt.date

        #Guardemos el dataset filtrado
        source_file_name = source_file_name.replace('.csv', '.parquet')
        df_user_review_r.to_parquet(r'gs://' + destination_bucket_name + '/' + source_file_name)

                
    elif "tip_sample.csv" in source_file_name:
        print('Entre a la función tip sample')
        df_tip = pd.read_csv(BytesIO(data))
        
        
        #cargamos dataset bigquery
        client = bigquery.Client(project=project_name)

        sql_query = """ select user_id from pure-hue-399113.restaurant_staging_dataset.yelp_users """

        df_user_id = client.query(sql_query).to_dataframe()
        
        # Crear una lista de IDs a partir de df1
        lista_de_user_id = df_user_id["user_id"].tolist()        

        # Filtrar basándose en la lista de IDs que aparecen en Restaurant
        df_tip_r = df_tip[df_tip['user_id'].isin(lista_de_user_id)].copy()

        #Dejar la fecha en formato año/mes/día: 
        df_tip_r['date'] = pd.to_datetime(df_tip_r['date']).dt.date

        #Guardemos el dataset filtrado
        source_file_name = source_file_name.replace('.csv', '.parquet')
        df_tip_r.to_parquet(r'gs://' + destination_bucket_name + '/' + source_file_name)


    return print(f"Archivo {source_file_name} del bucket {source_bucket_name} procesado con éxito.")
