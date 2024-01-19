import inspect
import types
import typing
from collections.abc import Callable
from typing import (
    Annotated,
    Any,
    NotRequired,
    TypedDict,
    TypeVar,
)

T = TypeVar("T")
AnnotatedToStr = Callable[[Annotated[Any, ...]], str]


class PropertySchema(TypedDict):
    type: str | list[str]
    description: NotRequired[str]
    enum: NotRequired[list[str]]


class ParametersSchema(TypedDict):
    type: str
    properties: dict[str, PropertySchema]
    required: list[str]


class FunctionSchema(TypedDict):
    name: str
    description: NotRequired[str]
    parameters: ParametersSchema


def as_json_schema(func: Callable) -> FunctionSchema:
    """Generate a json schema from a function signature."""
    parameters_properties: dict[str, PropertySchema] = {}
    parameters_required: list[str] = []
    for name, obj in inspect.signature(func).parameters.items():
        if obj.annotation == inspect.Parameter.empty:
            raise ValueError(
                f"`{func.__name__}` parameter `{name!s}` has no annotation, please provide an annotation to be able to generate the function specification."
            )
        parameters_properties[name] = parse_annotation(obj.annotation)
        if obj.default == inspect.Parameter.empty:
            parameters_required.append(name)
    doc_string = inspect.getdoc(func)
    function_schema: FunctionSchema = {
        "name": func.__name__,
        "description": doc_string or "",
        "parameters": {
            "type": "object",
            "properties": parameters_properties,
            "required": parameters_required,
        },
    }
    if doc_string is None:
        del function_schema["description"]
    return function_schema


def ann2str(ann: Annotated[Any, ...]) -> str:
    return "; ".join([str(a) for a in ann.__metadata__])


def parse_annotation(
    annotation: type, ann2str: AnnotatedToStr = ann2str
) -> PropertySchema:
    """Parse annotation to json schema"""
    if annotation is None or annotation is types.NoneType:
        return {"type": "null"}
    elif typing.get_origin(annotation) is typing.Annotated:
        origin_parsed: PropertySchema = parse_annotation(annotation.__origin__)  # type: ignore
        origin_parsed["description"] = ann2str(annotation)
        return origin_parsed
    elif typing.get_origin(annotation) in (typing.Union, types.UnionType):
        union_types = [
            t
            for a in annotation.__args__  # type: ignore
            for t in _as_list(parse_annotation(a)["type"])
        ]
        return {"type": _dedup(union_types)}
    elif typing.get_origin(annotation) is typing.Literal:
        return {"type": "string", "enum": list(annotation.__args__)}  # type: ignore
    elif issubclass(annotation, list) or typing.get_origin(annotation) is list:
        return {"type": "array"}
    elif issubclass(annotation, dict) or typing.get_origin(annotation) is dict:
        return {"type": "object"}
    elif type(annotation) is type:
        if issubclass(annotation, str):
            return {"type": "string"}
        elif issubclass(annotation, int):
            return {"type": "number"}
        elif issubclass(annotation, float):
            return {"type": "number"}
        elif issubclass(annotation, bool):
            return {"type": "boolean"}
    raise ValueError(f"Unknown annotation {annotation}")


def _as_list(maybe_list: list[T] | T) -> list[T]:
    if isinstance(maybe_list, list):
        return maybe_list
    else:
        return [maybe_list]


def _dedup(items: list[T]) -> list[T]:
    """Remove duplicates from a list while preserving order."""
    # Python 3.7+ preserves insertion order for dictionaries
    return list(dict.fromkeys(items))
