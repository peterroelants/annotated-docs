import typing
from typing import Annotated as A

from annotated_docs import as_json_schema
from annotated_docs import doc as D
from pydantic import BaseModel, Field


def test_as_json_schema_no_annotations() -> None:
    """
    This function tests that a function without any annotations is properly converted
    to JSON Schema. Specifically:
    	- It defines a test function 'test_func'.
    	- It asserts that the JSON schema for 'test_func' has two properties: 'name'
    and 'parameters'.
    	- The 'name' property is set to the name of the function ('test_func.__name__').
    	- The 'parameters' property is an object with no additional properties.

    """
    def test_func():
        """
        Nothing; it does nothing. The `test_func()` function has no code within
        its bodies (i.e., between the `def` and `:` lines) and thus doesn't perform
        any actions when called.

        """
        pass

    assert as_json_schema(test_func) == {
        "name": test_func.__name__,
        "parameters": {
            "properties": {},
            "type": "object",
        },
    }


# Simple types #####################################################
def test_as_json_schema_simple() -> None:
    """
    This function tests whether `as_json_schema()` correctly serializes a Python
    function to a JSON schema object.

    """
    def test_func(a: int, b: str, c: float) -> str:
        """Test function"""
        return "hello"

    assert as_json_schema(test_func) == {
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


def test_as_json_schema_union() -> None:
    """
    This function checks whether `as_json_schema` correctly generates a JSON schema
    for a Python function with an argument of type `typing.Union[intstr]`.

    """
    def test_func(
        a: typing.Union[int, str],
    ) -> str:
        """Test function"""
        return "hello"

    assert as_json_schema(test_func) == {
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


def test_as_json_schema_union_pipe() -> None:
    """
    This function tests if a given function can be represented as a JSON schema
    using the `as_json_schema()` method and checks that the resulting schema
    accurately reflects the parameters of the function. Specifically it checks the
    parameters' types and whether they are required or not.

    """
    def test_func(
        a: int | str,
    ) -> str:
        """Test function"""
        return "hello"

    assert as_json_schema(test_func) == {
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


def test_as_json_schema_literal() -> None:
    """
    This function tests whether a given Python function can be converted to a JSON
    Schema object. Specifically:
    1/ It defines a sample function `test_func`.
    2/ It converts `test_func` into a JSON Schema using `as_json_schema`.
    3/ It compares the resulting JSON Schema object to a expected output to ensure
    that the conversion worked correctly.

    """
    def test_func(
        a: typing.Literal["b", "c"],
    ) -> str:
        """Test function"""
        return "hello"

    assert as_json_schema(test_func) == {
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


def test_as_json_schema_default() -> None:
    """
    This function checks if the 'as_json_schema' function is working as expected
    by testing it on a test function object and comparing its resulting JSON schema
    with an expected result.

    """
    def test_func(
        a: int = 1,
    ) -> str:
        """Test function"""
        return "hello"

    assert as_json_schema(test_func) == {
        "name": test_func.__name__,
        "description": "Test function",
        "parameters": {
            "properties": {
                "a": {"default": 1, "type": "integer"},
            },
            "type": "object",
        },
    }


def test_as_json_schema_maybe() -> None:
    """
    This function tests that a given Python function can be converted to a JSON schema.

    """
    def test_func(
        a: int | None,
    ) -> str:
        """Test function"""
        return "hello"

    assert as_json_schema(test_func) == {
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


def test_as_json_schema_optional() -> None:
    """
    This function tests the JSON schema representation of a Python function object
    as an optional integer using the `as_json_schema()` function.

    """
    def test_func(
        a: typing.Optional[int],
    ) -> str:
        """Test function"""
        return "hello"

    assert as_json_schema(test_func) == {
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


# Simple Types using Annotated #####################################
def test_as_json_schema_annotated() -> None:
    """
    This function takes an object type A with an integer attribute 'a' and a string
    description 'param a test', and tests that the JSON Schema of the given function
    is correctly generated as expected.

    """
    def test_func(
        a: A[int, D("param a test")],
    ) -> str:
        """Test function"""
        return "hello"

    assert as_json_schema(test_func) == {
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


def test_as_json_schema_annotated_literal() -> None:
    """
    This function tests whether a Python function's parameters and return type can
    be annotated with JSON schema definitions.

    """
    def test_func(
        a: A[typing.Literal["b", "c"], D("param a test")],
    ) -> str:
        """Test function"""
        return "hello"

    assert as_json_schema(test_func) == {
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


def test_as_json_schema_annotated_union() -> None:
    """
    This function tests the JSON schema for the given Python function using
    `as_json_schema()`. The JSON schema is constructed based on the function's
    parameters and description.

    """
    def test_func(
        a: A[int | str, D("param a test")],
    ) -> str:
        """Test function"""
        return "hello"

    assert as_json_schema(test_func) == {
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


# Pydantic #########################################################
def test_as_json_schema_pydantic() -> None:
    """
    This function tests that the given Python function can be serialized as a JSON
    schema using Pydantic. The function takes a TestModel object as an argument
    and returns a string. TheTestModel class is defined inside the function and
    has one attribute b of type int with a description "param b test". The function
    checks if the schema representation of the function with parameters matched
    what's expected based on the given signature.

    """
    class TestModel(BaseModel):
        b: A[int, Field(..., description="param b test")]

    def test_func(
        a: TestModel,
    ) -> str:
        """Test function"""
        return "hello"

    assert as_json_schema(test_func) == {
        "name": test_func.__name__,
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
        "description": "Test function",
    }
