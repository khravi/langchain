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