import os
import requests
import contextlib

from dotenv import load_dotenv

# Loading the API token
load_dotenv()
access_token = " eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbml0YWpuNzk5MCIsImFjY291bnRfdHlwZSI6IkZyZWUiLCJleHAiOjQ4OTk2ODY4Njd9.zLA5twIi6ViWYZURY16g0dombf84YWcQSaq54xA02L8"

# API endpoint and headers
url = "https://api.sunbird.ai/tasks/stt"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {access_token}",
}

# available languages and their codes
language_codes = {
    "english": "eng",
    "luganda": "lug",
    "runyankole": "nyn",
    "ateso": "teo",
    "lugbara": "lgg",
    "acholi": "ach"
}

def get_user_input():
    file_path = input("Enter path to MP3 audio file (less than 5 minutes): ").strip()

    # Checking for file existence
    if not os.path.isfile(file_path):
        print("File does not exist.")
        exit()

    # Checking for file format
    if not file_path.lower().endswith('.mp3'):
        print("Only MP3 files are allowed.")
        exit()

    print("Available languages:", ", ".join(language_codes.keys()))
    language = input("Enter language of the audio: ").strip().lower()

    if language not in language_codes:
        print("Unsupported language.")
        exit()

    return file_path, language

def transcribe_audio(file_path, language):
    lang_code = language_codes[language]

    with open(file_path, "rb") as audio_file:
        files = {
            "audio": (os.path.basename(file_path), audio_file, "audio/mpeg"),
        }
        data = {
            "language": lang_code,
            "adapter": lang_code,
        }

        response = requests.post(url, headers=headers, files=files, data=data)

        if response.status_code == 200:
            result = response.json()
            print("\n📝 Transcription:")
            print(result.get("result", "[No transcription returned]"))
        else:
            print(f"Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    path, lang = get_user_input()
    transcribe_audio(path, lang)
