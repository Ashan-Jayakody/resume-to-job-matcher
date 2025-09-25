import os
from dotenv import load_dotenv
import psycopg2

load_dotenv() # load variables from .env

def get_db_connection():
    return psycopg2.connect(
        host = os.environ['DB_HOST'],
        database = os.environ['DB_NAME'],
        user = os.environ['DB_USER'],
        password = os.environ['DB_PASSWORD'],
        port = os.environ.get('DB_PORT', 5432)
    )