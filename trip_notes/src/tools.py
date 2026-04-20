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
