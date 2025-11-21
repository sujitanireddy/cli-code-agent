import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


if len(sys.argv) <= 1:
    print('ai-agent')
    print('Usage: python main.py "<prompt>"')
    print("No prompt given. Exiting the program..")
    exit(1)

user_prompt = sys.argv[1]

#load api key from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

#create a new instance of a Gemini client
client = genai.Client(api_key=api_key)

messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]

response = client.models.generate_content(model='gemini-2.5-flash', contents=messages)

print(response.text)

if '--verbose' in sys.argv: 
    print(f'User prompt: {user_prompt}')
    print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
    print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
