from openai import OpenAI
from os import getenv

OPENROUTER_API_KEY = "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"

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENROUTER_API_KEY,
)

completion = client.chat.completions.create(
  model="openai/gpt-4o-mini",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)
print(completion.choices[0].message.role)
