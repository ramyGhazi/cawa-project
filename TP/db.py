import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Load database config from environment or use defaults
DB_HOST     = os.getenv('DB_HOST', 'localhost')
DB_PORT     = os.getenv('DB_PORT', '5432')
DB_NAME     = os.getenv('DB_NAME', 'bibliotheque')
DB_USER     = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')

def get_db_connection():
    """
    Establishes a new database connection and returns it.
    """
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print(f"[INFO] Connected to database '{DB_NAME}' at {DB_HOST}:{DB_PORT}")
        return conn
    except Exception as e:
        print(f"[ERROR] Failed to connect to database: {e}")
        raise
