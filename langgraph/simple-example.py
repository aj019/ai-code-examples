from langchain.tools import tool
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain.messages import AnyMessage, SystemMessage, ToolMessage, HumanMessage
from typing import Annotated, TypedDict, Dict
from IPython.display import Image, display
import operator

import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

model = init_chat_model(
    "gpt-4o-mini",
    temperature=0
)

#DEfine tools

@tool
def add(a:float, b:float) -> float:
    """ Add two numbers together
        Args: 
        a : the first number
        b : the second number
    """
    return a + b


@tool
def multiply(a:float, b:float) -> float:
    """ Multiply two numbers together
        Args: 
        a : the first number
        b : the second number
    """
    return a * b


tools = [add, multiply]

tools_by_name = {tool.name: tool for tool in tools}

model_with_tools = model.bind_tools(tools)


# This state will be shared by the whole graph including all nodes
class MessageState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int


def llm_call(state: Dict):
    """ LLM Decides whether to call a tool or not """

    return {
        "messages": [
            model_with_tools.invoke([
                SystemMessage(content="You are a helpful assistant that can use tools to help the user."),
            ] + state["messages"])
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

def tool_node(state: Dict):
    """ Perform's the tool call and returns the result """

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}

# Conditional Edge Function to decide whether to continue the graph or not
def should_continue(state: Dict):
    """ Decides whether to continue the graph or not """
    
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tool_node"
    else:
        return END

# Let's build the agent graph

agent_builder = StateGraph(MessageState)

agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)


agent_builder.add_edge(START, "llm_call")

agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node", END]
)

agent_builder.add_edge("tool_node", "llm_call")

agent = agent_builder.compile()

# # Show the agent
# print(display(Image(agent.get_graph(xray=True).draw_ascii())))

# image_bytes = agent.get_graph().draw_mermaid_png()

# # Save the bytes to a file
# with open("langgraph_flow.png", "wb") as f:
#     f.write(image_bytes)

# print("Graph saved as langgraph_flow.png")

result = agent.invoke({"messages": [HumanMessage(content="What is pi * (2 + 1)")]})
print("Total LLM Calls", result["llm_calls"])
for m in result["messages"]:
    m.pretty_print()


