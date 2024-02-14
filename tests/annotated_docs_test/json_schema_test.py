import typing
from typing import Annotated as A

import jsonschema
from annotated_docs import as_json_schema
from annotated_docs import doc as D
from annotated_docs.json_schema import RETURNS_KEY
from pydantic import BaseModel


def test_as_json_schema_no_annotations() -> None:
    """
    This function tests the `as_json_schema()` function by taking a Python function
    object as input and converts it into a JSON Schema object. It then checks that
    the resulting JSON Schema object has the correct format and contents.

    """
    def test_func():
        """
        This function does nothing. It has no statements or side effects and only
        contains a pass statement. Therefore it has no effect and serves no purpose.

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
    jsonschema.Draft202012Validator.check_schema(schema)


# Simple types #####################################################
def test_as_json_schema_simple() -> None:
    """
    This function defines a test function 'test_func', converts it into a JSON
    schema using 'as_json_schema' and checks the validity of the resulting schema
    using the 'jsonschema.Draft202012Validator' module.

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
    This function tests the JSON schema representation of a Python function using
    the `as_json_schema` method and then validates it against the JSON Schema specification.

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
    This function tests that the `as_json_schema()` function correctly generates
    a JSON schema from a Python function by validating the generated schema against
    a reference schema.

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
    This function tests a function's parameters as JSON Schema to ensure it conforms
    to a specific structure.

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
    This function takes a Python function as an argument and returns its JSON
    schema by using the `as_json_schema()` method. The JSON schema includes
    information such as the function name description parameters types etc.

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
    jsonschema.Draft202012Validator.check_schema(schema)


def test_as_json_schema_maybe() -> None:
    """
    This function takes a Python function as an argument and converts it to a JSON
    schema. The schema includes information about the function's name , description
    and parameters and their types . Then , it uses the JSON Schema validator to
    check that the schema is well - formed

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
    This function defines a test function and converts it to a JSON Schema using
    the `as_json_schema` decorator. It then asserts that the resulting schema is
    correct and checks it against the validator of the JSON schema draft 2020-12.

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
    This function takes a Python function as an argument and converts it into a
    JSON schema. It then validates the schema using the `jsonschema` library.

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
    This function defines a test function 'test_func' and then converts the function
    into a JSON Schema using 'as_json_schema()'. The JSON schema is then validated
    using the 'jsonschema.Draft202012Validator'.

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
    This function tests the JSON Schema for a Python function 'test_func'. The
    schema represents the function's parameters and returns a dictionary containing
    information about the function such as name , description , parameter details
    and other attributes

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
    This is a test function that creates a JSON schema object for the purpose of
    testing against Py Dantic's JSON schema implementation using as_json_schema
    decorator on the provided function and asserts that it validates correctly
    when passed through Py Dantic validation mechanism.

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


# Test returns #####################################################
def test_as_json_schema_include_returns_simple() -> None:
    """
    This code checks whether the JSON schema generated for a given Python function
    is valid using the `jsonschema` library.

    """
    def test_func(a: int, b: float) -> str:
        """Test function"""
        return "hello"

    # Check schema
    schema = as_json_schema(test_func, include_returns=True)
    assert schema == {
        "name": test_func.__name__,
        "description": "Test function",
        "parameters": {
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "number"},
            },
            "required": ["a", "b"],
            "type": "object",
        },
        "returns": {"type": "string"},
    }
    jsonschema.Draft202012Validator.check_schema(schema)
    # Call function and test output
    result = test_func(a=1, b=2.0)
    jsonschema.validate(instance=result, schema=schema[RETURNS_KEY])


def test_as_json_schema_include_returns_pydantic() -> None:
    """
    This unit test is using `pydantic` to check that a given Python function can
    be validated as JSON Schema including returns type by comparing it against the
    generated JSON schema.

    """
    class TestModel(BaseModel):
        """Test model description"""

        b: A[int, D("param b test")]

    def test_func(
        a: int,
    ) -> A[TestModel, D("return test")]:
        """Test function"""
        return TestModel(b=a * 2)

    schema = as_json_schema(test_func, include_returns=True)
    assert schema == {
        "name": test_func.__name__,
        "description": "Test function",
        "parameters": {
            "properties": {
                "a": {"type": "integer"},
            },
            "required": ["a"],
            "type": "object",
        },
        "returns": {
            "$defs": {
                "TestModel": {
                    "description": "Test model description",
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
            "allOf": [{"$ref": "#/$defs/TestModel"}],
            "description": "return test",
        },
    }
    jsonschema.Draft202012Validator.check_schema(schema)
    # Call function and test output
    result: TestModel = test_func(a=1)
    jsonschema.validate(instance=result.model_dump(), schema=schema[RETURNS_KEY])
