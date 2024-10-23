import psycopg2
import numpy as np
import pandas as pd
from tqdm import tqdm
import numpy as np
from datetime import datetime, timedelta
import random
from sentence_transformers import SentenceTransformer
import numpy as np

# Carregar um modelo pré-treinado
model = SentenceTransformer('all-MiniLM-L6-v2')  # Você pode escolher outro modelo se preferir

def convert_to_vector(query):
    # Converter sua consulta para um vetor usando o modelo carregado
    vector = model.encode(query)  # O método encode converte a string em um vetor
    return vector.tolist()  # Retorna como lista, se necessário

# Function to generate a random publication date within the last year
def generate_random_date():
    days_delta = random.randint(0, 365)  # Random number of days in the last year
    return (datetime.now() - timedelta(days=days_delta)).date()

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname='mydb',
        user='myuser',
        password='mypassword',
        host='0.0.0.0',
        port='5432'
    )
    return conn

# print("ok mundo")
    
try:
    conn = get_db_connection()
    cursor = conn.cursor()

    df = pd.read_json("news.json")
    df_partial = df.head(20)
        
    for index, row in tqdm(df_partial.iterrows(), total=len(df_partial)):

        title = row['headline']
        author = row['authors']
        category = row['category']
        content = row['short_description']
        publication_date = generate_random_date()  # Generate a random publication date
        
        # Gerar a representação vetorial para o conteúdo
        vector_representation = convert_to_vector(content)

        # Inserir dados na tabela magazine_information
        insert_info_query = """
            INSERT INTO magazine_information (title, author, publication_date, category)
            VALUES (%s, %s, %s, %s)
            RETURNING id;  -- Retorna o ID do registro inserido
        """
        cursor.execute(insert_info_query, (title, author, publication_date, category))
        magazine_id = cursor.fetchone()[0]  # Obtém o ID do registro recém-inserido
        
        # Inserir os dados na tabela magazine_content
        insert_content_query = """
            INSERT INTO magazine_content (magazine_id, content, vector_representation)
            VALUES (%s, %s, %s)
        """
        cursor.execute(insert_content_query, (magazine_id, content, vector_representation))

    conn.commit()
    cursor.close()
    conn.close()
    print("Dados inseridos com sucesso!")
except Exception as e:
        print(str(e))
