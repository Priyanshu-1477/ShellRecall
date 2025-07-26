# shellrecall.py

import os
import sys
from db import init_db, log_command
from datetime import datetime

def extract_tags(command: str) -> list[str]:
    """Extract tags from the command, e.g., #deploy, #test"""
    return [word[1:] for word in command.split() if word.startswith("#") and len(word) > 1]

def main():
    init_db()
    
    command = os.environ.get("SHELLRECALL_CMD")
    exit_code = int(os.environ.get("SHELLRECALL_EXIT", 0))
    cwd = os.getcwd()
    timestamp = datetime.now().isoformat()
    
    if command:
        command = command.strip()
        tags = extract_tags(command)
        log_command(command, cwd, timestamp, exit_code, tags)

if __name__ == "__main__":
    main()
