from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Fetch MongoDB credentials from environment variables
openAI_key = os.getenv("openAI_key")

client = OpenAI(
  api_key=openAI_key,
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message)
