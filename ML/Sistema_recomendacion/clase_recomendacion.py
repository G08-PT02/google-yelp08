from google.cloud import bigquery
import os
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import math
import numpy as np

class recomendacion:
    def __init__(self):
        self.nlp_en = spacy.load("en_core_web_md")
        spacy.cli.download("en_core_web_sm")
        spacy.cli.download("es_core_news_sm")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credencial.json"
        self.df = self.consulta()

    def load_model(model_name): 
        # Intenta cargar el modelo
        try:
            nlp = spacy.load(model_name)
            return nlp
        except OSError:
            print(f"El modelo {model_name} no está instalado. Descargando e instalando...")
            spacy.cli.download(model_name)
            nlp = spacy.load(model_name)
            return nlp

    def consulta(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../credencial.json"

        client = bigquery.Client()

        query = f"""
        SELECT *
        FROM `pure-hue-399113.googleBase.Restaurantes`
        """

        query_job = client.query(query)
        results = query_job.result()

        rows = []
        for row in results:
            rows.append(row)

        results_df = pd.DataFrame(data=[list(x.values()) for x in rows], columns=list(rows[0].keys()))
        return results_df
    
    def palabras_clave(self,texto, idioma):
        # Cargar el modelo de spaCy según el idioma
        if idioma == "es":
            nlp = spacy.load("es_core_news_sm")
        elif idioma == "en":
            nlp = spacy.load("en_core_web_sm")
        else:
            raise ValueError("Idioma no compatible. Usa 'es' para español o 'en' para inglés.")

        # Procesar el texto con spaCy
        doc = nlp(texto)

        # Extraer sustantivos (nombres) y adjetivos
        palabras_clave = [token.text for token in doc if token.pos_ in ['NOUN', 'ADJ']]

        return palabras_clave

    def buscar_palabras_similares(self,dataframe, columna, lista_busqueda, umbral_similitud=0.7):
        indices = []

        # Calcular embeddings para las palabras de la lista de búsqueda
        embeddings_busqueda = np.array([self.nlp_en(palabra).vector for palabra in lista_busqueda])

        for index, palabras_lista in enumerate(dataframe[columna]):
            # Calcular embeddings para las palabras de la lista actual
            embeddings_lista = np.array([self.nlp_en(palabra).vector for palabra in palabras_lista])
            
            # Calcular la similitud coseno entre los embeddings de las palabras de la lista actual y las de búsqueda
            similitudes = cosine_similarity(embeddings_lista, embeddings_busqueda).max(axis=1)
            
            # Si la similitud es mayor que el umbral, agregar el índice
            if np.any(similitudes >= umbral_similitud):
                indices.append(index)

        return indices
    
    def distancia(self,user_location, restaurant_location):
        # Extraer las coordenadas de latitud y longitud del usuario y del restaurante
        user_lat, user_lon = user_location
        restaurant_lat, restaurant_lon = restaurant_location

        # Radio de la Tierra en kilómetros
        R = 6371.0

        # Convertir latitud y longitud de grados a radianes
        user_lat = math.radians(user_lat)
        user_lon = math.radians(user_lon)
        restaurant_lat = math.radians(restaurant_lat)
        restaurant_lon = math.radians(restaurant_lon)

        # Diferencia en latitud y longitud
        dlon = restaurant_lon - user_lon
        dlat = restaurant_lat - user_lat

        # Fórmula de Haversine para calcular la distancia
        a = math.sin(dlat / 2)**2 + math.cos(user_lat) * math.cos(restaurant_lat) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Distancia en kilómetros
        distance = R * c

        return distance
