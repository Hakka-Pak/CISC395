"""
Lab 08: Adding AI to Trip Notes — Setup
========================================
Run this script from your CISC395 workspace root AFTER completing Lab 07.

Usage (from CISC395/ root):
    python Labs/Lab08/setup.py

OR download and run:
    curl -o setup.py https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab08/setup.py
    python setup.py
"""

import os
import sys
import urllib.request

BASE_URL = "https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab08/"

# All files download into trip_notes/ (paths are relative to trip_notes/)
DOWNLOADS = [
    ("tests/check_api_setup.py",        "tests/check_api_setup.py"),
    ("tests/check_openrouter.py",       "tests/check_openrouter.py"),
    ("tests/check_gemini.py",           "tests/check_gemini.py"),
    ("tests/test_ai_assistant.py",      "tests/test_ai_assistant.py"),
    ("prompts/Lab08_Setup_menu.md",     "prompts/Lab08_Setup_menu.md"),
    ("prompts/Lab08_Ex01_assistant.md", "prompts/Lab08_Ex01_assistant.md"),
    ("prompts/Lab08_Ex03_menu.md",      "prompts/Lab08_Ex03_menu.md"),
    ("prompts/Lab08_Ex04_chaining.md",  "prompts/Lab08_Ex04_chaining.md"),
    ("prompts/Lab08_Ex04b_menu.md",     "prompts/Lab08_Ex04b_menu.md"),
]

def check_location():
    cwd = os.getcwd()
    if os.path.basename(cwd) in ("Lab08", "Labs"):
        print("WARNING: Run this from your CISC395 workspace root, not from inside Labs/.")
        print(f"  Current directory: {cwd}")
        print("  Try: cd ../.." if os.path.basename(cwd) == "Lab08" else "  Try: cd ..")
        print("  Then: python Labs/Lab08/setup.py")
        sys.exit(1)


def setup():
    check_location()

    root = "trip_notes"

    if not os.path.exists(root):
        print("ERROR: trip_notes/ not found.")
        print("Complete Lab 07 first to create the project, then run this setup.")
        sys.exit(1)

    print("Downloading Lab 08 files into trip_notes/...")
    print()

    # Ensure trip_notes/prompts/ and trip_notes/tests/ exist
    for d in ["prompts", "tests"]:
        os.makedirs(os.path.join(root, d), exist_ok=True)

    # Download files into trip_notes/
    print("Downloading...")
    failed = []
    for remote, local in DOWNLOADS:
        dest = os.path.join(root, local)
        url = BASE_URL + remote
        try:
            urllib.request.urlretrieve(url, dest)
            print(f"  \u2713  trip_notes/{local}")
        except Exception as e:
            print(f"  \u2717  trip_notes/{local}  ({e})")
            failed.append((dest, url))

    print()
    if failed:
        print("Some downloads failed. Retry manually:")
        for dest, url in failed:
            print(f"  curl -o {dest} {url}")
        print()

    print("Done! Lab 08 files downloaded to trip_notes/.")
    print()
    print("Next steps — follow Lab 08 Setup section in order:")
    print("  1. Create CISC395/.gitignore  →  git add + commit + push")
    print("  2. Create CISC395/.env with your API key")
    print("  3. Create CISC395/.venv (if not already done)  →  pip install  →  pip freeze")
    print("  4. cd trip_notes  (both terminals)")
    print("  5. python tests/check_api_setup.py")


def refresh():
    root = "trip_notes"
    if not os.path.exists(root):
        print("trip_notes/ not found. Run without --refresh first.")
        sys.exit(1)
    print("Refreshing Lab 08 files in trip_notes/...")
    for remote, local in DOWNLOADS:
        dest = os.path.join(root, local)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        url = BASE_URL + remote
        try:
            urllib.request.urlretrieve(url, dest)
            print(f"  \u2713  trip_notes/{local}")
        except Exception as e:
            print(f"  \u2717  {local}  ({e})")


if __name__ == "__main__":
    if "--refresh" in sys.argv:
        check_location()
        refresh()
    else:
        setup()
