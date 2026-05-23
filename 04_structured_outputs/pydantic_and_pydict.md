# Structured Output in LangChain: Pydantic vs TypedDict

## Overview

When building LangChain applications, you need to structure language model outputs in predictable formats. Two main approaches are:

1. **Pydantic**: A powerful data validation library with runtime validation and type safety
2. **TypedDict**: A lightweight Python typing construct for structured dictionaries

This guide compares both approaches and when to use each in LangChain.

---

## Pydantic

### What is Pydantic?

Pydantic is a data validation and settings management library in Python that uses Python type annotations to validate and parse data at runtime. 

In the context of LangChain, Pydantic can be used to define structured output formats for language model responses. By using Pydantic models, developers can ensure that the output from the language model adheres to a specific schema with built-in validation.

This is particularly useful when you want to extract specific information from the model's response or when you want to enforce a certain format and validate constraints on the output.

### Why Use Pydantic in LangChain?

1. **Structured Output**: Pydantic allows you to define structured output formats for language model responses. This ensures that the data you receive from the model is in a predictable format, making it easier to process downstream.

2. **Data Validation**: Pydantic provides powerful data validation capabilities. You can define constraints on the data, such as types, ranges, formats, and custom validators. This helps catch errors early and ensure data quality.

3. **Improved Developer Experience**: Using Pydantic provides clear and concise definitions of the expected output format. This makes it easier for developers to understand what fields are available and what types they should expect.

4. **Integration with LangChain**: Pydantic integrates seamlessly with LangChain via the `.with_structured_output()` method, allowing you to leverage validation and parsing capabilities within the framework.

5. **Field Documentation**: The `Field` class provides descriptions and default values, making your schemas self-documenting.

### Pydantic Example in LangChain

```python
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

# Define a Pydantic model for movie information
class Movie(BaseModel):
    title: str = Field(..., description="The title of the movie")
    director: str = Field(..., description="The director of the movie")
    release_year: int = Field(..., description="The year the movie was released")

# Bind the model to the LLM for structured output
llm = ChatOpenAI(model="gpt-4")
llm_with_structured = llm.with_structured_output(Movie)

# Invoke and get structured response
response = llm_with_structured.invoke("Tell me about the movie KGF")
print(response.title)        # Type-safe access
print(response.director)
print(response.release_year)
```

---

## TypedDict

### What is TypedDict?

TypedDict is a Python typing construct (from the `typing` module) that allows you to define the structure of dictionaries with type hints. It provides type checking at development time but does not perform runtime validation.

In LangChain, TypedDict can be used as a lightweight alternative to Pydantic when you want structured outputs without the overhead of runtime validation.

### Why Use TypedDict in LangChain?

1. **Lightweight**: TypedDict is part of Python's standard `typing` module - no external dependencies required.

2. **Simple Type Hints**: Provides clear type information for developers without extra validation logic.

3. **Good for Simple Schemas**: Works well when you have straightforward data structures that don't need validation.

4. **Lower Overhead**: Minimal performance impact compared to Pydantic's validation.

5. **IDE Support**: Excellent autocomplete and type checking in modern IDEs and type checkers like mypy.

### TypedDict Example in LangChain

```python
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser

# Define a TypedDict for structured output
class MovieInfo(TypedDict):
    title: str
    director: str
    release_year: int

# Use with LangChain
llm = ChatOpenAI(model="gpt-4")
parser = JsonOutputParser(pydantic_object=MovieInfo)

response = llm.invoke("Tell me about the movie KGF")
# Manual parsing needed (TypedDict doesn't validate at runtime)
movie_data = parser.parse(response.content)
print(movie_data["title"])
print(movie_data["director"])
```

---

## Comparison: Pydantic vs TypedDict

| Feature | Pydantic | TypedDict |
|---------|----------|-----------|
| **Runtime Validation** | ✅ Yes | ❌ No |
| **External Dependency** | ✅ Required | ❌ Built-in |
| **Type Safety** | ✅ Full (runtime + IDE) | ✅ IDE only |
| **Error Messages** | ✅ Detailed validation errors | ❌ None (dict accepted) |
| **Default Values** | ✅ Supported | ⚠️ Limited support |
| **Custom Validators** | ✅ Yes (via @validator) | ❌ No |
| **Documentation/Descriptions** | ✅ Yes (Field descriptions) | ❌ No |
| **Complexity** | Medium | Low |
| **Learning Curve** | Moderate | Very Low |
| **LangChain Integration** | ✅ Native support | ⚠️ Requires JSON parser |

---

## When to Use Each in LangChain

### Use Pydantic When:

1. **You need runtime validation** - When the LLM output must meet specific constraints (ranges, formats, patterns)
2. **Complex data structures** - Working with nested objects, lists, or intricate schemas
3. **Error handling** - You want detailed validation error messages
4. **Production applications** - Building robust systems where data quality is critical
5. **Field descriptions matter** - You want self-documenting schemas with descriptions

**Example Use Case**: Extracting customer information from unstructured text where you must validate email formats, age ranges, and required fields.

```python
from pydantic import BaseModel, Field, validator
from langchain_openai import ChatOpenAI

class Customer(BaseModel):
    name: str = Field(..., description="Customer full name")
    email: str = Field(..., description="Valid email address")
    age: int = Field(..., ge=0, le=150, description="Customer age")
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v

llm = ChatOpenAI(model="gpt-4")
llm_structured = llm.with_structured_output(Customer)
response = llm_structured.invoke("Extract customer info from this text...")
```

### Use TypedDict When:

1. **Simple, flat structures** - Working with basic key-value pairs
2. **No validation needed** - The LLM output is generally reliable and doesn't need constraints
3. **Minimal dependencies** - You want to avoid adding external packages
4. **Type hints only** - You primarily need IDE support and static type checking
5. **Quick prototyping** - Building proof-of-concepts or MVPs

**Example Use Case**: Simple metadata extraction where you just need to capture basic fields.

```python
from typing import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser

class ArticleMetadata(TypedDict):
    title: str
    author: str
    publication_date: str

llm = ChatOpenAI(model="gpt-4")
parser = JsonOutputParser(pydantic_object=ArticleMetadata)
response = llm.invoke("Extract article metadata and return as JSON...")
```

---

## Key Takeaway

- **Pydantic is best for production LangChain applications** requiring data validation, complex schemas, and robust error handling.
- **TypedDict is best for simple use cases** where you need type hints without runtime validation overhead.

For most LangChain projects dealing with structured outputs, **Pydantic is the recommended choice** due to its seamless LangChain integration and comprehensive validation capabilities.
