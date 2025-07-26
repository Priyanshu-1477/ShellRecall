import argparse
from query import search_commands

def main():
    parser = argparse.ArgumentParser(description="🔍 Search your shell command history.")
    
    parser.add_argument("-k", "--keyword", help="Keyword to search for in commands")
    parser.add_argument("-c", "--cwd", action="store_true", help="Filter by current working directory")
    parser.add_argument("-s", "--since", help="Start date (YYYY-MM-DD or ISO)")
    parser.add_argument("-u", "--until", help="End date (YYYY-MM-DD or ISO)")
    parser.add_argument("-l", "--limit", type=int, default=20, help="Limit number of results")
    parser.add_argument("-t", "--tags", nargs="+", help="Search by one or more tags")

    args = parser.parse_args()

    results = search_commands(
        keyword=args.keyword,
        cwd=args.cwd,
        since=args.since,
        until=args.until,
        limit=args.limit,
        tags=args.tags
    )

    if results:
        for row in results:
            id, timestamp, command, cwd, tags = row
            tag_str = f"[Tags: {tags}]" if tags else ""
            command_display = command.replace("\n", " && ")
            print(f"[{timestamp}] {command_display} ({cwd}) {tag_str}")
    else:
        print("No results found.")

if __name__ == "__main__":
    main()
