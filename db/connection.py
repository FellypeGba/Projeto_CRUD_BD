import psycopg2
import psycopg2.extras

DB_CONFIG = {
  "dbname": "storeF1",
  "user": "postgres",
  "password": "senha", #projetobd
  "host": "localhost",
  "port": 5432
}

def get_connection():
  return psycopg2.connect(**DB_CONFIG)
