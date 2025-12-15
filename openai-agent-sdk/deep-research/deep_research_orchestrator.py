from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content
import os
from dotenv import load_dotenv
from deep_research_planner import planner_agent
from deep_research_writer import writer_agent
from deep_research_search_agent import search_agent
from agents import Runner, trace, function_tool, Agent
import asyncio

load_dotenv()

sg = SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))

async def plan_searches(query):
    print(f"Planning searches for query: {query}")
    planner_result = await Runner.run(planner_agent, query)
    print(f"Will perform {len(planner_result.final_output.search_items)} searches")
    return planner_result.final_output.search_items

async def perform_searches(search_items):
    print(f"Call search for each item")
    search_results = []
    tasks = [asyncio.create_task(search_item_on_web(search_item)) for search_item in search_items]
    results = await asyncio.gather(*tasks)    
        
    return results

async def search_item_on_web(search_item):
    print(f"Searching web for query: {search_item.query}")
    input = f"Search the web for the following term: {search_item.query} and Reason for searching: {search_item.reason}"
    search_result = await Runner.run(search_agent, input)
    print(f"Search result: {search_result.final_output}")
    return search_result.final_output

async def write_report(query, search_results):
    print(f"Write report")
    input = f"Write a report based on the following search results: {search_results} for the query: {query}"
    print(f"Input: {input}")
    report_result = await Runner.run(writer_agent, input)
    print(f"Report result: {report_result.final_output}")
    return report_result.final_output


@function_tool
def send_email(subject: str, html_body: str):
    """
    Send an HTML email using SendGrid.
    
    Args:
        subject: The email subject line
        html_body: The HTML content of the email body
    """
    # print(f"Sending email {subject} {html_body}")
    # content = Content(type="text/html", value=html_body)
    html_content = """
    <html>
    <body>
        <h2 style="color: blue">Welcome</h2>
        <p>This is a sample message with HTML.</p>
        <p>You can add <strong>bold text</strong>, images, links and more.</p>
    </body>
    </html>
    """
    message = Mail(
        from_email=os.getenv('SENDGRID_FROM_EMAIL'),
        to_emails=os.getenv('SENDGRID_TO_EMAIL'),
        subject=subject,
        html_content=html_body
    )
    # message = Mail(
    #     from_email=os.getenv('SENDGRID_FROM_EMAIL'),
    #     to_emails=os.getenv('SENDGRID_TO_EMAIL'),
    #     subject=subject,
    #     html_content=body
    # )
    try:
        print("Sending email")
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
        return False
    return {"status": "success"}

email_agent = Agent(
    name="Email Agent",
    instructions="You are able to send a nicely formatted HTML email based on a text . You will be provied a text . You should use your tool to send one email providing the text converted in to clearn, well presented HTML with an appropriate subject line.",
    model="gpt-4o-mini",
    tools=[send_email]
)


query = "what are some of the research areas where voice ai agent startups are spending the most money in 2025"

with trace("Deep Research Orchestrator"):
    print("Starting Deep Research Orchestrator")
    search_plan = asyncio.run(plan_searches(query))
    print(f"Search plan: {search_plan}")
    search_results = asyncio.run(perform_searches([search_plan[0],search_plan[1]]))
    print(f"Search results: {search_results}")
    report = asyncio.run(write_report(query, search_results))
    # print(f"Report: {report}")
    asyncio.run(Runner.run(email_agent, report.markdown_report))
    # print("Deep Research Orchestrator completed")