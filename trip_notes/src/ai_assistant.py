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

if __name__ == "__main__":
    print("Testing AI Assistant...")
    result = ask("What is the best time of year to visit Japan?", system_prompt=TRAVEL_SYSTEM_PROMPT)
    print(result)