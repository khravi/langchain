from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI
import os
from dotenv import load_dotenv 
from langchain_core.runnables import RunnableSequence, RunnableLambda, RunnableParallel
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

# initiate the OpenAI LLM
llm_openai = ChatOpenAI(model="gpt-5.4-mini",temperature=0)

# TASK -1 [Prompt]

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a movie reviewer. Provide a brief review based on the movie name."),
    ("human", "Please provide a brief review of the movie {input}:")])


# TASK - 2 [LLM]
llm_openai = ChatOpenAI(model="gpt-5-mini",temperature=0)

# TASK - 3 [Str Parser]
str_parser = StrOutputParser()

# TASK - 4 [Custom Runnable]
def dictionary_maker(text:str)-> dict:
    return {"text" : text}

dictionary_maker_runnable = RunnableLambda(dictionary_maker)


# parallel chain 1 - Insta post
# TASK - 1 [Template For Post]
insta_post = ChatPromptTemplate.from_messages(
    messages=[
        ("system", "You're a social media post generator. "),
        ("human", "Create movie review post for Instagram: {text}"),
    ]
)

# taks 2: Genrate social media post from the film review
llm_openai_Insta_post = ChatOpenAI(model="gpt-5.4-mini",temperature=0)

# Task 3 - Output parser for the post
output_parser_post = StrOutputParser()

instagram_chain = insta_post | llm_openai_Insta_post | output_parser_post

#parallel chain 2 - LinkedIn post
# TASK - 1 [Template For Post]
linkedin_post = ChatPromptTemplate.from_messages(
    messages=[
        ("system", "You're a social media post generator. "),
        ("human", "Create movie review post for LinkedIn: {text}"),
    ]
)

# taks 2: Genrate social media post from the film review
llm_openai_linkedin_post = ChatOpenAI(model="gpt-5.4-mini",temperature=0)

# Task 3 - Output parser for the post
output_parser_linkedin_post = StrOutputParser()

linkedin_chain = linkedin_post | llm_openai_linkedin_post | output_parser_linkedin_post


#Final Orchestration of the parallel chain
# Create chain by combining the tasks using LECL operator

final_chain = (
    prompt_template | llm_openai | str_parser | dictionary_maker_runnable | 
    RunnableParallel({"instagram": instagram_chain, "linkedin": linkedin_chain})
    )

response = final_chain.invoke({"input": "KGF"})

print("This is the Instagram Post:", response["instagram"], end="\n\n")

print("This is the LinkedIn Post:", response["linkedin"], end="\n\n")
