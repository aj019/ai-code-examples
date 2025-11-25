import pydantic
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

class Evaluator(BaseModel):
    is_accepatable: bool
    feedback: str

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

evaluator_system_prompt = f"""
You are a helpful assistant that evaluates the quality of the response.
You will be given a response and you need to evaluate if it is acceptable or not.
You need to provide feedback on how to improve it.
"""

def evaluator_user_prompt(reply, message, history):
    return f"""
    The user's message: {message}
    The assistant's reply: {reply}
    The conversation history: {history}
    """    


question = "What is the capital of France?"
question_response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": question}]
)
reply = question_response.choices[0].message.content
print(reply)
history = []

evaluator_response = client.chat.completions.parse(
    model="gpt-4o",
    messages=[{"role": "system", "content": evaluator_system_prompt}, {"role": "user", "content": evaluator_user_prompt(reply, question, history)}],
    response_format=Evaluator
)

print(evaluator_response.choices[0].message.content)
