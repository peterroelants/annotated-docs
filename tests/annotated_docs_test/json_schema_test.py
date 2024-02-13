import typing
from typing import Annotated as A

from annotated_docs import as_json_schema
from annotated_docs import doc as D
from jsonschema import Draft202012Validator
from pydantic import BaseModel


def test_as_json_schema_no_annotations() -> None:
    """
    This function takes a Python function as input and converts it into a JSON
    Schema. It returns the JSON schema for the function without any annotations.
    The function also includes some additional metadata about the schema.

    """
    def test_func():
        """
        Nothing. The function simply passes without doing anything.

        """
        pass

    schema = as_json_schema(test_func)
    assert schema == {
        "name": test_func.__name__,
        "parameters": {
            "properties": {},
            "type": "object",
        },
    }
    Draft202012Validator.check_schema(schema)


# Simple types #####################################################
def test_as_json_schema_simple() -> None:
    """
    This function tests the JSON schema produced by `as_json_schema()` by validating
    it against a set of expected properties and types using the `Draft202012Validator`.

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
    Draft202012Validator.check_schema(schema)


def test_as_json_schema_union() -> None:
    """
    This code defines a function 'test_func' that takes an argument 'a' of type
    Union[int ,str]. It then creates a json schema from the test function using
    the 'as_json_schema() method and asserts that the resulting schema matches
    certain expected properties . Finally , it validates the schema using
    'Draft202012Validator. check_ schema()'.

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
    Draft202012Validator.check_schema(schema)


def test_as_json_schema_union_pipe() -> None:
    """
    This function takes a Python function as an argument and converts it to a JSON
    schema. The function is called 'test_func' and takes an argument 'a' of type
    int or str. The resulting schema is a JSON object with the name of the function
    and its description and parameter details including anyOf containing integer
    and string types for 'a' which is a required parameter.

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
    Draft202012Validator.check_schema(schema)


def test_as_json_schema_literal() -> None:
    """
    This function tests a Python function using the `as_json_schema` library to
    convert it into a JSON schema and checks whether the resulting schema is valid
    according to the JSON Schema specification.

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
    Draft202012Validator.check_schema(schema)


def test_as_json_schema_default() -> None:
    """
    This function tests a given function's compatibility with the JSON schema draft
    of the year 2020 (Draft 2020-12) using `as_json_schema()`. It checks that the
    parameters have type `object`, a property 'a' of `integer` defaulted to 1 and
    a valid schema description and name.

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
                "a": {"default": 1, "type": "integer"},
            },
            "type": "object",
        },
    }
    Draft202012Validator.check_schema(schema)


def test_as_json_schema_maybe() -> None:
    """
    This function tests the JSON schema created by `as_json_schema` and validates
    it using the `Draft202012Validator`. The schema represents a test function
    that takes an integer or null as input and returns a string.

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
    Draft202012Validator.check_schema(schema)


def test_as_json_schema_optional() -> None:
    """
    This function creates a JSON Schema for the provided function test_func and
    then checks that the schema is valid using the Draft 2020-12 Validator.

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
    Draft202012Validator.check_schema(schema)


# Simple Types using Annotated #####################################
def test_as_json_schema_annotated() -> None:
    """
    This function tests a Python function's parameters and type as a JSON schema
    and annotates it.

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
    Draft202012Validator.check_schema(schema)


def test_as_json_schema_annotated_literal() -> None:
    """
    This code defines a test function `test_func` with one parameter `a` of type
    string with allowed values "b" or "c". It then creates a JSON schema from the
    function using the `as_json_schema()` method and checks that the schema is valid.

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
    Draft202012Validator.check_schema(schema)


def test_as_json_schema_annotated_union() -> None:
    """
    This function defines a test function 'test_func' with input parameter 'a'
    that can be of type integer or string and checks if the schema for this function
    matches the expected JSON schema using as_json_schema() function from the
    ajsonSchema module

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
    Draft202012Validator.check_schema(schema)


# Pydantic #########################################################
def test_as_json_schema_pydantic() -> None:
    """
    This function converts a Python function into a JSON schema.

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
    Draft202012Validator.check_schema(schema)
