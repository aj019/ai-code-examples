import gradio as gr
from sidekick import sidekick
from langchain.messages import HumanMessage
import asyncio


async def process_message(message, history):
    sidekick_response = await sidekick.ainvoke({"messages": [HumanMessage(content=message)]}, {"configurable": {"thread_id": "1"}})
    for m in sidekick_response["messages"]:
        m.pretty_print()
    sidekick_response_content = sidekick_response["messages"][-1].content
    return sidekick_response_content


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(placeholder="<strong>Your Sidekick</strong><br>How can i help ?")    
    gr.ChatInterface(fn=process_message, chatbot=chatbot)
    
demo.launch()