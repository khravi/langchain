import os
from dotenv import load_dotenv 
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate

# Check OpenAI API key is set
load_dotenv()  # Load environment variables from .env file

if os.getenv("OPENAI_API_KEY"):
    print("OpenAI API key is set.")
else:
    print("OpenAI API key is not set. Please set it in the .env file.")
    raise ValueError("OpenAI API key is not set. Please set it in the .env file.")

# initiate the OpenAI LLM
llm_openai = ChatOpenAI(model="gpt-5.4-mini",temperature=0)

# define a chat prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a {tone} assistant."),
    ("user", "Write fun facts about {topic}.")
])

# Get input from user (tone and topic)
tone = input("Enter the tone for the assistant (e.g., friendly, formal): ")
topic = input("Enter a topic for the fun facts: ")

# format the prompt
ready_prompt =  prompt_template.format(tone=tone, topic=topic)

# invoke the LLM with the formatted prompt
response = llm_openai.invoke(ready_prompt).content

print(response)