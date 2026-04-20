"""
Lab 10: Function Calling + ReAct Agent — Setup
===============================================
Run this script from your CISC395 workspace root AFTER completing Lab 09.

Usage (from CISC395/ root):
    mkdir -p Labs/Lab10 && curl -o Labs/Lab10/setup.py https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab10/setup.py && python Labs/Lab10/setup.py
"""

import os
import sys
import urllib.request

BASE_URL   = "https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab10/"
SHARED_URL = "https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/shared/"
ZIP_URL    = "https://github.com/tisage/CISC395/archive/refs/heads/main.zip"


def download_file(url, dest):
    """Download a file and verify it is not empty or an HTML error page."""
    try:
        urllib.request.urlretrieve(url, dest)
    except Exception as e:
        return False, str(e)

    if os.path.getsize(dest) == 0:
        os.remove(dest)
        return False, "empty file (server returned nothing)"

    try:
        with open(dest, "r", errors="ignore") as f:
            first = f.read(80).lstrip()
        if first.startswith("<"):
            os.remove(dest)
            return False, "blocked by network (received HTML instead of file)"
    except Exception:
        pass

    return True, None


DOWNLOADS = [
    ("prompts/Lab10_Ex01_tools.md",  "prompts/Lab10_Ex01_tools.md"),
    ("prompts/Lab10_Ex02_agent.md",  "prompts/Lab10_Ex02_agent.md"),
    ("prompts/Lab10_Ex03_menu.md",   "prompts/Lab10_Ex03_menu.md"),
    ("tests/test_agent.py",          "tests/test_agent.py"),
]

SHARED_DOWNLOADS = [
    ("check_progress.py", "tests/check_progress.py"),
]


def check_location():
    cwd = os.getcwd()
    if os.path.basename(cwd) in ("Lab10", "Labs"):
        print("WARNING: Run this from your CISC395 workspace root, not from inside Labs/.")
        print(f"  Current directory: {cwd}")
        print("  Try: cd ../.." if os.path.basename(cwd) == "Lab10" else "  Try: cd ..")
        print("  Then: python Labs/Lab10/setup.py")
        sys.exit(1)


def setup():
    check_location()

    root = "trip_notes"
    if not os.path.exists(root):
        print("ERROR: trip_notes/ not found.")
        print("Complete Lab 07 first to create the project, then run this setup.")
        sys.exit(1)

    if not os.path.exists(os.path.join(root, "src", "rag.py")):
        print("WARNING: src/rag.py not found — Lab 09 may not be complete.")
        print("You can continue but complete Lab 09 exercises first.")
        print()

    print("Setting up Lab 10 in trip_notes/...")
    print()

    for d in ["prompts", "tests"]:
        os.makedirs(os.path.join(root, d), exist_ok=True)

    print("Downloading...")
    failed = []
    all_downloads = [(BASE_URL + r, l) for r, l in DOWNLOADS] + \
                    [(SHARED_URL + r, l) for r, l in SHARED_DOWNLOADS]

    for url, local in all_downloads:
        dest = os.path.join(root, local)
        ok, reason = download_file(url, dest)
        if ok:
            print(f"  \u2713  trip_notes/{local}")
        else:
            print(f"  \u2717  trip_notes/{local}  ({reason})")
            failed.append(local)

    print()
    if failed:
        print(f"  {len(failed)} file(s) failed to download:")
        for f in failed:
            print(f"    - trip_notes/{f}")
        print()
        print("  Fix: Download the ZIP and copy the missing files manually:")
        print(f"    {ZIP_URL}")
        print()

    print("Done! Lab 10 files ready in trip_notes/.")
    print()
    print("Next steps:")
    print("  1. cd trip_notes")
    print("  2. python tests/check_progress.py --lab 10")
    print("  3. Follow Lab 10 exercises in order")


def refresh():
    root = "trip_notes"
    if not os.path.exists(root):
        print("trip_notes/ not found. Run without --refresh first.")
        sys.exit(1)
    print("Refreshing Lab 10 files...")
    all_downloads = [(BASE_URL + r, l) for r, l in DOWNLOADS] + \
                    [(SHARED_URL + r, l) for r, l in SHARED_DOWNLOADS]
    for url, local in all_downloads:
        dest = os.path.join(root, local)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        ok, reason = download_file(url, dest)
        if ok:
            print(f"  \u2713  trip_notes/{local}")
        else:
            print(f"  \u2717  {local}  ({reason})")


if __name__ == "__main__":
    if "--refresh" in sys.argv:
        check_location()
        refresh()
    else:
        setup()
