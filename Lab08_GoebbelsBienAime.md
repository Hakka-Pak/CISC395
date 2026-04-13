# Lab 08: Adding AI to Trip Notes — API Programming Foundations

**Course:** CISC 395 Applied Generative AI and LLM Applications
**Week:** 9
**Points:** 100

---

## Overview

In Lab 07 you built a working CLI app entirely offline. This week you add the first AI feature: a travel assistant powered by a real language model.

**What changes in `trip_notes/` this week:**

```
trip_notes/
├── src/
│   ├── ai_assistant.py  ← NEW: API client + ask() function
│   ├── main.py          ← polish menu (Q key + grouping), add [6] Ask AI, [7] Briefing
│   ├── models.py        (unchanged)
│   └── storage.py       (unchanged)
├── .env                 ← NEW: your API key (never commit this)
├── .gitignore           ← NEW: protects .env and .venv
├── requirements.txt     ← updated: openai, python-dotenv
└── ...
```

**AI tool:** Use Gemini CLI, GitHub Copilot, Claude Code, or any terminal AI. All exercises use `@prompts/` files — no copy-paste needed.

---

## Setup

Run from your **CISC395 root** to download prompt files and the test file:

```bash
mkdir -p Labs/Lab08
curl -o Labs/Lab08/setup.py https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab08/setup.py
python Labs/Lab08/setup.py
```

> **Windows (if curl doesn't work):** Use PowerShell:
> ```powershell
> New-Item -ItemType Directory -Force -Path Labs\Lab08
> Invoke-WebRequest -Uri https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab08/setup.py -OutFile Labs\Lab08\setup.py
> ```

Steps 1–4 run from **CISC395/ root**. Steps 5–6 run from **`trip_notes/`**.

**Step 1 — Create `CISC395/.gitignore`** (manually in VS Code or any text editor):
```
.env
.venv/
__pycache__/
*.pyc
chroma_db/
```
Then commit and push **before creating `.env`**:
```bash
git add .gitignore
git commit -m "chore: add gitignore"
git push
```
> If `.env` enters git history before `.gitignore` is committed, your API key is permanently recorded — even if you delete the file later.

**Step 2 — Create `CISC395/.env`** (never commit this file):
```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```
Get a free key at openrouter.ai (no credit card required). Gemini alternative: `GEMINI_API_KEY=AIza-...` from aistudio.google.com.

**Step 3 — Create `.venv` (skip if already exists from a previous lab):**
```bash
python -m venv .venv
```
Or in VS Code: `Ctrl+Shift+P` → *Python: Create Virtual Environment* → select `.venv`.

Activate and install:
```bash
# Activate — Windows:
.venv\Scripts\activate
# Activate — Mac/Linux:
source .venv/bin/activate

pip install openai python-dotenv
pip freeze > requirements.txt
```
> `.venv/` and `.env` both live at `CISC395/` root and are shared across all labs. VS Code auto-detects `.venv` since it is at the workspace root.

> **Windows PowerShell error?** Run once: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Step 4 — Enter `trip_notes/` in both terminals:**
```bash
cd trip_notes
```
**AI (Option A):** launch Gemini CLI (`gemini`) or Claude Code. **Run Terminal:** all python, git, and test commands. `.venv` stays active after `cd`.

**Step 5 — Run the setup check (Run Terminal):**
```bash
python tests/check_api_setup.py
```
Checks `CISC395/.gitignore`, `.env`, `.venv`, `requirements.txt`, then automatically tests your API key. **Fix every failure before continuing.**

If OpenRouter is unavailable, try the Gemini backup:
```bash
python tests/check_gemini.py
```
The script prints the exact lines to swap into `ai_assistant.py`.

**Step 6 — Run the code structure check (Run Terminal):**
```bash
python tests/test_ai_assistant.py
# Expected: import error — src/ai_assistant.py is empty (normal for now)
```

**Step 7 — Polish the menu before adding AI options:**

**AI (one line):**
```
# Option A — Gemini CLI / Claude Code
Please read and follow the instructions in @prompts/Lab08_Setup_menu.md

# Option B — Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab08_Setup_menu.md
```

This refactors `main.py` to use `[Q]` to quit and adds visual grouping with an empty `-- AI --` section ready for Ex 3. Verify it works:
```bash
python src/main.py
# Menu should show grouped sections and Q to quit
```

Then commit:
```bash
git add src/main.py ../requirements.txt
git commit -m "chore: lab08 environment ready"
git push
```

---

## Exercises

### Exercise 1 — Build `src/ai_assistant.py` (25 pts)

This file holds the API client, the `ask()` function, and the system prompt. All AI logic lives here so `main.py` stays focused on the menu.

**AI (one line):**
```
# Gemini CLI / Claude Code
Please read and follow the instructions in @prompts/Lab08_Ex01_assistant.md

# Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab08_Ex01_assistant.md
```

The AI reads the prompt file and writes `src/ai_assistant.py` directly.

**Verify structure (Run Terminal):**
```bash
python tests/test_ai_assistant.py
# ask(), TRAVEL_SYSTEM_PROMPT, client, MODEL should all pass
```

**Live API test (Run Terminal):**
```bash
python src/ai_assistant.py
```

**Paste the output of `python src/ai_assistant.py`:**

```
[Paste AI response here]

Testing AI Assistant...


For budget-conscious students, **winter (December-February)** is Japan's best travel season. Key reasons:

1.  **Cheaper Flights & Accommodation:** Significant discounts on flights and hostels/hotels, especially in major cities and ski resorts like Nagano/Niseko.
2.  **Less Crowds:** Major attractions are far less crowded than spring or autumn.
3.  **Unique Experiences:** Snow festivals (Sapporo), winter illuminations, and relaxing in onsens (hot springs) like Hakone or Beppu are affordable highlights.
4.  **Budget Food:** Convenience stores (7-Eleven, FamilyMart) offer incredibly cheap, filling meals (onigiri, bento).

**Avoid:** Spring (cherry blossom crowds & prices) and Autumn (foliage crowds & prices). Winter requires packing warm clothes, but the savings and unique experiences
```

**Understanding check (required):** `TRAVEL_SYSTEM_PROMPT` is defined in `ai_assistant.py`, not in `main.py`. Using the separation of concerns idea from Lab 07 — which layer does `ai_assistant.py` represent? What would break if you moved the system prompt into `main.py`?

```
the ai_assistant.py represents the service/API integration layer. if you were to move the the system prompt into main.py the seperation of concerns would break, this would limit the UI from accessing the prompt
```

**Git commit:**
```bash
git add src/ai_assistant.py requirements.txt
git commit -m "feat: ai_assistant.py with ask() function"
git push
```

---

### Exercise 2 — Temperature and System Prompt (25 pts)

#### Part A — Temperature experiment (15 pts)

Ask the same travel question at three temperatures. Run each **twice** using a short script in the Run Terminal:

```python
# Run from trip_notes/ — save as temp_test.py or paste directly into python shell
from src.ai_assistant import ask, TRAVEL_SYSTEM_PROMPT
print(ask("Suggest a unique activity for a solo traveler visiting Tokyo.",
          system_prompt=TRAVEL_SYSTEM_PROMPT,
          temperature=0.1))
```

Change `temperature=` to `0.1`, `0.7`, and `1.4` for each row. Run each twice.

Suggested question: `"Suggest a unique activity for a solo traveler visiting Tokyo."`

| Temperature | Run 1 (first 15 words) | Run 2 (first 15 words) |
|-------------|----------------------|----------------------|
| 0.1 | | |     4. **Budget tip** – Total cost ≈ ¥3,300 (~US$22). Use a Suica/Pasmo card for transit; the market and gardens 

**Tokyo Night Photography Walk – Shibuya & Harajuku**

| What | Where | How |
|------|-------|-----|
| Meet a local photographer (free group on Meetup
| 0.7 | | |    It's social yet solo-friendly—you’ll join a small team, often mixing with locals and

and is perfect for reflection. Afterward, explore the gardens' beautiful landscapes and teahouse overlooking
| 1.4 | | |    r affordability, local vibes, and memorable street art. Stay at **K's House Kanda**, a cheap and clean

- Lunch: ¥450  
- Snacks/Dinner: ¥600  
- Suica top‑up: ¥1,000  
**Total ≈ ¥6,950 (≈ $50)** – a full‑day solo adventure without breaking the budget.

**Analysis:** What pattern do you see across the three temperatures? For a feature that recommends well-known landmarks, which temperature would you choose? For generating creative trip ideas, which one? (3–4 sentences)

```
[Your analysis]

As the temperature increases from 0.1 to 1.4, the AI's responses become more diverse, creative, and sometimes less predictable. For a feature recommending well known landmarks, a low temperature 0.1 is best because it provides consistent, factual, and highly probable outputs. for generating creative trip ideas or off-the-beaten-path suggestions, a higher temperature 0.7 or 1.4 is best as it encourages the AI to explore different answers.
```

#### Part B — System prompt in action (10 pts)

Test `TRAVEL_SYSTEM_PROMPT` with these two messages:

Message 1: `"I have $500 and 5 days. Where should I go in Southeast Asia?"`
Message 2: `"Is it safe to travel alone as a student?"`

**Output from Message 1:**
```
[Paste here]

A unique and solo-wise-serving activity in Tokyo could be **hiking and exploring lesser-known spots in the Nikko region rather than just the city**, although this can be a bit challenging geographically, it offers something remarkable.

**Activation + Detail:**  
Instead of just going around the city, spend **one or two days off-pulse exploring the tranquil shrines and mountains outside Tokyo** for your trip. This allows you to travel outside heavily-touristed routes without overcrowding yourself and is unique among visitors, especially for solo tourism in Japan.

- **Option:** Take the first train to Nikko, spend one full day hiking in the cedar forests of Hakone (like Oyako Park with its hot springs) or Kegon Falls for breathtaking views.
- **Uniqueness:** Find yourself solitude in natural serenity, away from the usual buzz. It also builds the theme: nature + solitude = something rare.

**Transport tip:** Take day 2 of Nikko trip (even within Tokyo time zone travel) or pair it with a day trip, since that’s one place and gives the adventure element. Tokyo can be covered for a day or two alone with efficient trains, fitting your schedule constraint.

Would you like alternative unique solo-oriented activities in Tokyo not in its famous hot-spots area?
```

**Output from Message 2:**
```
[Paste here]

One unique activity for a solo traveler visiting Tokyo is to explore the vibrant neighborhood of Shimokitazawa. Known for its bohemian atmosphere and eclectic mix of vintage shops, cafes, and live music venues, Shimokitazawa offers a glimpse into Tokyo's alternative culture. You can spend hours wandering through the narrow streets, browsing through quirky boutiques, and sampling delicious street food. Additionally, the area is home to several small theaters and performance spaces, where you can catch indie films, plays, or live music shows. It's a great way to immerse yourself in Tokyo's creative scene and meet fellow travelers or locals who share your interests.
```

**Reflection:** Pick one response and identify a specific phrase that shows the persona is working. If the persona is not visible, rewrite the system prompt and test again. (2–3 sentences)

```
I would say that the first response captures the AI persona of being a travel assistant, it takes the persons schedule into account for trips you are taking throughout the days, in the end of message 1 the AI agent mentions 'schedule constraint'.
```

---

### Exercise 3 — Add AI to the Menu (20 pts)

Add option `[6] Ask AI` to `main.py` so users can ask travel questions and optionally save the answer as a note on a saved trip.

**AI (one line):**
```
# Gemini CLI / Claude Code
Please read and follow the instructions in @prompts/Lab08_Ex03_menu.md

# Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab08_Ex03_menu.md
```

**Test the full app (Run Terminal):**
```bash
python src/main.py
```

**Paste a test session showing:**
1. Asking the AI a travel question via option [6]
2. Saving the AI response as a note on a saved trip
3. Viewing that trip (option [2]) to confirm the note was attached

```
[Paste terminal output here]

AI Response:
China is located in East Asia. It borders 14 countries, including Russia, Mongolia, India, and Vietnam. The country stretches from the Pacific Ocean in the east to Central Asia in the west, covering a vast area of 9.6 million square kilometers.
```

**Understanding check (required):** `main.py` calls `ask()` from `ai_assistant.py` — it doesn't know what model is running or how errors are handled. Following the same dependency rule as Lab 07, what would you need to change to switch from LLaMA to a different model? Which files would you touch?

```
[Your answer]

based off AI's reasoning, you would need to change the model variable inside the ai_Aassistant.py, this is due to seperation concerns, the file that you would touch is the src ai_assistant.py. 
```

**Git commit:**
```bash
git add src/main.py
git commit -m "feat: Ask AI menu option"
git push
```

---

### Exercise 4 — Prompt Chaining: Trip Briefing (20 pts)

Build a two-step AI pipeline where the output of Call 1 becomes the input of Call 2. Then connect it to your saved trips data.

#### Part A — Build `generate_trip_briefing()` (10 pts)

**AI (one line):**
```
# Gemini CLI / Claude Code
Please read and follow the instructions in @prompts/Lab08_Ex04_chaining.md

# Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab08_Ex04_chaining.md
```

**Run the structure test (Run Terminal):**
```bash
python tests/test_ai_assistant.py
# generate_trip_briefing() section should now pass (city, country, notes)
```

**Run the live test (Run Terminal):**
```bash
python src/ai_assistant.py
```

**Paste the output for `generate_trip_briefing("Tokyo", "Japan")`:**

```
Overview:
Tokyo is a vibrant metropolis blending cutting-edge technology with rich traditions, offering everything from neon-lit streets to serene temples. Visit during spring (March–May) for cherry blossoms or autumn (November–December) for vibrant foliage, both ideal for sightseeing. Don’t miss the iconic Shibuya Crossing and a visit to the historic Asakusa Senso-ji Temple for a taste of old Japan.


Packing list:
Packing list:
 **5‑Item Tokyo Packing List for a Budget‑Savvy Student**

1. **Compact Umbrella & Light Raincoat** – Spring showers are common; a foldable umbrella (≈¥1,200) and a thin waterproof jacket keep you dry without bulk.  
2. **Reusable Water Bottle + Small Detachable Thermos** – Tap water is safe; refill stations are everywhere (convenience stores, train stations). A thermos lets you bring cheap “bento‑style” meals on the go.  
3. **Portable Wi‑Fi Router or SIM Card** – Pocket Wi‑Fi (≈¥400/day) or a prepaid data SIM (e.g., b-mobile, ¥3,000 for 30 GB) is essential for navigating trains, translating menus, and grabbing last‑minute hostel deals.  
4. **Comfortable, Slip‑On Sneakers + Packable Sock Liners** – You’ll walk 10‑15 km daily; breathable sneakers (e.g., Uniqlo) paired with thin liner socks prevent blisters and are easy to remove for Japan’s shoe‑off etiquette in temples and some cafés.  
5. **Travel‑Size Hand Sanitizer & Pack of Disposable Masks** – Public transport can be crowded; a 50 ml sanitizer bottle (≈¥300) and a small mask pack (≈¥200) keep you healthy and respect local hygiene norms.  

*All items fit in a 25‑L backpack, leaving room for souvenirs and your camera.*
```

**Understanding check (required):** The packing list (Call 2) uses the overview text from Call 1 as its input, not just the city name. Why does giving Call 2 more context produce a better packing list? What would the packing list look like if Call 2 only received `"Tokyo"`? (2–3 sentences)

```
[Your answer]

By giving call 2 more context gives it all the information like the weather, seasons, and activities, this allows it to recommend things to you based off the conditions, if call 2 only recieved tokyo then the output would have been more generic then specific. 
```

**Git commit:**
```bash
git add src/ai_assistant.py
git commit -m "feat: trip briefing prompt chain"
git push
```

---

#### Part B — Connect to Menu [7] (10 pts)

Now connect `generate_trip_briefing()` to your real saved trips. Option [7] reads destinations from `storage.py` and generates a personalized briefing using the trip's saved notes.

**AI (one line):**
```
# Gemini CLI / Claude Code
Please read and follow the instructions in @prompts/Lab08_Ex04b_menu.md

# Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab08_Ex04b_menu.md
```

**Add at least 2 destinations with notes (Run Terminal):**
```bash
python src/main.py
# Use option [1] to add trips, option [4] to add notes
# Then use option [7] to generate a briefing
```

> If a destination has no notes, the briefing still works — the `notes` parameter is optional and ignored when empty.

**Paste a test session showing:**
1. Selecting a destination from the numbered list
2. The generated Overview and Packing List output

```
[Paste terminal output here]

Generating briefing for NYC...

--- NYC Briefing ---
Overview:
New York City is a vibrant, fast-paced metropolis with endless free attractions like Central Park, the High Line, and the Staten Island Ferry for iconic skyline views. The best time to visit is spring (April-May) or fall (September-October) for mild weather and fewer crowds. A must-see is walking across the Brooklyn Bridge at sunset for breathtaking views of Manhattan and the Statue of Liberty.

Packing List:


Here’s a 5-item NYC-specific packing list for budget-conscious students:

1.  **Comfortable Walking Shoes:** Invest in sturdy, broken-in sneakers or walking sandals (e.g., Skechers Go Walk, Converse). NYC demands miles of walking daily.
2.  **Reusable Water Bottle:** Save cash and stay hydrated (e.g., Hydro Flask or a cheap insulated bottle). Fill up at free water fountains.
3.  **Lightweight, Packable Jacket:** A compact windbreaker or hoodie (e.g., Uniqlo Heattech) for unpredictable spring/fall weather.
4.  **Crossbody Bag:** A secure, affordable option (e.g., Amazon Basics or a thrifted tote) to keep essentials safe on crowded subways and streets.
5.  **Portable Phone Charger:** Essential for all-day exploration (e.g., Anker PowerCore 10000). NYC has long days and constant photo ops.
```

**Understanding check (required):** If one of your notes says "business conference" or "travelling with kids", does the briefing reflect it? Why does passing `dest.notes` into `generate_trip_briefing()` allow the AI to personalize the output? (2–3 sentences)

```
[Your answer]

Yes the briefing will reflect it, passing the dest note into the generate_trip_briefing function will add the users specific context into the prompt which gives the AI what it needs to personalize the output such as recommendations and activities.
```

**Git commit:**
```bash
git add src/main.py
git commit -m "feat: trip briefing menu option"
git push
```

---

### Reflection (10 pts)

**1.** What is `.venv/` and why do we create it? What would happen if two different projects on your computer used the same global Python environment instead of separate `.venv/` folders?

```
the venv is a virtual environment folder that acts as an isolated sandbox for projects, if two different projects shared the same environment installing a new version for a library would break one of the two projects that relied on the older version of that library.
```

**2.** What does `pip install openai python-dotenv` actually do? Why do we also run `pip freeze > requirements.txt` afterward — what problem does that file solve?

```
pip install command downloads and installs external libraries from the internet so that way we are able to use them within our files and code, the freeze > requirements.txt` records every library and its versions that are installed to ensure there is no cloning. 
```

**3.** You committed `.gitignore` before creating `.env`. Why does the order matter? What would happen if you created `.env` first, committed it, then added it to `.gitignore`?

```
the order matters because gitgore prevents untracked files from being added to the git, if you were to create the env file first then the API key would be recorded in the git history permanently, this would expose your secret to your public. 
```

**4.** In this lab, every time a user types a travel question, your app makes an API call to OpenRouter. What is actually happening in that call — what does your app send, and what does it get back? How is this different from just searching Google?

```
when the app makes an API call it sends an HTTP request containing a json payload that contains the models name and the system prompt with the users question that is authenticated by the API key, open router sends back a response in form of json that contains generated text by the language model. this is different from a google search because a google search will give you a list of websites and link with match keywords, The AI gives you a custom answer tailored to your prompts constraints. 
```

---

## Grading Rubric

| Exercise | Criteria | Points |
|----------|---------|--------|
| Ex 1: ai_assistant.py | Structural test passes, live API output pasted, understanding check answered | 25 |
| Ex 2A: Temperature | Table filled with real outputs, analysis addresses pattern | 15 |
| Ex 2B: System prompt | Two outputs pasted, reflection identifies specific phrase | 10 |
| Ex 3: Menu option | App runs, test session pasted (ask + save + view), understanding check answered | 20 |
| Ex 4A: Prompt chaining | Structural test passes (city/country/notes), output pasted, understanding check answered | 10 |
| Ex 4B: Menu integration | Option [7] runs with real data, test session pasted, understanding check answered | 10 |
| Reflection | Both questions answered with substance | 10 |

**Understanding checks are required.** Empty answers lose those points.
**Commits are required.** Missing commits lose the commit portion of each exercise's points.

---

## Quick Reference

**Always run from inside `trip_notes/`** (with `.venv` active in Run Terminal):
```bash
python src/main.py          # run the full app
python src/ai_assistant.py  # test API directly
python tests/test_ai_assistant.py    # structural checks
```

**Activate venv** (if you opened a new terminal):
```bash
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

**Re-download prompts and test file** (from CISC395/ root):
```bash
cd ..
python Labs/Lab08/setup.py --refresh
cd trip_notes
```

**messages structure:**
```python
messages = [
    {"role": "system", "content": "You are a travel assistant."},
    {"role": "user",   "content": "What should I pack for Iceland?"},
]
```

**Model and extra_body:**
```python
MODEL = "openrouter/free"
# Always include extra_body — required for openrouter/free routing
extra_body = {"reasoning": {"enabled": True}}
```
`openrouter/free` routes to the best available free model. With reasoning enabled, `content` may be `None` — the `ask()` function handles this automatically.

**Next lab:** Lab 09 adds RAG — upload your own destination guide documents and let the AI search them before answering.
