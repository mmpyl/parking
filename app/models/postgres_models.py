# Simple wrappers for postgres models - use lib.database.db to run queries.
from lib.database import db
from datetime import datetime, timedelta

class UserModel:
    @staticmethod
    def create_table():
        query = '''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(80) UNIQUE NOT NULL,
            email VARCHAR(120),
            password_hash VARCHAR(255),
            full_name VARCHAR(120),
            role VARCHAR(20) DEFAULT 'operator',
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )'''
        db.execute(query)