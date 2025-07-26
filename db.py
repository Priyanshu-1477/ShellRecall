# db.py

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path.home() / "ShellRecall" / "shellrecall.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Main commands table
    c.execute("""
        CREATE TABLE IF NOT EXISTS commands(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT NOT NULL,
            cwd TEXT,
            timestamp TEXT,
            exit_code INTEGER
        );
    """)

    # Tags table
    c.execute("""
        CREATE TABLE IF NOT EXISTS tags(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
    """)

    # Many-to-many relationship table
    c.execute("""
        CREATE TABLE IF NOT EXISTS command_tags(
            command_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY (command_id) REFERENCES commands(id),
            FOREIGN KEY (tag_id) REFERENCES tags(id),
            PRIMARY KEY (command_id, tag_id)
        );
    """)

    conn.commit()
    conn.close()

def log_command(command, cwd, timestamp, exit_code, tags=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Insert command
    c.execute("""
        INSERT INTO commands (command, cwd, timestamp, exit_code)
        VALUES (?, ?, ?, ?)
    """, (command, cwd, timestamp, exit_code))
    command_id = c.lastrowid

    # Insert tags
    if tags:
        for tag in tags:
            c.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag,))
            c.execute("SELECT id FROM tags WHERE name = ?", (tag,))
            tag_id = c.fetchone()[0]
            c.execute("INSERT OR IGNORE INTO command_tags (command_id, tag_id) VALUES (?, ?)",
                      (command_id, tag_id))

    conn.commit()
    conn.close()
