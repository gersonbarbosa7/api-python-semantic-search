import psycopg2

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