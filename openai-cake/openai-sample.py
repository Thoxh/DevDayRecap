from openai import OpenAI
import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant. Answer always in German."},
        {
            "role": "user",
            "content": "Erstelle mir ein Rezept für einen Apfelkuchen."
        }
    ]
)

print(completion.choices[0].message)