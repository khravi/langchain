# LangChain: Custom Runnables

## Core Concept
* A **Custom Runnable** allows you to inject arbitrary Python logic (any standard Python function) into a LangChain Expression Language (LCEL) chain.
* Because LCEL requires all components in a pipeline (`|`) to follow the `Runnable` protocol (meaning they have methods like `.invoke()`, `.stream()`, etc.), standard Python functions must be wrapped to become "Runnables" before they can be chained.

## When to Use Them
* **Data Transformation:** Modifying, cleaning, or formatting inputs before they reach the Prompt or LLM.
* **Routing:** Writing custom logic to decide which LLM or prompt to use based on the input.
* **External API Calls:** Fetching data from a non-LangChain tool or database mid-chain.
* **Debugging/Logging:** Adding a step in the chain that simply prints the current state of the data passing through.

## How to Create Them (Two Methods)
1. **`RunnableLambda`:** A class that explicitly wraps a Python function.
2. **`@chain` decorator:** Syntactic sugar that automatically converts a function into a runnable.

---

## Example Implementation

Here is how you can create and use custom runnables using both methods within a standard LCEL pipeline:

```python
from langchain_core.runnables import RunnableLambda, chain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# ---------------------------------------------------------
# Method 1: Using RunnableLambda (Explicit Wrapping)
# ---------------------------------------------------------
def clean_input(text: str) -> str:
    """A standard python function to clean whitespace and make text lowercase."""
    return text.strip().lower()

# Wrap the function to make it a compatible Runnable
cleaner_runnable = RunnableLambda(clean_input)


# ---------------------------------------------------------
# Method 2: Using the @chain decorator (Syntactic Sugar)
# ---------------------------------------------------------
@chain
def custom_formatter(ai_response: str) -> str:
    """Automatically becomes a runnable. Adds a custom prefix to the final output."""
    return f"🤖 Custom AI Output: {ai_response}"


# ---------------------------------------------------------
# Building the Pipeline
# ---------------------------------------------------------
prompt = PromptTemplate.from_template("Tell me a fact about {topic}")
model = ChatOpenAI(model="gpt-4")
parser = StrOutputParser()

# The custom runnables act just like standard LangChain components
my_chain = cleaner_runnable | prompt | model | parser | custom_formatter

# Execute the chain
# 1. 'cleaner_runnable' strips the spaces and lowers the text
# 2. 'prompt' formats the string
# 3. 'model' generates the fact
# 4. 'parser' extracts the string
# 5. 'custom_formatter' prepends the robot emoji
result = my_chain.invoke("   SPaCe ExPloRaTiOn   ")
print(result)

```