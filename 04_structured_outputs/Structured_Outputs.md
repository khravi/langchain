# Structured Outputs in LangChain

Structured Outputs in LangChain means forcing or guiding an LLM to return responses in a fixed and predictable format instead of free-form text.

Instead of getting random natural language, you get outputs like:

1. JSON
2. Python dictionaries
3. Pydantic models
4. Typed objects
5. Tool/function call responses

## Why Structured Outputs Are Important

Normally, LLMs generate text freely.

Example without structure:

```txt
The customer name is Ravi and the order id is 1234.
```

This is hard for applications to reliably parse.

With structured outputs:
```json
{
  "customer_name": "Ravi",
  "order_id": 1234
}
```
Now programs, APIs, databases, and agents can directly use the response.

## Main Uses of Structured Outputs
### 1. API Integration

Applications need data in proper format.

Example:
```json
{
  "city": "Bangalore",
  "temperature": 30
}
```
instead of paragraph text.

### 2. AI Agents

Agents in LangGraph or LangChain need structured state updates.

Example:
```json
{
    "task": "search weather",
    "status": "completed"
}
```
### 3. Database Storage

Structured data can directly go into:

    SQL databases
    MongoDB
    Vector DB metadata
    CSV/Excel

### 4. Workflow Automation

Useful in:

    Approval systems
    Ticketing systems
    BOM agents
    ETL pipelines
    Azure workflows
    ADF pipelines

### 5. Reliable Multi-Step Chains

Each chain step expects a known schema.

Example:

    Step 1 -> Extract entities
    Step 2 -> Classify sentiment
    Step 3 -> Save results

All steps require predictable outputs.

## Types of Structured Outputs in LangChain
### 1. JSON Output

Simplest structure.

Example:
``` json
{
  "name": "Ravi",
  "age": 25
}
```
Use Cases
    APIs
    Frontend apps
    Automation

### 2. Pydantic Structured Output

Most commonly used in modern LangChain.

Uses Python classes for validation.

Example:

from pydantic import BaseModel
``` py
class Person(BaseModel):
    name: str
    age: int
```
LLM output becomes validated Python object.

    Benefits
    Type safety
    Validation
    Cleaner code
    Error handling


### 3. TypedDict Output

Uses Python typing.

Example:
``` py
from typing import TypedDict

class Person(TypedDict):
    name: str
    age: int

```
### Benefits
    Lightweight
    Good for simple workflows

### 4. Tool Calling / Function Calling

LLM generates structured arguments for tools.

Example:
```json
{
  "tool": "get_weather",
  "arguments": {
    "city": "Bangalore"
  }
}
```
### Used In
    AI Agents
    LangGraph
    OpenAI tools
    Automation systems
### 5. Output Parsers

LangChain provides parsers to enforce formatting.

Examples:

    JsonOutputParser
    PydanticOutputParser
    StructuredOutputParser
    Common Structured Output Components in LangChain

### A. Output Parser

Converts raw LLM text into structured data.

Example:

```py
parser.parse(response)
```
### B. Response Schema

Defines expected fields.

Example:
    ```py
    name: str
    age: int
    ```

### C. Validation

Checks correctness.

Example:
 ```json
    age must be integer
    email must contain @
```