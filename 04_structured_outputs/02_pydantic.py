import os
from dotenv import load_dotenv 
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Check OpenAI API key is set
load_dotenv()  # Load environment variables from .env file

if os.getenv("OPENAI_API_KEY"):
    print("OpenAI API key is set.")
else:
    print("OpenAI API key is not set. Please set it in the .env file.")
    raise ValueError("OpenAI API key is not set. Please set it in the .env file.")

# initiate the OpenAI LLM
llm_openai = ChatOpenAI(model="gpt-5.4-mini",temperature=0)

# using pydantic models to structure the output of the LLM
# To use pydantic models, we need to define a class that inherits from BaseModel. Each attribute of the class will represent a field in the structured output, and we can use Field to provide additional metadata for each field.
# In this example, we will create a pydantic model for a movie, which includes the title, director, and release year.

# import the pydantic library and define the Movie class as follows:
class Movie(BaseModel):
    title: str = Field(..., description="The title of the movie")
    director: str = Field(..., description="The director of the movie")
    release_year: int = Field(..., description="The year the movie was released")

# Bind the Movie pydantic model to the LLM to get structured output
llm_with_structured = llm_openai.with_structured_output(Movie)

# Create a prompt template that instructs the LLM to generate movie information
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a movie expert. Provide information about the movie in structured format."),
        ("user", "Please provide information about the movie '{movie_title}'.")
    ]
)

# Format the prompt with the movie title and invoke the LLM
response = llm_with_structured.invoke(prompt_template.format(movie_title="KGF"))

# The response is now a Movie object with structured data
print(f"Title: {response.title}")
print(f"Director: {response.director}")
print(f"Release Year: {response.release_year}")

# parse the response into a Movie object
print(response)

