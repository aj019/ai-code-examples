from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from openai import OpenAI
import os
import asyncio
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)




past_commands = []

page_content = ""

def plan_subtask_for_browser_agent(task):
    prompt = f"""
    You are a helpful assistant that plans the next command for a browser agent in python using playwright sync api.
    You will be provided a task and you need to plan the next command for the browser agent.    
    It should be a single command that can be executed by the browser agent not a sequence of commands in a single line.
    The command should be in the form of a python code that can be executed by the browser agent.
    The command needs to be playwright commands that can be executed by the browser agent.
    The output needs to be only a single line of python code . No explaination needed. No comments needed. 
    Do not include ```python or ``` in the output.
    Do not include any other text in the output.
    Make sure to not repeat the same command again.
    If there is no more commands to execute return exit().
    If the task requests print then you need to output print() function to print the result.
    Do not use any loops in the output.

    For element specific commands such as gettingt the right text from the element.  
    Use the current page content to understand the structure of the page then look for the class name or id to find the right element.
    The page content is in the format of a string of HTML code.
    You need to find the right class to use the page.locator() function.

    Here are the commands the browser agent has already executed:
    {past_commands}

    Here is the task:
    {task}

    Current page content:
    {page_content}

    Output like this:
    await page.goto('https://news.ycombinator.com/'); await page.locator('a.storylink').first.click(); 
    is not acceptable. It should be a single command that can be executed by the browser agent.
    It should be like this:
    page.goto('https://news.ycombinator.com/');
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": task}
        ]
    )
    return response.choices[0].message.content

task = f"""Go to https://www.sec.gov/edgar/searchedgar/companysearch. Search for Nvidia. You will see a list of links for documents. 
We need to click at each and another page will open. Copy the link for all documents. I need the output which will be all the links on that page. 
After getting links for one page go back do same for next link."""







def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    
    current_command = plan_subtask_for_browser_agent(task)
    print(current_command)
    while current_command != "exit()":
        exec(current_command)
        past_commands.append(current_command)
        page_content = page.content()        
        current_command = plan_subtask_for_browser_agent(task)
        print(current_command)
    print("Browser agent has completed the task")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)