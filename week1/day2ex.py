from openai import OpenAI, Stream
import os
from IPython import get_ipython
from IPython.display import Markdown, display, update_display

from scraper import fetch_website_contents

system_prompt = """
You are a snarky assistant that analyzes the contents of a website,
and provides a short, snarky, humorous summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""

user_prompt_prefix = """
Here are the contents of a website.
Provide a short summary of this website.
If it includes news or announcements, then summarize these too.

"""


def messages_for(website):
    """Create message list for the LLM."""
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website}
    ]
    
base_url = os.getenv("SMOLLM2_URL", "http://localhost:12434/v1/")
model = os.getenv("SMOLLM2_MODEL", "ai/smollm2:latest")

client = OpenAI(base_url=base_url, api_key="not-needed")

def summarize(url) -> Stream:
    website = fetch_website_contents(url)
    return client.chat.completions.create(
        model = model,
        messages = messages_for(website),
        stream = True
    )


response = ""
display_handle = None

stream = summarize("https://edwarddonner.com")

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        response += content
        if display_handle is not None:
            update_display(Markdown(response), display_id=display_handle.display_id)
        else:
            print(content, end="", flush=True)

