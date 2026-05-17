from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv 
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Check OpenAI API key is set
load_dotenv()  # Load environment variables from .env file

if os.getenv("OPENAI_API_KEY"):
    print("OpenAI API key is set.")
else:
    print("OpenAI API key is not set. Please set it in the .env file.")
    raise ValueError("OpenAI API key is not set. Please set it in the .env file.")

# initiate the OpenAI LLM
llm_openai = ChatOpenAI(model="gpt-5.4-mini",temperature=0)

#Messages
 #SystemMessage is used to set the behavior of the assistant
 #HumanMessage is used to represent the user's input
 #AIMessage is used to represent the assistant's response
 
my_messages =[
    SystemMessage(content = "You are a helpful assistant."),  #SystemMessage is used to set the behavior of the assistant
    HumanMessage(content = "What is the capital of India?") #HumanMessage is used to represent the user's input
]

# Invoke the LLM with a list of messages
response = llm_openai.invoke(my_messages).content
print(response)
