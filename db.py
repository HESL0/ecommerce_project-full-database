import psycopg
import os
from dotenv import load_dotenv 

load_dotenv()

def get_connection():
    connection = psycopg.connect(
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        port = os.getenv("DB_PORT"),
        host = os.getenv("DB_HOST")
    )
    return connection