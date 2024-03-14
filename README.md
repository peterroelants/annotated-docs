# Annotated Docs

Make use of Python type annotations to generate JSON Schemas compatible with the [OpenAI function calling API](https://platform.openai.com/docs/guides/function-calling) from your annotated functions.

Leverages:
- [pydantic](https://docs.pydantic.dev/latest/) for data validation and JSON schema generation.
- [typing module](https://docs.python.org/3/library/typing.html) for type annotations.
- [`typing.Annotated`](https://docs.python.org/3/library/typing.html#typing.Annotated) for and [`pydantic.Field`](https://docs.pydantic.dev/latest/concepts/fields/) for descriptions.


The main function is `annotated_docs.json_schema.as_json_schema` which takes a function as input and returns a json schema as output.


## Installation
Directly from this GitHub repo using pip:
```bash
pip install "annotated_docs @ git+https://git@github.com/peterroelants/annotated-docs.git@v0.0.4"
```


## Usage
For example to rewrite the `get_current_weather` function from the [OpenAI example](https://platform.openai.com/docs/guides/function-calling#:~:text=Example%20invoking%20multiple%20function%20calls%20in%20one%20response) using annotations:

```python
from typing import Annotated as A, Literal as L
from pydantic import BaseModel
from annotated_docs import doc as D

class Location(BaseModel):
    city: A[str, D("The city, e.g. San Francisco")]
    country: A[str, D("The country, e.g. USA")]

# Example Annotated dummy function
def get_current_weather(
    location: A[Location, D("Location to get the weather for.")],
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
  "parameters": {
    "$defs": {
      "Location": {
        "properties": {
          "city": {
            "description": "The city, e.g. San Francisco",
            "type": "string"
          },
          "country": {
            "description": "The country, e.g. USA",
            "type": "string"
          }
        },
        "required": [
          "city",
          "country"
        ],
        "type": "object"
      }
    },
    "properties": {
      "location": {
        "allOf": [
          {
            "$ref": "#/$defs/Location"
          }
        ],
        "description": "Location to get the weather for."
      },
      "unit": {
        "default": "fahrenheit",
        "enum": [
          "celsius",
          "fahrenheit"
        ],
        "type": "string"
      }
    },
    "required": [
      "location"
    ],
    "type": "object"
  },
  "description": "Get the current weather in a given location"
}
```

And we can call
```python
from annotated_docs import call_with_json

current_weather = call_with_json(get_current_weather, function_args_from_llm)
```

See [notebooks/examples/test_function_calling.ipynb](notebooks/examples/test_function_calling.ipynb) for a full example.
