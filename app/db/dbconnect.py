import psycopg2
import numpy as np

from app.db.dbconfig import get_db_connection

def create_db_connection():
    try:
        return get_db_connection()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting", error)
    return None