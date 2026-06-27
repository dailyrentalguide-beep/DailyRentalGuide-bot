"""
=========================================
RG AI Database Engine
=========================================
Handles all SQLite operations.
"""

import sqlite3
from config import DATABASE_PATH


class Database:

    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.connection.cursor()

    def create_tables(self):

        # Users
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            telegram_id TEXT UNIQUE,

            username TEXT,

            first_name TEXT,

            activation_code TEXT,

            is_active INTEGER DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            last_seen TIMESTAMP
        )
        """)

        # Knowledge
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            question TEXT,

            answer TEXT,

            category TEXT,

            source TEXT,

            version INTEGER DEFAULT 1,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Unknown Questions
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS unknown_questions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            question TEXT,

            asked_count INTEGER DEFAULT 1,

            status TEXT DEFAULT 'Pending',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Consultations
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            telegram_id TEXT,

            question TEXT,

            status TEXT DEFAULT 'Pending',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Logs
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            action TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.connection.commit()


db = Database()

db.create_tables()
