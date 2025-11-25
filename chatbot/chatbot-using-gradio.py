# This script creates a chatbot using gradio and openai

import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def chatbot(message, history):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a helpful assistant."}] + history + [{"role": "user", "content": message}]
    )
    return response.choices[0].message.content

demo = gr.ChatInterface(fn=chatbot)

demo.launch()