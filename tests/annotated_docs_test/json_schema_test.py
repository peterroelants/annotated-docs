import typing
from typing import Annotated as A

import jsonschema
from annotated_docs import as_json_schema
from annotated_docs import doc as D
from annotated_docs.json_schema import RETURNS_KEY
from pydantic import BaseModel


def test_as_json_schema_no_annotations() -> None:
    def test_func():
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
