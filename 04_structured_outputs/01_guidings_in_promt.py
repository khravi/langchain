import os
from dotenv import load_dotenv 
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import PromptTemplate

# Check OpenAI API key is set
load_dotenv()  # Load environment variables from .env file

if os.getenv("OPENAI_API_KEY"):
    print("OpenAI API key is set.")
else:
    print("OpenAI API key is not set. Please set it in the .env file.")
    raise ValueError("OpenAI API key is not set. Please set it in the .env file.")

# initiate the OpenAI LLM
llm_openai = ChatOpenAI(model="gpt-5.4-mini",temperature=0)

# Guiding the output format using instructions in the prompt
# Here, we are asking the model to generate a joke in a specific key-value pair format with keys "setup" and "punchline". This helps in structuring the output in a predictable way, making it easier to parse and use in applications.
template = ("Tell me a joke. Generate the output in key-value pair format with the following keys: setup, punchline")

response = llm_openai.invoke(template).content
print(response)
