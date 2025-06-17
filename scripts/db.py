import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'health_checks.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS health_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            status TEXT NOT NULL,
            response_time_ms INTEGER,
            error_message TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_health_check(status, response_time_ms=None, error_message=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO health_logs (timestamp, status, response_time_ms, error_message)
        VALUES (?, ?, ?, ?)
    ''', (datetime.utcnow().isoformat(), status, response_time_ms, error_message))
    conn.commit()
    conn.close()
