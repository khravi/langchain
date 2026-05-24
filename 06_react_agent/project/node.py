from dotenv import load_dotenv

from agent_reason_runnable import react_agent_runnable, tools
from define_state import AgentState

load_dotenv()


def reason_node(state: AgentState):
    # react_agent_runnable is a function (not a Runnable), so call it directly
    agent_outcome = react_agent_runnable(state)
    return {"agent_outcome": agent_outcome}


def act_node(state: AgentState):
    agent_action = state["agent_outcome"]

    # Extract tool name and input from AgentAction
    tool_name = agent_action.tool
    tool_input = agent_action.tool_input

    # Find the matching tool function
    tool_function = None
    for t in tools:
        if t.name == tool_name:
            tool_function = t
            break

    # Execute the tool with the input
    if tool_function:
        output = tool_function.invoke(tool_input)
    else:
        output = f"Tool '{tool_name}' not found"

    return {"intermediate_steps": [(agent_action, str(output))]}