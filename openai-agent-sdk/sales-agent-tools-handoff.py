from dotenv import load_dotenv
from agents import Agent, Runner, trace,function_tool
import asyncio

load_dotenv()



instruction1 = "You are a serious sales agent of a compliance company called ComplyAI and you write emails in a very serious tone"

instruction2 = "You are a funny sales agent of a compliance company called ComplyAI and you write emails in a very fun humorous tone"

instruction3 = "You are a busy sales agent of a compliance company called ComplyAI and you write emails in a very concise manner"

# Creating Sales Agent and then using them as tools for Sales Manager Agent
sales_agent1 = Agent(name="Sales Agent 1",instructions=instruction1, model="gpt-4o-mini")
tool1 = sales_agent1.as_tool(tool_name="sales_agent1", tool_description="Write a cold sales email")

sales_agent2 = Agent(name="Sales Agent 2",instructions=instruction1, model="gpt-4o-mini")
tool2 = sales_agent2.as_tool(tool_name="sales_agent2", tool_description="Write a cold sales email")

sales_agent3 = Agent(name="Sales Agent 3",instructions=instruction1, model="gpt-4o-mini")
tool3 = sales_agent3.as_tool(tool_name="sales_agent3", tool_description="Write a cold sales email")


# ---------------------------- End of Part 1: Sales Agents

subject_writer_instructions = f"""You are a subject writer and your job is to write the subject of the email. You will be given a topic and you need to write the subject of the email."""
html_writer_instructions = f"""You are a html writer and your job is to write the html of the email. You will be given a topic and you need to write the html of the email."""


subject_writer_agent = Agent(name="Subject Writer",instructions=subject_writer_instructions,model="gpt-4o-mini")
subject_writer_tool = subject_writer_agent.as_tool(tool_name="subject_writer", tool_description="Write the subject of the email")

html_writer_agent = Agent(name="HTML Writer",instructions=html_writer_instructions,model="gpt-4o-mini")
html_writer_tool = html_writer_agent.as_tool(tool_name="html_writer", tool_description="Write the html of the email")

email_writer_instructions = f"""You are a email writer.
You will receive the body of an email to be sent. You first use the subject_writer_tool to write the subject 
and then the html_writer_tool to write the body of the email. 
And then combine them for the output."""

email_writer_agent = Agent(name="Email Writer",
instructions=email_writer_instructions,
model="gpt-4o-mini",
tools=[subject_writer_tool,html_writer_tool],
handoff_description="Convert an email to HTML"
)
# ---------------------------- End of Part 2: Email Writer Agent


sales_manager_instructions = f"""You are a sales manager working for ComplAI. You use the tools given to you to generate cold sales emails. \
You never generate sales emails yourself, you always use the tools. \
You try all 3 sales agent tools at least once before choosing the best one. \
You can use the tools multiple times if you're not satisfied with the results from the first try. \
You select the single best email using your own judgement of which email will be most effective. \
After picking the email, you handoff to the Email Writer agent to format and send the email.=."""

sales_manager_agent = Agent(
    name="Sales Manager",
    instructions=sales_manager_instructions,
    model="gpt-4o-mini",
    tools=[tool1, tool2, tool3],
    handoffs=[email_writer_agent]
)


with trace("Sales Cold Email"):
    result = asyncio.run(Runner.run(sales_manager_agent, "Send a cold email to Anuj Gupta , Founder and CTO of AppX"))
    print(result.final_output)


