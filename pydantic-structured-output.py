import pydantic
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

class User(BaseModel):
    name: str
    age: int

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

response = client.chat.completions.parse(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Give me a name and age of a user."}],
    response_format=User
)

print(response.choices[0].message.content)
