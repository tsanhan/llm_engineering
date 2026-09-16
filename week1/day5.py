import os
import json
from dotenv import load_dotenv
from IPython.display import Markdown, display, update_display
from scraper import fetch_website_links, fetch_website_contents
from openai import OpenAI

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith('sk-proj-') and len(api_key)>10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key? Please visit the troubleshooting notebook!")
    
openai = OpenAI()

links = fetch_website_links("https://edwarddonner.com")
print(f"Found {len(links)} links on the website.")

client = OpenAI(
    base_url=os.getenv('DEEPSEEK_URL'),
    api_key='not-needed'
)
model = os.getenv('DEEPSEEK_MODEL')
response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": "hi"}
        ]
    )
result = response.choices[0].message.content
print(f"Response from {model}: {result}")
