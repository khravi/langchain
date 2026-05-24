from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv 
import datetime
from langchain_core.tools import tool
from langchain_tavily.tavily_search import TavilySearch
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage

# Check OpenAI API key is set
load_dotenv()  # Load environment variables from .env file

if os.getenv("OPENAI_API_KEY"):
    print("OpenAI API key is set.")
else:
    print("OpenAI API key is not set. Please set it in the .env file.")
    raise ValueError("OpenAI API key is not set. Please set it in the .env file.")

# initiate the OpenAI LLM
llm_openai = ChatOpenAI(model="gpt-5.4-mini", temperature=0)


# Define current system time tool
@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """Returns the current system time formatted according to the provided format string."""
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time

# define search tool
search_tool = TavilySearch(search_depth="basic")

tools = [get_system_time, search_tool]

# Bind tools to the LLM (this tells the model about available tools
# but does NOT create a full agent loop — our graph handles the loop)
llm_with_tools = llm_openai.bind_tools(tools)

# System prompt for the ReAct agent
react_system_prompt = """Answer the following questions as best you can.
You have access to tools that you can use to look up information or get the current time.
Always think step by step before taking an action.

Begin!"""


def react_agent_runnable(state):
    """Call the LLM with tools and return AgentAction or AgentFinish.
    
    This is the 'reasoning' step: the LLM decides whether to call a tool
    (AgentAction) or return a final answer (AgentFinish).
    """
    # Build the message history from state
    messages = [SystemMessage(content=react_system_prompt)]
    messages.append(HumanMessage(content=state["input"]))

    # Replay intermediate steps as tool-call / tool-response pairs
    for i, (action, observation) in enumerate(state.get("intermediate_steps", [])):
        tool_call_id = f"call_{i}"
        messages.append(AIMessage(
            content="",
            tool_calls=[{
                "id": tool_call_id,
                "name": action.tool,
                "args": action.tool_input if isinstance(action.tool_input, dict) else {"__arg1": action.tool_input},
            }],
        ))
        messages.append(ToolMessage(content=str(observation), tool_call_id=tool_call_id))

    # Call the LLM
    response = llm_with_tools.invoke(messages)

    # Parse response: tool_calls → AgentAction, otherwise → AgentFinish
    if response.tool_calls:
        tc = response.tool_calls[0]
        return AgentAction(
            tool=tc["name"],
            tool_input=tc["args"],
            log=response.content or f"Calling {tc['name']}",
        )
    else:
        return AgentFinish(
            return_values={"output": response.content},
            log=response.content,
        )
