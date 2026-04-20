In my Trip Notes project (run from trip_notes/):

src/tools.py already has:
- budget_breakdown(destination, days, budget_usd) -> str   (pure math)
- get_weather(city) -> str                                 (external HTTP API)
- search_guides_tool(query) -> str                         (searches local guides via rag.py)
- TOOL_DEFINITIONS: list of 3 dicts in OpenAI function-calling format

src/ai_assistant.py already has:
- client, MODEL (OpenAI client pointing to OpenRouter)
- ask(user_message, system_prompt=None, temperature=0.7, max_tokens=1024) -> str

Add a function run_agent(user_question: str) -> str to src/tools.py:

1. Imports at the top of tools.py (add if not already present):
   import json
   from src.ai_assistant import client, MODEL

2. run_agent(user_question: str) -> str:
   a. Build initial messages list:
      system: "You are a travel planning agent. Use the available tools to help
               users plan trips. Always use a tool if it can answer the question
               more accurately — especially for real-time data or guide content."
      user: user_question

   b. Run a loop (max 5 iterations):
      - Call client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
            max_tokens=1024,
            timeout=30,
        )
      - Get msg = response.choices[0].message
      - If msg.tool_calls is None or empty:
            return msg.content  ← final answer, exit loop
      - For each tool call in msg.tool_calls:
            name = tc.function.name
            args = json.loads(tc.function.arguments)
            print(f"[Tool call] {name}({args})")
            Call the matching Python function:
              if name == "budget_breakdown":   result = budget_breakdown(**args)
              elif name == "get_weather":      result = get_weather(**args)
              elif name == "search_guides_tool": result = search_guides_tool(**args)
              else: result = f"Unknown tool: {name}"
            print(f"[Tool result] {result[:120]}...")
            Append to messages:
              {"role": "assistant", "content": None, "tool_calls": [tc]}  ← assistant turn
              {"role": "tool", "tool_call_id": tc.id, "content": result}  ← tool result

   c. If loop ends without returning: return "Agent reached maximum iterations."

3. Do NOT add a new if __name__ == "__main__" block — one already exists.

Write the updated file directly to src/tools.py.
