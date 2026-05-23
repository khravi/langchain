md_content = """# ReAct Agent in LangChain

## Core Concept
**ReAct** stands for **Re**asoning and **Act**ing. It is an agentic framework that prompts a Large Language Model (LLM) to alternate between thinking about a problem and taking action to solve it. Instead of just guessing an answer, a ReAct agent breaks a prompt down, figures out what information it is missing, and uses external tools to find that information.

## The ReAct Loop
When you give a ReAct agent a task, it enters a continuous loop until it solves the problem:

1. **Thought:** The LLM reasons about what it needs to do next based on the user's prompt or previous steps.
2. **Action:** The LLM decides to use a specific tool from its provided toolkit (e.g., a web search, a calculator, a database query) and generates the input for it.
3. **Observation:** The tool executes and returns real-world data back to the LLM.
4. **Repeat / Final Answer:** The agent analyzes the observation. If it has the final answer, it stops and responds to the user. If not, it generates a new "Thought" and repeats the loop.

## Key Advantages
* **Reduced Hallucinations:** Because the agent relies on "Observations" from actual tools rather than just its internal memory, it is much more accurate.
* **Transparency:** You can see exactly *how* the model arrived at its answer by reading its "Thoughts" and "Actions". 
* **Multi-step Problem Solving:** It excels at complex queries that require chaining multiple actions together.

## Python Example (Using LangGraph)
In modern LangChain, ReAct agents are highly optimized and built using LangGraph. Here is a basic example of setting up a ReAct agent with a custom tool:

```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# 1. Define the tools the agent can use
@tool
def get_weather(location: str) -> str:
    \"\"\"Returns the weather for a given location.\"\"\"
    # In a real app, this would call a real weather API
    if "bengaluru" in location.lower():
        return "The weather in Bengaluru is 28°C and partly cloudy."
    return f"The weather in {location} is 72°F and sunny."

# 2. Initialize the LLM (must support tool calling)
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 3. Create the ReAct agent
tools = [get_weather]
agent_executor = create_react_agent(llm, tools)

# 4. Run the agent
inputs = {"messages": [("user", "What is the weather in Bengaluru?")]}
response = agent_executor.invoke(inputs)

# Print the final response
print(response["messages"][-1].content)
```