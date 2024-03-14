import typing
from typing import Annotated as A

import jsonschema
from annotated_docs import as_json_schema
from annotated_docs import doc as D
from pydantic import BaseModel


def test_as_json_schema_no_annotations() -> None:
    """
    converts a Python function to a JSON schema and verifies that the resulting
    schema matches expected properties and types.

    """
    def test_func():
        pass

    schema = as_json_schema(test_func)
    assert schema == {
        "name": test_func.__name__,
        "description": "",
        "parameters": {
            "properties": {},
            "type": "object",
        },
    }
    jsonschema.Draft202012Validator.check_schema(schema)


# Simple types #####################################################
def test_as_json_schema_simple() -> None:
    """
    generates a JSON schema for a function given as an argument. It returns the
    schema in a dictionary, along with various information such as name, description,
    parameters, and type.

    """
    def test_func(a: int, b: str, c: float) -> str:
        """Test function"""
        return "hello"

    schema = as_json_schema(test_func)
    assert schema == {
        "name": test_func.__name__,
        "description": "Test function",
        "parameters": {
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "string"},
                "c": {"type": "number"},
            },
            "required": ["a", "b", "c"],
            "type": "object",
        },
    }
    jsonschema.Draft202012Validator.check_schema(schema)


def test_as_json_schema_union() -> None:
    """
    generates a JSON schema representation of a function `test_func`. The resulting
    schema includes the function name, description, and parameters with type annotations.

    """
    def test_func(
        a: typing.Union[int, str],
    ) -> str:
        """Test function"""
        return "hello"

    schema = as_json_schema(test_func)
    assert schema == {
        "name": test_func.__name__,
        "description": "Test function",
        "parameters": {
            "properties": {
                "a": {
                    "anyOf": [
                        {"type": "integer"},
                        {"type": "string"},
                    ]
                },
            },
            "required": ["a"],
            "type": "object",
        },
    }
    jsonschema.Draft202012Validator.check_schema(schema)


def test_as_json_schema_union_pipe() -> None:
    """
    generates a JSON schema representation of a given Python function, which can
    be used for validating input data using the `jsonschema` library.

    """
    def test_func(
        a: int | str,
    ) -> str:
        """Test function"""
        return "hello"

    schema = as_json_schema(test_func)
    assert schema == {
        "name": test_func.__name__,
        "description": "Test function",
        "parameters": {
            "properties": {
                "a": {
                    "anyOf": [
                        {"type": "integer"},
                        {"type": "string"},
                    ]
                },
            },
            "required": ["a"],
            "type": "object",
        },
    }
    jsonschema.Draft202012Validator.check_schema(schema)


def test_as_json_schema_literal() -> None:
    """
    generates high-quality documentation for code by converting a Python function
    into a JSON Schema literal.

    """
    def test_func(
        a: typing.Literal["b", "c"],
    ) -> str:
        """Test function"""
        return "hello"

    schema = as_json_schema(test_func)
    assert schema == {
        "name": test_func.__name__,
        "description": "Test function",
        "parameters": {
            "properties": {
                "a": {
                    "type": "string",
                    "enum": ["b", "c"],
                },
            },
            "required": ["a"],
            "type": "object",
        },
    }
    jsonschema.Draft202012Validator.check_schema(schema)


def test_as_json_schema_default() -> None:
    """
    generates a JSON schema representation of a function, in this case `test_func`,
    based on its parameter and return types. It then checks if the generated schema
    validates correctly using the `Draft202012Validator`.

    """
    def test_func(
        a: int = 1,
    ) -> str:
        """Test function"""
        return "hello"

    schema = as_json_schema(test_func)
    assert schema == {
        "name": test_func.__name__,
        "description": "Test function",
        "parameters": {
            "properties": {
                "a": {
                    "default": 1,
                    "type": "integer",
                },
            },
            "type": "object",
        },
    }
    jsonschema.Draft202012Validator.check_schema(schema)


def test_as_json_schema_maybe() -> None:
    """
    converts a function to JSON schema for validation. It generates a schema that
    includes the function name, description, and parameter types. The `check_schema()`
    method validates the schema against the function implementation.

    """
    def test_func(
        a: int | None,
    ) -> str:
        """Test function"""
        return "hello"

    schema = as_json_schema(test_func)
    assert schema == {
        "name": test_func.__name__,
        "description": "Test function",
        "parameters": {
            "properties": {
                "a": {
                    "anyOf": [
                        {"type": "integer"},
                        {"type": "null"},
                    ]
                }
            },
            "required": ["a"],
            "type": "object",
        },
    }
    jsonschema.Draft202012Validator.check_schema(schema)


def test_as_json_schema_optional() -> None:
    """
    defines a JSON schema for a test function with a single optional parameter
    `a`, which can be an integer or `null`.

    """
    def test_func(
        a: typing.Optional[int],
    ) -> str:
        """Test function"""
        return "hello"

    schema = as_json_schema(test_func)
    assert schema == {
        "name": test_func.__name__,
        "description": "Test function",
        "parameters": {
            "properties": {
                "a": {
                    "anyOf": [
                        {"type": "integer"},
                        {"type": "null"},
                    ]
                }
            },
            "required": ["a"],
            "type": "object",
        },
    }
    jsonschema.Draft202012Validator.check_schema(schema)


# Simple Types using Annotated #####################################
def test_as_json_schema_annotated() -> None:
    """
    generates a JSON schema for a function based on its definition, and checks
    that the schema conforms to the JSON Schema specification using the `jsonschema.Draft202012Validator`.

    """
    def test_func(
        a: A[int, D("param a test")],
    ) -> str:
        """Test function"""
        return "hello"

    schema = as_json_schema(test_func)
    assert schema == {
        "name": test_func.__name__,
        "description": "Test function",
        "parameters": {
            "properties": {
                "a": {
                    "type": "integer",
                    "description": "param a test",
                },
            },
            "required": ["a"],
            "type": "object",
        },
    }
    jsonschema.Draft202012Validator.check_schema(schema)


def test_as_json_schema_annotated_literal() -> None:
    """
    defines a schema for a function that takes a string parameter "a" and returns
    a string.

    """
    def test_func(
        a: A[typing.Literal["b", "c"], D("param a test")],
    ) -> str:
        """Test function"""
        return "hello"

    schema = as_json_schema(test_func)
    assert schema == {
        "name": test_func.__name__,
        "description": "Test function",
        "parameters": {
            "properties": {
                "a": {
                    "type": "string",
                    "enum": ["b", "c"],
                    "description": "param a test",
                },
            },
            "required": ["a"],
            "type": "object",
        },
    }
    jsonschema.Draft202012Validator.check_schema(schema)


def test_as_json_schema_annotated_union() -> None:
    """
    generates a JSON schema representation of the `test_func` function, including
    its name, description, and parameter types.

    """
    def test_func(
        a: A[int | str, D("param a test")],
    ) -> str:
        """Test function"""
        return "hello"

    schema = as_json_schema(test_func)
    assert schema == {
        "name": test_func.__name__,
        "description": "Test function",
        "parameters": {
            "properties": {
                "a": {
                    "anyOf": [
                        {"type": "integer"},
                        {"type": "string"},
                    ],
                    "description": "param a test",
                },
            },
            "required": ["a"],
            "type": "object",
        },
    }
    jsonschema.Draft202012Validator.check_schema(schema)


# Pydantic #########################################################
def test_as_json_schema_pydantic() -> None:
    """
    generates a JSON schema representation of the `test_func` function based on
    its definition, and validates it using the `jsonschema.Draft202012Validator`.

    """
    class TestModel(BaseModel):
        b: A[int, D("param b test")]

    def test_func(
        a: TestModel,
    ) -> str:
        """Test function"""
        return "hello"

    schema = as_json_schema(test_func)
    assert schema == {
        "name": test_func.__name__,
        "description": "Test function",
        "parameters": {
            "$defs": {
                "TestModel": {
                    "properties": {
                        "b": {
                            "description": "param b test",
                            "type": "integer",
                        }
                    },
                    "required": ["b"],
                    "type": "object",
                }
            },
            "properties": {"a": {"$ref": "#/$defs/TestModel"}},
            "required": ["a"],
            "type": "object",
        },
    }
    jsonschema.Draft202012Validator.check_schema(schema)
