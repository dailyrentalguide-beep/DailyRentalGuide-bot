"""
=========================================
RG AI Database Engine
=========================================
Handles all SQLite operations: users, activation codes,
consultations, knowledge, logs.
=========================================
"""

import os
import sqlite3
from datetime import datetime, timedelta

from config import DATABASE_PATH

FREE_TRIAL_DAYS = 7


class Database:

    def __init__(self):
        # Make sure the database folder exists before connecting
        folder = os.path.dirname(DATABASE_PATH)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        # check_same_thread=False because python-telegram-bot may
        # touch this connection from different async tasks
        self.connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    # ==========================================================
    # Tables
    # ==========================================================

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id TEXT UNIQUE,
            username TEXT,
            first_name TEXT,
            activation_code TEXT,
            is_active INTEGER DEFAULT 0,
            subscription TEXT DEFAULT 'FREE',
            consultation_start TIMESTAMP,
            consultation_end TIMESTAMP,
            consultations_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_seen TIMESTAMP
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS activation_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            used INTEGER DEFAULT 0,
            used_by TEXT,
            subscription_type TEXT DEFAULT 'FREE',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            used_at TIMESTAMP
        )
        """)

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

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS unknown_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            asked_count INTEGER DEFAULT 1,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id TEXT,
            question TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.connection.commit()

    # ==========================================================
    # Users
    # ==========================================================

    def get_user(self, telegram_id):
        self.cursor.execute(
            "SELECT * FROM users WHERE telegram_id = ?", (str(telegram_id),)
        )
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def create_user(self, telegram_id, username, first_name):
        existing = self.get_user(telegram_id)
        if existing:
            return existing

        self.cursor.execute(
            """
            INSERT INTO users (telegram_id, username, first_name, last_seen)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (str(telegram_id), username, first_name),
        )
        self.connection.commit()
        self.log(f"New user created: {telegram_id}")
        return self.get_user(telegram_id)

    def update_last_seen(self, telegram_id):
        self.cursor.execute(
            "UPDATE users SET last_seen = CURRENT_TIMESTAMP WHERE telegram_id = ?",
            (str(telegram_id),),
        )
        self.connection.commit()

    def activate_user(self, telegram_id, code, subscription_type="FREE"):
        self.cursor.execute(
            """
            UPDATE users
            SET is_active = 1, activation_code = ?, subscription = ?
            WHERE telegram_id = ?
            """,
            (code, subscription_type, str(telegram_id)),
        )
        self.connection.commit()
        self.log(f"User activated: {telegram_id} with code {code}")

    def start_consultation_period(self, telegram_id):
        """Starts the 7-day free support window on the FIRST question,
        not at purchase/activation time. Safe to call every time —
        only sets the window if it hasn't been set yet."""

        user = self.get_user(telegram_id)
        if not user or user["consultation_start"]:
            return

        start = datetime.now()
        end = start + timedelta(days=FREE_TRIAL_DAYS)

        self.cursor.execute(
            """
            UPDATE users
            SET consultation_start = ?, consultation_end = ?
            WHERE telegram_id = ?
            """,
            (start.isoformat(), end.isoformat(), str(telegram_id)),
        )
        self.connection.commit()

    def is_subscription_valid(self, telegram_id):
        """Starts the trial window if needed, then checks if the user
        is still within it. Returns True/False."""

        self.start_consultation_period(telegram_id)
        user = self.get_user(telegram_id)

        if not user or not user["consultation_end"]:
            return True  # safety fallback, shouldn't normally happen

        end = datetime.fromisoformat(user["consultation_end"])
        return datetime.now() <= end

    def increment_consultations(self, telegram_id):
        self.cursor.execute(
            """
            UPDATE users
            SET consultations_count = consultations_count + 1
            WHERE telegram_id = ?
            """,
            (str(telegram_id),),
        )
        self.connection.commit()

    # ==========================================================
    # Activation Codes
    # ==========================================================

    def add_code(self, code, subscription_type="FREE"):
        self.cursor.execute(
            "INSERT OR IGNORE INTO activation_codes (code, subscription_type) VALUES (?, ?)",
            (code, subscription_type),
        )
        self.connection.commit()

    def verify_code(self, code):
        self.cursor.execute(
            "SELECT * FROM activation_codes WHERE code = ?", (code,)
        )
        row = self.cursor.fetchone()

        if not row:
            return {"success": False, "message": "الكود غير صحيح."}

        if row["used"]:
            return {"success": False, "message": "الكود مستخدم مسبقًا."}

        return {"success": True, "data": dict(row)}

    def use_code(self, code, telegram_id):
        self.cursor.execute(
            """
            UPDATE activation_codes
            SET used = 1, used_by = ?, used_at = CURRENT_TIMESTAMP
            WHERE code = ?
            """,
            (str(telegram_id), code),
        )
        self.connection.commit()

    # ==========================================================
    # Consultations
    # ==========================================================

    def save_consultation(self, telegram_id, question):
        self.cursor.execute(
            "INSERT INTO consultations (telegram_id, question) VALUES (?, ?)",
            (str(telegram_id), question),
        )
        self.connection.commit()
        self.increment_consultations(telegram_id)

    # ==========================================================
    # Logs
    # ==========================================================

    def log(self, action):
        self.cursor.execute(
            "INSERT INTO logs (action) VALUES (?)", (action,)
        )
        self.connection.commit()


db = Database()
db.create_tables()
