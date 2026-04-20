I am extending a Python CLI project called Trip Notes (run from trip_notes/).

Create src/tools.py with three travel tool functions that demonstrate different tool types.

---

1. budget_breakdown(destination: str, days: int, budget_usd: float) -> str
   Type: Pure computation (no external calls)
   Calculates a daily budget breakdown:
   - accommodation: 40% of daily budget
   - food: 30% of daily budget
   - transport: 15% of daily budget
   - activities: 15% of daily budget
   Returns a formatted multi-line string.
   Example output:
     7-day Tokyo budget ($1400.00 total)
     Daily: $200.00
       Accommodation : $80.00
       Food          : $60.00
       Transport     : $30.00
       Activities    : $30.00

---

2. get_weather(city: str) -> str
   Type: External HTTP API call (no API key required)
   Fetches current weather from https://wttr.in/{city}?format=j1 using urllib.request (standard library, no pip install).
   Parse:
   - data["current_condition"][0]["temp_C"]
   - data["current_condition"][0]["temp_F"]
   - data["current_condition"][0]["weatherDesc"][0]["value"]
   Return: "{city}: {description}, {temp_c}°C / {temp_f}°F"
   On any exception: return "Could not fetch weather for {city}: {error}"
   Use timeout=5 for the request.
   Replace spaces in city name with + in the URL.

---

3. search_guides_tool(query: str) -> str
   Type: Internal system call (uses this project's own rag.py)
   Import: from src.rag import search_guides, ensure_index
   Call ensure_index() first, then search_guides(query, n_results=2).
   Join chunks with "\n\n---\n\n".
   If no chunks returned: return "No relevant information found in guides."

---

Also define TOOL_DEFINITIONS: a list of 3 dicts in OpenAI function-calling format.
Each dict has: type="function", function={name, description, parameters (JSON Schema)}.
Mark all parameters as required.
Add a clear description for each tool so the LLM knows when to use it:
- budget_breakdown: "Calculate a daily budget breakdown for a trip given destination, number of days, and total budget in USD"
- get_weather: "Get the current real-time weather for a city"
- search_guides_tool: "Search the local travel guides for tips, recommendations, or information about a destination"

---

Imports needed at the top of the file (in this exact order):
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import urllib.request
from src.rag import search_guides, ensure_index

---

Under if __name__ == "__main__": test all three functions with sample inputs and print results.
Use Tokyo for budget_breakdown and get_weather.
Use "things to do in Tokyo" for search_guides_tool.

Write the file directly to src/tools.py.
