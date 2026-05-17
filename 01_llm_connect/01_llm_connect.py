from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv 

# Check OpenAI API key is set
load_dotenv()  # Load environment variables from .env file

if os.getenv("OPENAI_API_KEY"):
    print("OpenAI API key is set.")
else:
    print("OpenAI API key is not set. Please set it in the .env file.")
    raise ValueError("OpenAI API key is not set. Please set it in the .env file.")

# initiate the OpenAI LLM
llm_openai = ChatOpenAI(model="gpt-5.4-mini",temperature=0)

#Invoke the LLM with a prompt
response = llm_openai.invoke("What is the capital of France?").content
print(response)