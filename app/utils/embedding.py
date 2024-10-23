from sentence_transformers import SentenceTransformer
import numpy as np

# Carregar um modelo pré-treinado
model = SentenceTransformer('all-MiniLM-L6-v2')  # Você pode escolher outro modelo se preferir

def convert_to_vector(query):
    # Converter sua consulta para um vetor usando o modelo carregado
    vector = model.encode(query)  # O método encode converte a string em um vetor
    return vector.tolist()  # Retorna como lista, se necessário