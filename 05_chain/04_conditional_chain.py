from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI
import os
from dotenv import load_dotenv 
from langchain_core.runnables import RunnableSequence, RunnableLambda, RunnableParallel, RunnableBranch
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel
from typing import Literal


# Check OpenAI API key is set
load_dotenv()  # Load environment variables from .env file

if os.getenv("OPENAI_API_KEY"):
    print("OpenAI API key is set.")
else:
    print("OpenAI API key is not set. Please set it in the .env file.")
    raise ValueError("OpenAI API key is not set. Please set it in the .env file.")

# initiate the OpenAI LLM
llm_openai = ChatOpenAI(model="gpt-5.4-mini",temperature=0)


class llm_schema(BaseModel):
    movie_summary_flag: Literal["positive", "negative"]

llm_structured_output = llm_openai.with_structured_output(llm_schema)

# TASK -1 [Prompt]
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a movie review evaluator"),
    ("human", "Please categorize the movie review as positive or negative : {input}")])

# TASK - 2 [LLM]
llm_structured_output = llm_openai.with_structured_output(llm_schema)


# TASK - 3 [Custom Runnable]
def pydantic_json(input:llm_schema)-> str:
    return input.model_dump()['movie_summary_flag']

pydantic_json_lambda = RunnableLambda(pydantic_json)

# Chain 1

# TASK - 1 [Prompt]

linkedin_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a LinkedIn post generator"),
    ("human", "Create a post for the following text for LinkedIn: {text}")])

# TASK - 2 [LLM]

llm_openai = ChatOpenAI(model="gpt-5-mini",temperature=0)

# TASK - 3 [Str Parser]

str_parser = StrOutputParser()

chain_linkedin = linkedin_prompt | llm_openai | str_parser

# Chain 2
def insta_chain(text:dict):

    text = text["text"]

    # TASK - 1 [Prompt]
    insta_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a LinkedIn post generator"),
    ("human", "Create a post for the following text for Instagram: {text}")])
    
    # TASK - 2 [LLM]
    llm_openai = ChatOpenAI(model="gpt-5-mini",temperature=0)

    # TASK - 3 [Str Parser]
    str_parser = StrOutputParser()

    chain_insta = insta_prompt | llm_openai | str_parser

    result = chain_insta.invoke(text)

    return result

insta_chain_runnable = RunnableLambda(insta_chain)


# Final Orchestration of the conditional chain
conditional_chain = RunnableBranch(
    (lambda x: "positive" in x, chain_linkedin),
     insta_chain_runnable
)

final_orchestrator = prompt_template | llm_structured_output | pydantic_json_lambda | conditional_chain

response = final_orchestrator.invoke({"input": "I loved this KGF movie"})

print(response)