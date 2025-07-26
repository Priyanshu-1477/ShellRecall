# query.py

import sqlite3
from typing import Optional, List, Tuple
from datetime import datetime
from pathlib import Path
import difflib

DB_PATH = Path.home() / "ShellRecall" / "shellrecall.db"

def get_all_tags() -> List[str]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM tags")
    tags = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tags

def fuzzy_match_tags(input_tags: List[str], existing_tags: List[str]) -> List[str]:
    matched_tags = []
    for tag in input_tags:
        matches = difflib.get_close_matches(tag, existing_tags, n=1, cutoff=0.6)
        if matches:
            matched_tags.append(matches[0])
    return matched_tags

def search_commands(
    keyword: Optional[str] = None,
    cwd: Optional[bool] = False,
    since: Optional[str] = None,
    until: Optional[str] = None,
    limit: int = 20,
    tags: Optional[List[str]] = None
) -> List[Tuple]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Base query
    query = """
        SELECT DISTINCT commands.id, commands.timestamp, commands.command, commands.cwd,
                        GROUP_CONCAT(tags.name, ', ') as tag_list
        FROM commands
        LEFT JOIN command_tags ON commands.id = command_tags.command_id
        LEFT JOIN tags ON command_tags.tag_id = tags.id
        WHERE 1=1
    """
    params = []

    if keyword:
        query += " AND REPLACE(commands.command, '\n', ' ') LIKE ?"
        params.append(f"%{keyword}%")

    if cwd:
        current_dir = str(Path.cwd())
        query += " AND commands.cwd = ?"
        params.append(current_dir)

    if since:
        query += " AND commands.timestamp >= ?"
        params.append(since)

    if until:
        query += " AND commands.timestamp <= ?"
        params.append(until)

    if tags:
        existing_tags = get_all_tags()
        matched_tags = fuzzy_match_tags(tags, existing_tags)
        if matched_tags:
            tag_placeholders = ",".join("?" for _ in matched_tags)
            query += f"""
                AND commands.id IN (
                    SELECT command_id FROM command_tags
                    JOIN tags ON tags.id = command_tags.tag_id
                    WHERE tags.name IN ({tag_placeholders})
                    GROUP BY command_id
                )
            """
            params.extend(matched_tags)

    query += " GROUP BY commands.id ORDER BY commands.timestamp DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results
