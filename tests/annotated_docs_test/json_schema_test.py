import typing
from typing import Annotated as A

from annotated_docs import as_json_schema
from annotated_docs import doc as D
from jsonschema import Draft202012Validator
from pydantic import BaseModel


def test_as_json_schema_no_annotations() -> None:
    """
    This function tests that the `as_json_schema()` function returns a valid JSON
    schema for a Python function without any annotations. It does this by creating
    a function object from the `test_func` definition and then using `as_json_schema()`
    to convert it into a JSON schema. The resulting schema is then checked using
    the `Draft202012Validator` class from the `pydantic` package to ensure that
    it is valid according to the JSON Schema specification.

    """
    def test_func():
        """
        Nothing; it does nothing and merely passes.

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
    This function defines a test function 'test_func', extracts its schema as a
    JSON schema and uses a validator to ensure that the schema is correct.

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
    This function tests a function schema that has been generated using the
    `as_json_schema()` method of a Python function. It verifies that the resulting
    JSON Schema matches the expected format and content for a Union type function.

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
    This function tests that a Python function can be serialized as a JSON schema
    and validates it using the `as_json_schema()` function and the `Draft202012Validator`.
    The function also checks the properties of the schema that is generated and
    compares them with expected values.

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
    This function tests that the given function can be converted to a JSON Schema
    and then uses the `Draft202012Validator` class from the `pydraft` library to
    validate the schema.

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
    This function tests that the function `test_func` can be converted to a JSON
    Schema without any issues. It asserts that the resulting schema is correct and
    passes some basic validity checks.

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
    This is a unit test for the `as_json_schema` decorator which checks if the
    given Python function can be represented as a JSON schema. The test function
    `test_func` has an integer argument `a` which is optional and the decorator
    generates a JSON schema for it. The schema confirms that `a` is an integer or
    None with an optional type and requires the "a" parameter.

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
    This function tests an arbitrary function's compatibility with JSON schema and
    asserts that the output is compatible with a schema representing an object
    with one parameter of type int or null.

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
    This function takes a Python function as an argument and returns its JSON
    schema annotated with information such as name ,description and parameters .

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
    This code tests the JSON Schema produced by `as_json_schema()` for a given
    Python function. It takes a function `test_func` as an argument and constructs
    the JSON Schema for that function using `as_json_schema()`. It then compares
    the constructed schema with expected values for the parameter "a" to check
    that the function was correctly annotated with literals and descriptions using
    Typing.

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
    This function defines a test function `test_func` with an annotated parameter
    `a` of type `A[int|str]` and checks the resulting JSON Schema matches expected
    schema.

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
    This is a PyDT unit test for `as_json_schema()` method of `pydantic` library
    by testing the case when function arguments and return value are validated
    using `BaseModel`. It also uses `Draft202012Validator` from `pydantic.orm.
    Validators` to validate the resulting JSON schema against draft 2020-12 standard.

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
