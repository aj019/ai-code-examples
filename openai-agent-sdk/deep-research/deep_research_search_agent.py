from dotenv import load_dotenv
from agents import Agent, Runner, trace,function_tool, WebSearchTool, ModelSettings
import asyncio

load_dotenv()


INSTRUCTIONS = """
You are a deep research agent. Given a search term , you search the web for that term
and produce a concise summary of the research. The summary must 2-3 paragraphs and less than 300
words . Capture the main points and key insights. Write succintly , no need to have complete sentences.
This will be consumed by someone synthesizing the information for a report. so its vital you capture
the essance and ignore any fluff. Do not include any additional commentary other than the summary.
"""

search_agent = Agent(
    name="Web Search Agent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=[WebSearchTool(search_context_size="low")],
    model_settings=ModelSettings(tool_choice="required")
)

    