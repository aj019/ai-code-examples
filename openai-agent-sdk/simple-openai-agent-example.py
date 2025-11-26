from dotenv import load_dotenv
from agents import Agent, Runner, trace
import os
import asyncio

load_dotenv()


agent = Agent(name="Jokestar", instructions="You are a joke teller", model="gpt-4o-mini")

print(agent)

with trace("Telling a Joke"):
    result = asyncio.run(Runner.run(agent, "Tell me a joke on ai agents"))
    print(result.final_output)




