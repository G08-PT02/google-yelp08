from google.cloud import bigquery
import os
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import math
import numpy as np

class recomendacion:
    def __init__(self):
        self.nlp_en = self.load_model("en_core_web_md")
        #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credencial.json"
        #self.df = self.consulta()
        self.df = pd.read_pickle('../Datasets_ML/Rest_final_ML.pickle')

    def load_model(self,model_name): 
        # Intenta cargar el modelo
        try:
            nlp = spacy.load(model_name)
            return nlp
        except OSError:
            print(f"El modelo {model_name} no está instalado. Descargando e instalando...")
            spacy.cli.download(model_name)
            nlp = spacy.load(model_name)
            return nlp

    def query(self):
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
    
    def keywords(self,text):
        # Procesar el texto con spaCy
        if len(text.split()) == 1:
            return [text]
        else:
            doc = self.nlp_en(text)
            # Extraer sustantivos (nombres) y adjetivos
            palabras_clave = [token.text for token in doc if token.pos_ in ['NOUN', 'ADJ']]
            return palabras_clave

    def search(self,lista_busqueda, umbral_similitud=0.7):
        indices = []
        embeddings_busqueda = np.array([self.nlp_en(palabra).vector for palabra in lista_busqueda])

        for index, embedding in enumerate(self.df['embedding']):
            if embedding is not None:
                # Calcular la similitud coseno solo si el embedding es válido (no es None)
                similitudes = cosine_similarity(embedding, embeddings_busqueda).max(axis=1)
                
                # Si la similitud es mayor que el umbral, agregar el índice
                if np.any(similitudes >= umbral_similitud):
                    indices.append(index)

        return indices
    
    def distance(self,user_location, restaurant_location):
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
    
    def main(self,text,coord,limit=5):
        keywords = self.keywords(text)
        indices = self.search(keywords)
        df_recom = self.df.iloc[indices].reset_index()
        df_recom['distance'] = df_recom.apply(lambda row: round(self.distance(coord, row['coord']),2), axis=1)
        df_recom = df_recom.sort_values(by='distance', ascending=True).reset_index().head(limit)
        return df_recom[['name','address','distance','coord']]
