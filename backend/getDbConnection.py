import os
from dotenv import load_dotenv
import psycopg2

load_dotenv() # load variables from .env

def get_db_connection():

    postgres_url = os.environ.get('POSTGRES_URL')
    
    if postgres_url:
        print("Connecting using POSTGRES_URL")
        return psycopg2.connect(postgres_url)
    