import os
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# 2. Define the Tools
# Tool A: Real-world web search tool for live data
web_search_tool = TavilySearchResults(max_results=2)

# Tool B: Custom mathematical tool for the agent to use
@tool
def calculate_percentage_change(old_value: float, new_value: float) -> str:
    """
    Calculates the percentage change between two numbers. 
    Useful for financial, population, or statistical analysis.
    """
    change = ((new_value - old_value) / old_value) * 100
    return f"The percentage change is {change:.2f}%"

# Combine tools into a list
tools = [web_search_tool, calculate_percentage_change]

# 3. Initialize the LLM (Must be a model that supports Tool Calling)
llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0)

# 4. Create the ReAct Agent using LangGraph

# We provide a system prompt to guide its behavior via the state_modifier
system_instruction = """
You are an expert Data Analyst and Research Assistant. 
When asked to compare historical vs current data, always:
1. Search the web for the exact figures.
2. Use your calculation tool to find the exact percentage change.
3. Present the final answer clearly to the user.
"""

agent_executor = create_agent(
    llm, 
    tools,
    system_prompt=system_instruction
)

# 5. Execute the Agentic Workflow
if __name__ == "__main__":
    # A complex query requiring multiple steps: Search -> Calculate -> Respond
    query = "What was the population of India, Karnataka in 2010 compared to 2023? What is the exact percentage change?"
    print(f"User Query: {query}\n")
    print("-" * 50)
    
    # We stream the events to observe the Thought -> Action -> Observation loop
    events = agent_executor.stream(
        {"messages": [("user", query)]}, 
        stream_mode="values"
    )
    
    for event in events:
        # Get the latest message in the state memory
        message = event["messages"][-1]
        
        if message.type == "ai":
            if message.tool_calls:
                # The agent decided to take an ACTION
                for tc in message.tool_calls:
                    print(f"🧠 THOUGHT/ACTION: Agent decided to call '{tc['name']}'")
                    print(f"   Arguments: {tc['args']}\n")
            elif message.content:
                # The agent has reached a FINAL ANSWER
                print(f"✅ FINAL ANSWER:\n{message.content}")
                
        elif message.type == "tool":
            # The OBSERVATION from the real world
            # Truncated for terminal readability
            print(f"🔍 OBSERVATION (Tool Output): {message.content[:150]}...\n")