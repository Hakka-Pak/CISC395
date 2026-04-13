from src.ai_assistant import ask, TRAVEL_SYSTEM_PROMPT
print(ask("Suggest a unique activity for a solo traveler visiting Tokyo.",
          system_prompt="Is it safe to travel alone as a student?",
          temperature=1))