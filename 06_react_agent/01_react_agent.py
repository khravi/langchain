from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain.tools import tool
from langchain.agents import create_agent


# Check OpenAI API key is set
load_dotenv()  # Load environment variables from .env file

if os.getenv("OPENAI_API_KEY"):
    print("OpenAI API key is set.")
else:
    print("OpenAI API key is not set. Please set it in the .env file.")
    raise ValueError("OpenAI API key is not set. Please set it in the .env file.")

# initiate the OpenAI LLM
llm_openai = ChatOpenAI(model="gpt-5.4-mini", temperature=0, max_completion_tokens=1000, timeout=30)

# define Tools
# Tool -1
search_tool = DuckDuckGoSearchRun(description="Use this tool to search the web for up-to-date information.")

# Tool -2
wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(),description="This is a tool to search Wikipedia")

@tool
def enterprise_tool(query:str) -> str:
     """This is a tool to send emails to employees"""
    # define email sending logic here using SMTP gmail
     return "Email Sent"

ToolKit = [search_tool, wikipedia_tool, enterprise_tool]

agent = create_agent(model=llm_openai, tools=ToolKit)

example_query = {"messages": [("user", "What is the capital of India and send an email to all employees about it ?")]}


events = agent.stream(
    example_query,
    stream_mode="values",
)
for event in events:
    event["messages"][-1].pretty_print()

