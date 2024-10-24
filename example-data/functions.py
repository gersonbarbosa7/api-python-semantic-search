import psycopg2
import numpy as np
import pandas as pd
from tqdm import tqdm
from datetime import datetime, timedelta
import random
from sentence_transformers import SentenceTransformer
import time

# Load a pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Você pode escolher outro modelo se preferir

def convert_to_vector(query):
    # Convert your query to a vector using the loaded model
    vector = model.encode(query)  # The encode method converts the string into a vector
    return vector.tolist()  # Returns as list if necessary

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

def install_data_base():
    conn = get_db_connection()

    sql_file = 'init.sql'

    with open(sql_file, 'r') as file:
        sql_commands = file.read()

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_commands)
            conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def check_db_exists():
    conn = get_db_connection()

    sql_file = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE  table_schema = 'public'
            AND    table_name  IN ('magazine_information', 'magazine_content')
        );
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_file)
            conn.commit()
            res = cursor.fetchall()
            if res:  # Ensure there are results
                columns = [desc[0] for desc in cursor.description]  # Get the column names
                results = [dict(zip(columns, row)) for row in res]
            else:
                results = []

            return results[0]['exists']
    except Exception as e:
        return False
    finally:
        conn.close()

def import_data_from_json(qty):
    conn = get_db_connection()
    cursor = conn.cursor()

    df = pd.read_json("news.json")
    df_to_process = df.head(qty)
        
    for index, row in tqdm(df_to_process.iterrows(), total=len(df_to_process)):

        try:
            title = row['headline']
            author = row['authors']
            category = row['category']
            content = row['short_description']
            publication_date = generate_random_date()  # Generate a random publication date
            
            # Generate the vector representation for the content
            vector_representation = convert_to_vector(content)

            # Insert data into the magazine_information table
            insert_info_query = """
                INSERT INTO magazine_information (title, author, publication_date, category)
                VALUES (%s, %s, %s, %s)
                RETURNING id;  -- Retorna o ID do registro inserido
            """
            cursor.execute(insert_info_query, (title, author, publication_date, category))
            magazine_id = cursor.fetchone()[0]  # Gets the ID of the newly inserted record
            
            # Insert data into the magazine_content table
            insert_content_query = """
                INSERT INTO magazine_content (magazine_id, content, vector_representation)
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_content_query, (magazine_id, content, vector_representation))

            conn.commit()
            
        except Exception as e:
            print("*******")
            print("")
            print("Error to import row")
            print(str(e))
            print(row)
            print("")
            print("*******")

    cursor.close()
    conn.close()
    print("Dados inseridos com sucesso!")

def start(qty):
    try:
        check_db = check_db_exists()
        if(check_db == False):
            install_data_base()
            time.sleep(5)
            import_data_from_json(qty=qty)
        else: 
            import_data_from_json(qty=qty)
    except Exception as e:
            print(str(e))