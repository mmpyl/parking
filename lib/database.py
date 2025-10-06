import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

class Database:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.connection_string = os.environ.get('POSTGRES_URL')
        if not self.connection_string:
            # allow local env variables as fallback (optional)
            self.connection_string = os.environ.get('DATABASE_URL')
        self._initialized = True

    @contextmanager
    def get_connection(self):
        conn = psycopg2.connect(self.connection_string, cursor_factory=RealDictCursor)
        try:
            yield conn
            conn.commit()
        except:
            conn.rollback()
            raise
        finally:
            conn.close()

    def execute(self, query, params=None):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                if query.strip().upper().startswith('SELECT'):
                    return cur.fetchall()
                return cur.rowcount

    def execute_one(self, query, params=None):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                return cur.fetchone()

db = Database()