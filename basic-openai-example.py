import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

message = [{"role" : "user", "content": "What is 2+2 ?"}]

response =client.chat.completions.create(model="gpt-4o", messages=message)

print(response.choices[0].message.content)

