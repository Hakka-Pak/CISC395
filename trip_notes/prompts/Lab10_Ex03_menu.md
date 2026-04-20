In my Trip Notes project (run from trip_notes/):

src/main.py already has a grouped menu:
  -- Data --   [1] Add  [2] View all  [3] Search by country  [4] Add note
  -- AI --     [6] Ask AI  [7] Trip Briefing  [8] Search guides
  [R] Rebuild search index
  [Q] Quit

src/tools.py has run_agent(user_question: str) -> str

Add option [10] AI Travel Agent to the -- AI -- section of src/main.py:

1. Add to imports:
   from src.tools import run_agent

2. Add "[10] AI Travel Agent" to the -- AI -- section of the menu display.

3. Handler for choice "10":
   a. Print: "The agent can calculate budgets, check real-time weather, and search your travel guides."
   b. Input: "Your question: "
   c. Print: "\nThinking...\n"
   d. Call run_agent(question) — tool call traces will print automatically
   e. If result is None: print an error message and continue
   f. Print: "\nAgent answer:\n" + result
   g. Ask: "Save this as a note on a trip? (y/n): "
   h. If "y": same save-to-trip logic as option [6]

Write the updated file directly to src/main.py.
