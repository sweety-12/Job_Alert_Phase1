import sqlite3
import os

# Database file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "preferences.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create preferences table if not exists."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_role TEXT NOT NULL,
            location TEXT NOT NULL,
            experience INTEGER,
            work_mode TEXT,
            email TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
