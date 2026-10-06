import sqlite3
from pathlib import Path
from src.config import config

def ensure_db():
    db_path = Path(config.DATABASE_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE,
            title TEXT,
            status TEXT DEFAULT 'created',
            video_path TEXT,
            youtube_id TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn

def save_video_record(date_text, title, video_path, status='created'):
    conn = ensure_db()
    conn.execute(
        "INSERT OR REPLACE INTO videos (date, title, status, video_path) VALUES (?, ?, ?, ?)",
        (date_text, title, status, video_path),
    )
    conn.commit()
    conn.close()
