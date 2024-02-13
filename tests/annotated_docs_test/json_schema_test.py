import typing
from typing import Annotated as A

from annotated_docs import as_json_schema
from annotated_docs import doc as D
from jsonschema import Draft202012Validator
from pydantic import BaseModel


def test_as_json_schema_no_annotations() -> None:
    """
    This function tests a Python function as a JSON schema with no annotations.
    It converts the function to a JSON schema and checks that it is valid using
    the `Draft202012Validator`. The function merely has a single test that assesses
    that the schema object should only contain three properties—"name," "type,"
    and "properties."

    """
    def test_func():
        """
        The `test_func()` function does nothing; it has no instructions or statements
        inside the `pass` statement. In other words., it is an empty function.

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
    This function takes a Python function as an argument and converts it into a
    JSON Schema.

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
    This function takes a typing. Union[int str] arg and tests the returned value
    matches the schema created from the test_func.

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
    This code creates a JSON schema representing a function test_func taking
    argument 'a', which can be of type integer or string using Union type ( pipe
    ). Then it checks the schema validity using draft 2020-12 validator

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
    This function tests whether the `as_json_schema()` method correctly converts
    a Python function into a JSON Schema. It checks that the resulting schema has
    the expected properties and type for the input function's parameters.

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
    This function takes a Python function as an argument and converts it into a
    JSON Schema object. The JSON Schema object contains information about the
    function's name and description as well as its parameters and data types.

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
    This is a unit test that tests the `as_json_schema` function to convert a
    Python function into a JSON schema. It creates an example function with an
    optional integer parameter and verifies that the generated JSON schema accurately
    describes the parameter's type and constraint (allowing either an integer or
    null).

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
    This function tests the JSON schema representation of a Python function by
    checking that the schema's parameters and type definitions match the function's
    parameter and return types.

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
    This function tests whether a given Python function is annotated with the
    `as_json_schema` decorator and checks if the generated JSON schema matches the
    expected structure.

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
    This function takes a decorator `as_json_schema` that converts the given Python
    function into a JSON schema. The function returns the converted JSON schema
    of the given Python function.

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
    This function tests whether a given Python function can be serialized to a
    JSON Schema by using the `as_json_schema()` method from the `typing` module
    and then checking that the resulting JSON Schema is correct. The test function
    used is a simple function taking an argument of type `A[int | str]` which is
    an annotation of a parameter that can be either an integer or a string.

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
    This function creates a JSON Schema for a Python function and checks its
    validity using PyDantic's BaseModel and Draft202012Validator.

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
