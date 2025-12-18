from langchain.tools import tool
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain.messages import AnyMessage, SystemMessage, ToolMessage, HumanMessage
from typing import Annotated, TypedDict, Dict
from IPython.display import Image, display
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from playwright.async_api import async_playwright
import operator
import asyncio
import os

load_dotenv()

model = init_chat_model(
    "gpt-4o-mini",
    temperature=0
)

# First Step is defining tools

@tool
def add(a:float, b:float) -> float:
    """ Add two numbers together
        Args: 
        a : the first number
        b : the second number
    """
    return a + b

@tool
async def web_search(query: str) -> str:
    """ A tool that can search the web for information
        Args:
        query : the query to search the web for
     """
    return await GoogleSerperAPIWrapper().arun(query)

# Second Step is defining the state
class MessageState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int


# Third Step is defining the nodes

async def llm_call(state: Dict, tools_by_name: Dict, model_with_tools):
    """ LLM Decides whether to call a tool or not """
    
    return {
        "messages": [
            await model_with_tools.ainvoke([
                SystemMessage(content="You are a helpful assistant that can use tools to help the user."),
            ] + state["messages"])
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

async def tool_node(state: Dict, tools_by_name: Dict):
    """ Perform's the tool call and returns the result """
    
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = await tool.ainvoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}


def should_continue(state: Dict):
    """ Decides whether to continue the graph or not """
    
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tool_node"
    else:
        return END

# Fourth Step: Initialize tools and build graph asynchronously
async def create_agent():
    # Initialize Playwright tools
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    playwright_tools_list = toolkit.get_tools()
    
    # Combine all tools
    tools = [add, web_search] + FileManagementToolkit(root_dir="sandbox").get_tools() + playwright_tools_list
    model_with_tools = model.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}
    
    # Create node functions with tools bound
    async def llm_call_node(state: Dict):
        return await llm_call(state, tools_by_name, model_with_tools)
    
    async def tool_node_wrapper(state: Dict):
        return await tool_node(state, tools_by_name)
    
    # Build the graph
    agent_builder = StateGraph(MessageState)
    agent_builder.add_node("llm_call", llm_call_node)
    agent_builder.add_node("tool_node", tool_node_wrapper)
    agent_builder.add_edge(START, "llm_call")
    agent_builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
    agent_builder.add_edge("tool_node", "llm_call")
    agent = agent_builder.compile()
    
    return agent

print("Running the agent...")
# Fifth Step is running the graph
async def run_agent():
    agent = await create_agent()
    result = await agent.ainvoke({"messages": [HumanMessage(content="Get the top 5 news from news.ycombinator.com of today in markdown format and save it to a file called news.md")]})
    for m in result["messages"]:
        m.pretty_print()

asyncio.run(run_agent())