from dotenv import load_dotenv
from agents import Agent, Runner, trace,function_tool, WebSearchTool, ModelSettings
import asyncio
from pydantic import BaseModel

load_dotenv()

HOW_MANY_SEARCHES = 2


INSTRUCTIONS = """
You are a helful research assistant. You are given a query , come up with a set of web searches
to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for.
"""

class WebSearchItem(BaseModel):
    reason: str
    "Your reasoning for why this search is important to the query"
    query: str
    "The search item to use for the web search"


class WebSearchPlan(BaseModel):
    search_items: list[WebSearchItem]
    "The list of search items to use for the web search"

    
planner_agent = Agent(
    name="Web Search Planner",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan
)


    