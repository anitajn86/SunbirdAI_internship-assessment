import os
import requests
from dotenv import load_dotenv

# Load access token from .env
load_dotenv()
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbml0YWpuNzk5MCIsImFjY291bnRfdHlwZSI6IkZyZWUiLCJleHAiOjQ4OTk2ODY4Njd9.zLA5twIi6ViWYZURY16g0dombf84YWcQSaq54xA02L8"

# Language code mapping
language_codes = {
    "english": "eng",
    "luganda": "lug",
    "runyankole": "nyn",
    "ateso": "teo",
    "lugbara": "lgg",
    "acholi": "ach"
}

languages = list(language_codes.keys())

# Sunbird API endpoint
url = "https://api.sunbird.ai/tasks/nllb_translate"

# Request headers
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

def get_user_input():
    print("Welcome to the Translator")
    print("Languages supported:", ", ".join(lang.capitalize() for lang in languages))

    source = input("Enter source language: ").strip().lower()
    while source not in languages:
        print("Invalid source language. Try again.")
        source = input("Enter source language: ").strip().lower()

    target = input("Enter target language: ").strip().lower()
    while target not in languages or target == source:
        print("Invalid or same as source language. Try again.")
        target = input("Enter target language: ").strip().lower()

    text = input(f"Enter text in {source.capitalize()}: ").strip()
    return source, target, text

def translate_text(source, target, text):
    data = {
        "source_language": language_codes[source],
        "target_language": language_codes[target],
        "text": text,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json().get("result", "[No result in response]")
    else:
        return f"[Error {response.status_code}]: {response.text}"

def main():
    source, target, text = get_user_input()
    translated = translate_text(source, target, text)
    print(f"\n Translation ({source} → {target}): {translated}")

if __name__ == "__main__":
    main()
