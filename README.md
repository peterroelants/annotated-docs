# Annotated Docs

Make use of Python type annotations to generate JSON Schemas compatible with the [OpenAI function calling API](https://platform.openai.com/docs/guides/function-calling) from your annotated functions.

Leverages:
- [typing module](https://docs.python.org/3/library/typing.html) for type annotations.
- [typing.Annotated](https://docs.python.org/3/library/typing.html#typing.Annotated) for descriptions.
- [typing.Literal](https://docs.python.org/3/library/typing.html#typing.Literal) for enum values.


The main function is `annotated_docs.json_schema.as_json_schema` which takes a function as input and returns a json schema as output.


## Installation
Directly from this GitHub repo using pip:
```bash
pip install git+https://git@github.com/peterroelants/annotated-docs.git@v0.0.1
```


## Usage
For example to rewrite the `get_current_weather` function from the [OpenAI example](https://platform.openai.com/docs/guides/function-calling#:~:text=Example%20invoking%20multiple%20function%20calls%20in%20one%20response) using annotations:

```python
from typing import Annotated as A, Literal as L

# Example Annotated dummy function
def get_current_weather(
    location: A[str, "The city and state, e.g. San Francisco, CA"],
    unit: L["celsius", "fahrenheit"] = "fahrenheit",
) -> str:
    """Get the current weather in a given location"""
    ...
```

We can generate the json schema for this function using `as_json_schema`:
```python
from annotated_docs.json_schema import as_json_schema
print(as_json_schema(get_current_weather))
```

Resulting in:
```json
{
  "name": "get_current_weather",
  "description": "Get the current weather in a given location",
  "parameters": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "The city and state, e.g. San Francisco, CA"
      },
      "unit": {
        "type": "string",
        "enum": [
          "celsius",
          "fahrenheit"
        ]
      }
    },
    "required": [
      "location"
    ]
  }
}
```
