# recall-tags.py

import argparse
from query import get_all_tags
import difflib

def main():
    parser = argparse.ArgumentParser(description="🔖 Suggest or list tags used in ShellRecall.")
    parser.add_argument("partial", nargs="?", help="Partial tag to match (optional)")

    args = parser.parse_args()
    all_tags = get_all_tags()

    if args.partial:
        matches = difflib.get_close_matches(args.partial, all_tags, n=10, cutoff=0.3)
        if matches:
            print("🔎 Suggested tags:")
            for tag in matches:
                print(f"  - {tag}")
        else:
            print("❌ No matching tags found.")
    else:
        print("📦 All tags:")
        for tag in sorted(all_tags):
            print(f"  - {tag}")

if __name__ == "__main__":
    main()
