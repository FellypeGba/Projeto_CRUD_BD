import psycopg2
import psycopg2.extras

DB_CONFIG = {
    "dbname": "crud_flask",
    "user": "postgres",
    "password": "senha",
    "host": "localhost",
    "port": 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)
