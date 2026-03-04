import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("POSTGRES_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)