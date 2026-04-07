import os
import openai
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)
MODEL = "openrouter/free"

TRAVEL_SYSTEM_PROMPT = """You are a highly knowledgeable and concise travel assistant tailored for budget-conscious student travelers. 
Your advice should be extremely practical and prioritize affordability without sacrificing safety or the quality of the experience. 
Always recommend specific, tangible places, hostels, affordable eateries, and local transit options rather than speaking in generalities. 
Keep all your answers under 200 words."""

def ask(user_message: str, system_prompt: str | None = None, temperature: float = 0.7, max_tokens: int = 500) -> str | None:
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=30,
            extra_body={"reasoning": {"enabled": True}} # adding this explicitly as told in quick ref
        )
        return response.choices[0].message.content
    except openai.AuthenticationError:
        print("Error: Invalid or missing API key.")
        return None
    except openai.RateLimitError:
        print("Error: Rate limit exceeded. Try again later.")
        return None
    except openai.APIConnectionError:
        print("Error: Could not connect to the API. Check your internet connection.")
        return None

def generate_trip_briefing(city: str, country: str, notes: list = None) -> dict | None:
    base = f"Give a 3-sentence travel overview of {city}, {country}. Cover: what it's like to visit, best season to go, and one must-see attraction."
    
    if notes is not None and len(notes) > 0:
        notes_text = "\n".join(f"- {n}" for n in notes)
        prompt1 = base + f"\n\nPersonal notes about this trip:\n{notes_text}"
    else:
        prompt1 = base
        
    overview = ask(prompt1, system_prompt=TRAVEL_SYSTEM_PROMPT)
    if not overview:
        return None
        
    prompt2 = f"Based on this destination overview:\n{overview}\n\nWrite a 5-item packing list specific to {city}."
    packing_list = ask(prompt2, system_prompt=TRAVEL_SYSTEM_PROMPT)
    if not packing_list:
        return None
        
    return {"overview": overview, "packing_list": packing_list}

if __name__ == "__main__":
    print("Testing AI Assistant...")
    result = generate_trip_briefing("Tokyo", "Japan")
    if result:
        print("Overview:\n", result["overview"])
        print("\nPacking list:\n", result["packing_list"])