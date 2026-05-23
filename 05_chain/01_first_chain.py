from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv 
from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

# Check OpenAI API key is set
load_dotenv()  # Load environment variables from .env file

if os.getenv("OPENAI_API_KEY"):
    print("OpenAI API key is set.")
else:
    print("OpenAI API key is not set. Please set it in the .env file.")
    raise ValueError("OpenAI API key is not set. Please set it in the .env file.")


# Create first simple chain

# task 1: initiate the OpenAI LLM
llm_openai = ChatOpenAI(model="gpt-5.4-mini",temperature=0)


# task 2: define a chat prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an expert cook. Provide a recipe based on the main ingredient."),
    ("user", "{ingredient}") 
    ])

# task 3: Initialize output parser
output_parser = StrOutputParser()

# What output parser does is it takes the output from the LLM and converts it into a string format that we can easily work with in our code.
# This is especially useful when the LLM's response might be in a more complex format, and we want to ensure we have a clean string to work with for further processing or display.

# Create chain by combining the tasks using LECL operator
chain = prompt_template | llm_openai | output_parser

# task 4: invoke the chain with user input
response = chain.invoke(input={"ingredient": "chicken"})

print(response)

# # using runnable sequence to create the same chain
# chain_sequence = RunnableSequence(prompt_template, llm_openai, output_parser)
# response = chain_sequence.invoke(input={"ingredient": "chicken"})
# print(response)



