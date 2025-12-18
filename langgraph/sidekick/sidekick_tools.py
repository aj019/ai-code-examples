from langchain.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
import asyncio
from playwright.async_api import async_playwright

@tool
async def web_search(query: str) -> str:
    """ A tool that can search the web for information
        Args:
        query : the query to search the web for
     """
    return await GoogleSerperAPIWrapper().arun(query)


# Initialize Playwright tools
async def initialize_tools():
    print("Initializing tools...")
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    playwright_tools_list = toolkit.get_tools()
    tools = [web_search] + FileManagementToolkit(root_dir="sandbox").get_tools() + playwright_tools_list
    # Combine all tools
    return tools

agent_tools = asyncio.run(initialize_tools())