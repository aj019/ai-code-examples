# This script creates a chatbot using gradio and openai

import gradio as gr
from agents import Agent, Runner, trace
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")



agent = Agent(name="Assistant", instructions="You are a helpful assistant.", model="gpt-4o-mini")

def chatbot(message, history):
    result = asyncio.run(Runner.run(agent, message))
    return result.final_output

demo = gr.ChatInterface(fn=chatbot)

demo.launch()