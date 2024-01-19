import typing
from typing import Annotated as A

from annotated_docs.json_schema import as_json_schema


def test_as_json_schema_no_annotations() -> None:
    def test_func():
        pass

    assert as_json_schema(test_func) == {
        "name": test_func.__name__,
        "parameters": {
            "properties": {},
            "required": [],
            "type": "object",
        },
    }


def test_as_json_schema_simple() -> None:
    def test_func(a: int, b: str, c: float) -> str:
        """Test function"""
        return "hello"

    assert as_json_schema(test_func) == {
        "name": test_func.__name__,
        "description": "Test function",
        "parameters": {
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "string"},
                "c": {"type": "number"},
            },
            "required": ["a", "b", "c"],
            "type": "object",
        },
    }


def test_as_json_schema_annotated() -> None:
    def test_func(
        a: A[int, "param a test"],
    ) -> str:
        """Test function"""
        return "hello"

    assert as_json_schema(test_func) == {
        "name": test_func.__name__,
        "description": "Test function",
        "parameters": {
            "properties": {
                "a": {
                    "type": "number",
                    "description": "param a test",
                },
            },
            "required": ["a"],
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
                    "type": ["number", "string"],
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
                    "type": ["number", "string"],
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


def test_as_json_schema_annotated_literal() -> None:
    def test_func(
        a: A[typing.Literal["b", "c"], "param a test"],
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
        a: A[int | str, "param a test"],
    ) -> str:
        """Test function"""
        return "hello"

    assert as_json_schema(test_func) == {
        "name": test_func.__name__,
        "description": "Test function",
        "parameters": {
            "properties": {
                "a": {
                    "type": ["number", "string"],
                    "description": "param a test",
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
                "a": {"type": "number"},
            },
            "required": [],
            "type": "object",
        },
    }


def test_as_json_none() -> None:
    def test_func(
        a: None,
    ) -> str:
        """Test function"""
        return "hello"

    assert as_json_schema(test_func) == {
        "name": test_func.__name__,
        "description": "Test function",
        "parameters": {
            "properties": {
                "a": {"type": "null"},
            },
            "required": ["a"],
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
                "a": {"type": ["number", "null"]},
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
                "a": {"type": ["number", "null"]},
            },
            "required": ["a"],
            "type": "object",
        },
    }
