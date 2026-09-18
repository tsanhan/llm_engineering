import os
import json
from IPython.display import Markdown, display, update_display
from scraper import fetch_website_links, fetch_website_contents
from openai import OpenAI

links = fetch_website_links("https://edwarddonner.com")
print(f"Found {len(links)} links on the website.")

client = OpenAI(
    base_url=os.getenv('SMOLLM2_URL'),
    api_key='not-needed'
)
model = os.getenv('SMOLLM2_MODEL')
response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": "hi"}
        ]
    )
result = response.choices[0].message.content
print(f"Response from {model}: {result}")
