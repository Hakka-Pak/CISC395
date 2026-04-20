# Lab 10: Adding Tools to Trip Notes — Function Calling + ReAct Agent

**Course:** CISC 395 Applied Generative AI and LLM Applications
**Week:** 11
**Points:** 100

---

## Overview

Your AI assistant can now chat and search documents. This week you give it **tools**: Python functions the AI can call when it needs to compute something or take an action. You will build a ReAct agent — the AI reasons about which tool to use, calls it, and reasons again until it can give a final answer.

**What changes in `trip_notes/` this week:**

```
trip_notes/
├── src/
│   ├── tools.py        ← NEW: 3 travel tools + run_agent()
│   ├── main.py         ← add option [10] AI Travel Agent
│   ├── rag.py          (unchanged — search_guides_tool calls it)
│   ├── ai_assistant.py (unchanged)
│   ├── models.py       (unchanged)
│   └── storage.py      (unchanged)
├── guides/
├── chroma_db/
└── requirements.txt    (no new packages needed)
```

**Three tool types you will build:**

| Tool | Type | What it does |
|------|------|--------------|
| `budget_breakdown` | Pure computation | Math — splits budget by category |
| `get_weather` | External HTTP API | Fetches real-time weather (no API key needed) |
| `search_guides_tool` | Internal system call | Searches your guides/ via rag.py |

---

## Setup

**From CISC395/ root (one line):**

```bash
mkdir -p Labs/Lab10 && curl -o Labs/Lab10/setup.py https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab10/setup.py && python Labs/Lab10/setup.py
```

> **Windows PowerShell:**
> ```powershell
> New-Item -ItemType Directory -Force -Path Labs\Lab10; Invoke-WebRequest -Uri https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab10/setup.py -OutFile Labs\Lab10\setup.py; python Labs\Lab10\setup.py
> ```

Then from **`trip_notes/`:**

```bash
cd trip_notes
python tests/check_progress.py --lab 10
```

Fix any red items before starting exercises.

---

## Exercises

---

### Exercise 1 — Build the Tools (30 pts)

Create `src/tools.py` with three travel tool functions that represent different tool types.

**AI (one line):**
```
# Option A — Gemini CLI / Claude Code
Please read and follow the instructions in @prompts/Lab10_Ex01_tools.md

# Option B — Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab10_Ex01_tools.md
```

**Run Terminal — test:**
```bash
python src/tools.py
```

**Paste your `src/tools.py`:**
```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import urllib.request
from src.rag import search_guides, ensure_index
from src.ai_assistant import client, MODEL

def budget_breakdown(destination: str, days: int, budget_usd: float) -> str:
    if days <= 0:
        return "Days must be greater than 0."
    
    daily = budget_usd / days
    acc = daily * 0.40
    food = daily * 0.30
    trans = daily * 0.15
    act = daily * 0.15
    
    return (f"{days}-day {destination} budget (${budget_usd:.2f} total)\n"
            f"Daily: ${daily:.2f}\n"
            f"  Accommodation : ${acc:.2f}\n"
            f"  Food          : ${food:.2f}\n"
            f"  Transport     : ${trans:.2f}\n"
            f"  Activities    : ${act:.2f}")

def get_weather(city: str) -> str:
    try:
        query_city = city.replace(" ", "+")
        url = f"https://wttr.in/{query_city}?format=j1"
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            current = data["current_condition"][0]
            temp_c = current["temp_C"]
            temp_f = current["temp_F"]
            desc = current["weatherDesc"][0]["value"]
            return f"{city}: {desc}, {temp_c}°C / {temp_f}°F"
    except Exception as e:
        return f"Could not fetch weather for {city}: {e}"

def search_guides_tool(query: str) -> str:
    ensure_index()
    chunks = search_guides(query, n_results=2)
    if not chunks:
        return "No relevant information found in guides."
    return "\n\n---\n\n".join(chunks)

def run_agent(user_question: str) -> str:
    messages = [
        {"role": "system", "content": "You are a travel planning agent. Use the available tools to help users plan trips. Always use a tool if it can answer the question more accurately — especially for real-time data or guide content."},
        {"role": "user", "content": user_question}
    ]
    for _ in range(5):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
            max_tokens=1024,
            timeout=30,
        )
        msg = response.choices[0].message
        
        if not msg.tool_calls:
            return msg.content
        
        for tc in msg.tool_calls:
            name = tc.function.name
            args = json.loads(tc.function.arguments)
            print(f"[Tool call] {name}({args})")
            
            if name == "budget_breakdown":
                result = budget_breakdown(**args)
            elif name == "get_weather":
                result = get_weather(**args)
            elif name == "search_guides_tool":
                result = search_guides_tool(**args)
            else:
                result = f"Unknown tool: {name}"
                
            print(f"[Tool result] {result[:120]}...")
            messages.append({"role": "assistant", "content": None, "tool_calls": [tc]})
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
            
    return "Agent reached maximum iterations."

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "budget_breakdown",
            "description": "Calculate a daily budget breakdown for a trip given destination, number of days, and total budget in USD",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {"type": "string", "description": "The destination name"},
                    "days": {"type": "integer", "description": "Number of days for the trip"},
                    "budget_usd": {"type": "number", "description": "Total budget in USD"}
                },
                "required": ["destination", "days", "budget_usd"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current real-time weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city name"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_guides_tool",
            "description": "Search the local travel guides for tips, recommendations, or information about a destination",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"]
            }
        }
    }
]

if __name__ == "__main__":
    print(budget_breakdown("Tokyo", 7, 1400.00))
    print(get_weather("Tokyo"))
    print(search_guides_tool("things to do in Tokyo"))
```

**Paste the test output:**
```
7-day Tokyo budget ($1400.00 total)
Daily: $200.00
  Accommodation : $80.00
  Food          : $60.00
  Transport     : $30.00
  Activities    : $30.00
Tokyo: Light rain shower, 19°C / 66°F
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Loading weights: 100%|█████████████████████| 103/103 [00:00<00:00, 3131.06it/s]
BertModel LOAD REPORT from: sentence-transformers/all-MiniLM-L6-v2
Key                     | Status     |  | 
------------------------+------------+--+-
embeddings.position_ids | UNEXPECTED |  | 

Notes:
- UNEXPECTED:   can be ignored when loading from different task/architecture; not ok if you expect identical arch.
Visiting Japan is a mesmerizing experience where ancient traditions seamlessly blend with futuristic innovation. The country is known for its meticulously organized society, bustling neon-lit cities, and serene landscapes, all underpinned by a culture of deep respect. The best season to visit is during the spring, from March to May, when the weather is mild and the iconic cherry blossoms are in full bloom, or during the autumn to see the vibrant red and gold foliage. When it comes to food, you must try authentic sushi at a local market, a steaming bowl of rich tonkotsu ramen, and savory okonomiyaki, an interactive and highly customizable grilled cabbage pancake. For activities, spend time exploring the historic temples and tranquil bamboo forests of Kyoto, experience the energetic sensory overload of Tokyo's Shibuya crossing, and take a day to relax in a traditional geothermal onsen. For a student traveler on a budget, here are two practical tips. First, take advantage of convenience stores like 7-Eleven or Lawson, which offer high-quality, delicious, and incredibly cheap meals. Second, getting around is easiest with a prepaid IC transit card, but always carry some physical cash since many smaller shops still do not accept credit cards.

---

giving of pretty sweets. 14-15 APRIL & 9-10 OCTOBER TAKAYAMA FESTIVAL Takayama City, Gifu Prefecture Intricately decorated floats ( yatai) are paraded through the streets of the city’s old town to celebrate spring or a good harvest in autumn. JNTO2020p14_15_seasons_V8_MR_F.indd 14JNTO2020p14_15_seasons_V8_MR_F.indd 14 26/10/20 9:56 am26/10/20 9:56 am Honshu Kyushu Okinawa Shikoku Hokkaido Sapporo Sapporo ramen (miso broth, butter, corn) Sakura (cherry blossom) Gassho-zukuri village Mt Fuji Maiko / Geiko Adachi Museum of Art Himeji Castle Ryukyu Buyo (traditional Okinawan dance) Seven Stars in Kyushu cruise train Shodoshima olive park Danjo Garan Temple Onsen (hot springs) Aomori Sendai NagoyaKyoto Hiroshima Fukuoka Hakone Koyasan Shirakawa-go Osaka Naha Tokyo Naoshima Himeji Yasugi Oita www.japan.travel/en/au A travel guide to Japan The LUXURY of EXPERIENCE ILLUSTRATION: MIKE ROSSI JNTO2020p16_map_V8_MR_F.indd 16JNTO2020p16_map_V8_MR_F.indd 16 26/10/20 9:57 am26/10/20 9:57 am
```

**Understanding check:** The three tools use three different approaches: pure math, an external HTTP API, and calling your own project's rag.py. What does this tell you about what a "tool" can be? Why is it better to separate these operations from the LLM instead of just asking the LLM directly? (3 sentences)

```
It tells me that a tool can be virtually any programmed set of logic or integration that returns text, from a simple scripted calculator to a complex retrieval or internet search loop. It’s better to separate these out instead of querying the LLM directly primarily because LLMs are not reliable native computers nor can they fetch real-time or proprietary data on their own natively; they only know patterns in their training data. By having the LLM interface with external tools, we provide the reasoning part natively, while offloading the fetching and arithmetic parts directly to robust APIs / algorithms respectively.
```

**Commit:**
```bash
git add src/tools.py
git commit -m "feat: travel tools (budget, weather, guides search)"
git push
```

---

### Exercise 2 — Build the ReAct Agent (35 pts)

Add `run_agent()` to `src/tools.py`. The agent reasons about which tool to use, calls it, sees the result, and continues until it can give a final answer.

**AI (one line):**
```
# Option A — Gemini CLI / Claude Code
Please read and follow the instructions in @prompts/Lab10_Ex02_agent.md

# Option B — Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab10_Ex02_agent.md
```

**Step 1 — Quick test (Run Terminal):**

```bash
python tests/test_agent.py
```

Type or paste a question when prompted. You should see `[Tool call]` and `[Tool result]` lines before the final answer — this confirms the ReAct loop is working.

```
[Paste output here]
```

**Step 2 — Test with 3 questions:**

Run `python tests/test_agent.py` again for each question below. Copy-paste the question at the prompt:

Test 1 (computation): `I have $1200 for 8 days in Tokyo. Break down my budget.`
```
=== Agent Test ===
The agent will show [Tool call] and [Tool result] as it works.

Your question: I have $1200 for 8 days in Tokyo. Break down my budget.

[Tool call] budget_breakdown({'budget_usd': 1200, 'days': 8, 'destination': 'Tokyo'})
[Tool result] 8-day Tokyo budget ($1200.00 total)
Daily: $150.00
  Accommodation : $60.00
  Food          : $45.00
  Transport     : $...

Agent answer:
Here's your detailed budget breakdown for an 8-day trip to Tokyo with a $1200 total budget:

**Daily Budget:** $150.00  
- **Accommodation:** $60.00/day (e.g., budget hotels/hostels)  
- **Food:** $45.00/day (mix of local street food, convenience stores, and mid-range meals)  
- **Transport:** $22.50/day (public transit passes or taxis)  
- **Activities:** $22.50/day (museums, temples, or free cultural sites)  

This is a recommended split to cover essentials while allowing flexibility. Would you like tips for optimizing specific categories (e.g., cheap eats, free activities) or adjust any allocations?
```

Test 2 (real-time data): `What's the weather like in Paris right now?`
```
=== Agent Test ===
The agent will show [Tool call] and [Tool result] as it works.

Your question: What's the weather like in Paris right now?

[Tool call] get_weather({'city': 'Paris'})
[Tool result] Paris: Cloudy, 9°C / 49°F...

Agent answer:
Right nowin Paris it’s cloudy with a temperature of 9 °C (49 °F).
```

Test 3 (two tools): `I'm planning a trip to Tokyo. Check the current weather and search my travel guides for things to do.`
```
=== Agent Test ===
The agent will show [Tool call] and [Tool result] as it works.

Your question: I'm planning a trip to Tokyo. Check the current weather and search my travel guides for things to do.

[Tool call] get_weather({'city': 'Tokyo'})
[Tool result] Tokyo: Light rain shower, 19°C / 66°F...
[Tool call] search_guides_tool({'query': 'things to do in Tokyo'})
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Loading weights: 100%|█████████████████████| 103/103 [00:00<00:00, 7764.72it/s]
BertModel LOAD REPORT from: sentence-transformers/all-MiniLM-L6-v2
Key                     | Status     |  | 
------------------------+------------+--+-
embeddings.position_ids | UNEXPECTED |  | 

Notes:
- UNEXPECTED:   can be ignored when loading from different task/architecture; not ok if you expect identical arch.
[Tool result] Visiting Japan is a mesmerizing experience where ancient traditions seamlessly blend with futuristic innovation. The cou...

Agent answer:
**Current Weather in Tokyo**

- **Condition:** Light rain shower  
- **Temperature:** 19 °C  (66 °F)  

**Things to Do in Tokyo (Based on Travel Guides)**  

| Category | Highlights | Why It’s Worth It |
|----------|------------|-------------------|
| **Iconic Landmarks** | • *Shibuya Crossing* – world‑famous intersection; <br>• *Meiji Shrine* – serene Shinto shrine in a forested park; <br>• *Tokyo Tower / Tokyo Skytree* – panoramic city views | Mix of vibrant city life and cultural heritage. |
| **Traditional Experience** | • *Asakusa & Senso‑ji Temple* – old‑town vibes, historic street markets; <br>• *Tsukiji Outer Market* – fresh seafood, Japanese street food | Taste Japan’s culinary roots and walk through centuries‑old streets. |
| **Modern & Pop Culture** | • *Akihabara* – electronics, anime, and gaming hub; <br>• *Harajuku & Omotesando* – fashion boutiques, quirky street style; <br>• *Ghibli Museum* (by appointment) | Immerse in Japan’s cutting‑edge pop culture. |
| **Parks & Relaxation** | • *Ueno Park* – cherry blossoms (if in season), museums, zoo; <br>• *Shinjuku Gyoen National Garden* – spacious lawns, seasonal flowers; <br>• *Odaiba Seaside Park* – waterfront, futuristic architecture | Balance the bustling city with greenery and calm. |
| **Shopping & Souvenirs** | • *Ginza* – upscale department stores, luxury brands; <br>• *Omotesando Hills* – modern design; <br>• *Nakamise Street (Senso‑ji)* – traditional snacks & souvenirs | Find everything from high‑end to traditional Japanese craft. |
| **Culinary Adventures** | • *Sushi at Tsukiji Outer Market*; <br>• *Ramen all‑night (Shin‑yoku or Ichiran)*; <br>• *Okonomiyaki in Okonomiyaki‑demo* | Sample authentic Japanese cuisine across the city. |
| **Special Experiences** | • *Night bus around Tokyo Bay* – see city lights from the water; <br>• *Sumo practice (if free viewing, e.g., Ryogoku Kokugikan)* | Unique glimpses of Japanese traditions. |
| **Practical Tips (for a budget traveler)** | • Use convenience stores (7‑Eleven, Lawson) for quick meals<br>• Pre‑purchased IC cards (Suica/Pasmo) for transit <br>• Keep some cash — many smaller spots don’t accept cards | Keeps costs down while still enjoying key sights. |

---

**Quick Plan for a 3‑day Stay**

1. **Day 1** – Morning: Asakusa + Senso‑ji; Lunch at Tsukiji Market; Afternoon: Hamarikyu Gardens; Night: Kabuki‑theater or explore Shibuya crossing and Harajuku.  
2. **Day 2** – Morning: Meiji Shrine; Mid‑day: Omotesando & Harajuku; Lunch at a themed café; Afternoon: Akihabara; Evening: Ramen marathon in Shinjuku.  
3. **Day 3** – Morning: Tokyo Skytree & Sumida Aquarium; Lunch at a sushi spot; Afternoon: Ueno Park (museums or zoo) or a stroll through Yanaka‑Gyoen; Evening: Odaiba waterfront cruise and light show.

Enjoy your trip! Let me know if you’d like restaurant recommendations, transit routes, or any other details.
```

**Understanding check:** In Test 3, the agent called two different tool types (HTTP API + local guide search). Why couldn't the LLM answer both parts of that question without tools? (2–3 sentences)

```
The LLM couldn't answer the question without tools because it doesn't have access to real-time data like current weather, and it doesn't know the exact content of local proprietary guides unless we retrieve and feed them into the prompt. Without the HTTP weather tool, it would hallucinate a guess at the weather based on historical averages rather than knowing it right now. Without the local guide search tool, it would hallucinate recommendations from its pre-training rather than returning our personalized data.
```

**Commit:**
```bash
git add src/tools.py tests/test_agent.py
git commit -m "feat: react agent with tool calling"
git push
```

---

### Exercise 3 — Add Agent to the Menu (20 pts)

Add menu option `[10] AI Travel Agent` to `main.py`.

**AI (one line):**
```
# Option A — Gemini CLI / Claude Code
Please read and follow the instructions in @prompts/Lab10_Ex03_menu.md

# Option B — Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab10_Ex03_menu.md
```

**Paste the `[10]` handler from `main.py`:**
```python
[Paste here]
```

**Paste a test session with one compound question:**
```
[Paste terminal output]
```

**Commit:**
```bash
git add src/main.py
git commit -m "feat: add agent to menu [10]"
git push
```

---

### Reflection (15 pts)

**1.** Compare options `[6]`, `[8]`, and `[10]` in your menu. For each, describe a travel question where it is the **best** choice and explain why. (6–8 sentences total)

```
[6] Ask AI:           best for...

[8] Search my guides: best for...

[10] AI Travel Agent: best for...
```

**2.** The `get_weather` tool calls a real external API. Why is it better to have the agent call this tool rather than just asking the LLM "what's the weather in Tokyo?" directly? What category of problem does this solve? (3 sentences)

```
[Your answer]
```

---

## Grading Rubric

| Exercise | Criteria | Points |
|----------|---------|--------|
| Ex 1: tools.py | All 3 functions work (budget, weather, guides search), TOOL_DEFINITIONS defined, output pasted | 30 |
| Ex 2: run_agent() | Agent loop works, 3 test outputs pasted incl. two-tool question | 35 |
| Ex 3: Menu [10] | Works in app, test session pasted, commit present | 20 |
| Reflection | Both questions answered with substance | 15 |

---

## Quick Reference

**OpenAI tool calling format:**

```python
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=TOOL_DEFINITIONS,
    tool_choice="auto",
    max_tokens=1024,
    timeout=30,
)
msg = response.choices[0].message

if msg.tool_calls:
    for tc in msg.tool_calls:
        name = tc.function.name
        args = json.loads(tc.function.arguments)
        result = your_function(**args)
        messages.append({"role": "assistant", "content": None, "tool_calls": [tc]})
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
```

**Tool definition format:**

```python
# Example: a tool that calls an external API
{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current real-time weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"},
            },
            "required": ["city"],
        },
    },
}
```

The LLM reads the `description` field to decide when to call each tool. Write clear descriptions.

**Next lab:** Lab 11 replaces the CLI menu with a Streamlit web interface. All the code from Labs 07–10 will be reused — you are just changing how users interact with it.
