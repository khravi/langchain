# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv

# load_dotenv()  # Load environment variables from .env file

# llm_google = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0)

# response = llm_google.invoke("What is the capital of India")

# # print(response.content)

# print(response.generations[0][0].text)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv 
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_community.tools import TavilySearchResults, tool
import datetime

# Check OpenAI API key is set
load_dotenv()  # Load environment variables from .env file

if os.getenv("OPENAI_API_KEY"):
    print("OpenAI API key is set.")
else:
    print("OpenAI API key is not set. Please set it in the .env file.")
    raise ValueError("OpenAI API key is not set. Please set it in the .env file.")

# initiate the OpenAI LLM
llm_openai = ChatOpenAI(model="gpt-5.4-mini",temperature=0)
#llm_openai = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0)

@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """Returns the current system time formatted according to the provided format string."""

    current_time = datetime.datetime.now()
    # getting not attribute error for datetime for above linre. Correct it


    formatted_time = current_time.strftime(format)
    return formatted_time

search_tool = TavilySearchResults(search_depth = "basic")

tools = [search_tool, get_system_time]

model = ChatOpenAI(
    model="gpt-5.4-mini", 
    temperature=0,
    max_completion_tokens=1000,
    timeout=30)

agent = create_agent(model=model, tools=tools)

# response = agent.invoke({"messages": [{"role": "user", "content": "When was SpaceX's last launch and how many days ago was that from this instant?"}]})

# print(response)

question = {"messages": [{"role": "user", "content": "When was SpaceX's last launch and how many days ago was that from this instant?"}]}

events = agent.stream(
    question,
    stream_mode="values",
)

for event in events:
    event["messages"][-1].pretty_print()

