from flask import Flask, jsonify
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from flask_cors import CORS  # Für Cross-Origin Requests

# Lade Umgebungsvariablen
load_dotenv()

app = Flask(__name__)
CORS(app)  # Aktiviere CORS für alle Routen

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/get-recipe', methods=['GET'])
def get_recipe():
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful cooking assistant. Answer always in German."},
                {
                    "role": "user",
                    "content": "Erstelle mir ein Rezept für einen beliebigen Kuchen, den ich noch nicht kenne. "
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "recipe_response",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "response": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string"},
                                    "description": {"type": "string"},
                                    "difficulty": {"type": "string"},
                                    "prepTime": {"type": "string"},
                                    "servings": {"type": "string"},
                                    "category": {"type": "string"},
                                    "imageUrl": {"type": "string"},
                                    "author": {"type": "string"},
                                    "ingredients": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "steps": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "tips": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                },
                                "required": [
                                    "title", "description", "difficulty", "prepTime",
                                    "servings", "category", "imageUrl", "author",
                                    "ingredients", "steps", "tips"
                                ],
                                "additionalProperties": False
                            }
                        },
                        "required": ["response"],
                        "additionalProperties": False
                    }
                }
            }
        )
        recipe_content = json.loads(completion.choices[0].message.content)
        print(recipe_content)

        # Generate image based on recipe title
        image_prompt = f"Professional food photography of {recipe_content['response']['title']}, appetizing, high quality, restaurant style"
        image_response = client.images.generate(
            prompt=image_prompt,
            n=1,
            size="1024x1024",
            quality="standard",
            style="natural"
        )
        
        # Update the imageUrl in the recipe response
        recipe_content['response']['imageUrl'] = image_response.data[0].url # "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/Technische_Hochschule_Brandenburg_Logo.svg-yJa7AHSax1OpkUTnWn3Zya2dZhjJWU.png"
        print(jsonify(recipe_content))
        return jsonify(recipe_content)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)