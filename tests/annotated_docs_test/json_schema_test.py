import typing
from typing import Annotated as A

from annotated_docs import as_json_schema
from annotated_docs import doc as D
from pydantic import BaseModel, Field


def test_as_json_schema_no_annotations() -> None:
    def test_func():
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
