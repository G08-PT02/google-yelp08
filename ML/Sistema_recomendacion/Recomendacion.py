from google.cloud import bigquery
import os
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import math

class recomendacion:
    def __init__(self):
        spacy.cli.download("en_core_web_md")
        spacy.cli.download("en_core_web_sm")
        spacy.cli.download("es_core_news_sm")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credencial.json"

