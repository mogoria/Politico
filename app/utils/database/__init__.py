import psycopg2
import os


def db_con(db_url=None):
    
    if not db_url:
        db_url = os.getenv('DB_URL')

    con = psycopg2.connect(db_url)
    return con