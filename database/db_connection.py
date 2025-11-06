import psycopg2
import os
from dotenv import load_dotenv
import psycopg2
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env (solo en local)
load_dotenv()

def get_db_connection():
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        return connection
    except Exception as e:
        print(" Error al conectar con la base de datos:", e)
        return None
