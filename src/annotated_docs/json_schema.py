import inspect
from collections.abc import Callable
from typing import Any, TypeVar

import pydantic
import pydantic.json_schema

_RETURNS_KEY = "returns"

T = TypeVar("T")


def doc(description) -> Any:
    """Annotate a variable with a description."""
    return pydantic.Field(description=description)


def as_json_schema(func: Callable, include_returns: bool = False) -> dict[str, Any]:
    """
    Return a JSON schema for the given function.
    """
    parameters_schema = get_parameters_schema(func)
    schema_dct: dict[str, Any] = {"name": func.__name__}
    if func.__doc__:
        description = inspect.cleandoc(func.__doc__).strip()
        if description:
            schema_dct["description"] = description
    schema_dct["parameters"] = parameters_schema
    if include_returns:
        schema_dct[_RETURNS_KEY] = get_returns_schema(func)
    return schema_dct


def get_parameters_schema(func: Callable) -> dict[str, Any]:
    """Return a JSON schema for the parameters of the given function."""
    parameter_model = get_parameter_model(func)
    return parameter_model.model_json_schema(
        schema_generator=GenerateJsonSchemaNoTitle,
        mode="validation",
    )


def get_parameter_model(func: Callable) -> pydantic.BaseModel:
    """
    Return a Pydantic model for the parameters of the given function.
    """
    field_definitions: dict[str, tuple[Any, Any]] = {}
    for name, obj in inspect.signature(func).parameters.items():
        if obj.annotation == inspect.Parameter.empty:
            raise ValueError(
                f"`{func.__name__}` parameter `{name!s}` has no annotation, please provide an notation to be able to generate the function specification."
            )
        if obj.default == inspect.Parameter.empty:
            field_definitions[name] = (obj.annotation, pydantic.Field(...))
        else:
            field_definitions[name] = (obj.annotation, obj.default)
    _model_name = ""  # Empty model name
    return pydantic.create_model(_model_name, **field_definitions)  # type: ignore


def get_returns_schema(func: Callable) -> dict[str, Any]:
    """
    This function creates a JSON schema representing the returns of a given Callable
    function. It extracts the model from the function and generates a schema using
    the provided generator and mode. The resulting schema is returned without
    "required" or "type" attributes.

    Args:
        func (Callable): The `func` parameter is a callable function that is used
            to retrieve the returns model for the function. This returns model is
            then used to generate the JSON schema for the function's returns.

    Returns:
        dict[str, Any]: The output of this function is a dictionary containing the
        JSON schema for the returns of the given function.

    """
    returns_model = get_returns_model(func)
    return_schema = returns_model.model_json_schema(
        schema_generator=GenerateJsonSchemaNoTitle,
        mode="validation",
    )
    properties = return_schema.pop("properties")
    return_schema[_RETURNS_KEY] = properties[_RETURNS_KEY]
    if "required" in return_schema:
        del return_schema["required"]
    if "type" in return_schema:
        del return_schema["type"]
    return return_schema


def get_returns_model(func: Callable) -> pydantic.BaseModel:
    """
    Return a Pydantic model for the returns of the given function.
    """
    return_annotation = inspect.signature(func).return_annotation
    if return_annotation == inspect.Signature.empty:
        raise ValueError(
            f"`{func.__name__}` has no return annotation, please provide an annotation to be able to generate the function specification."
        )
    field_definitions: dict[str, tuple[Any, Any]] = {
        _RETURNS_KEY: (return_annotation, pydantic.Field(...))
    }
    _model_name = ""  # Empty model name
    return pydantic.create_model(_model_name, **field_definitions)  # type: ignore


def call(func: Callable, parameters_json: dict) -> Any:
    """
    Call the given function with the given parameters.
    Parameters are converted from JSON to Python using the function's parameter model.
    """
    parameter_model = get_parameter_model(func)
    # Validation: Convert JSON to Python using the parameter model
    parameters = parameter_model.model_validate(parameters_json)
    # Call with first layer of parameters as keyword arguments
    return func(**dict(parameters))


class GenerateJsonSchemaNoTitle(pydantic.json_schema.GenerateJsonSchema):
    def generate(
        self, schema, mode="validation"
    ) -> pydantic.json_schema.JsonSchemaValue:
        """
        This function generates a JSON Schema based on a given schema and removes
        the "title" field from the resulting schema if it's present.

        Args:
            schema (): The `schema` input parameter specifies the JSON schema that
                should be used to validate or generate the JSON data. It is passed
                to the `super()` method and used to create a Pydantic JSON Schema
                object that can be validated or generated.
            mode (str): The `mode` input parameter determines what kind of generation
                will be performed by the `generate()` function; two allowed modes
                are `"validation"` and something else. In its default state of
                `"validation"`, the function strips a title element from any
                resulting JSON Schema object.

        Returns:
            pydantic.json_schema.JsonSchemaValue: The function "generate" produces
            and returns a modified version of the JSON schema given as input.
            Specifically del title fields from JSON schema and returns new schema
            .  Therefore , the output returned by the function is pydantic.json_schema.JsonSchemaValue.

        """
        json_schema = super().generate(schema, mode=mode)
        if "title" in json_schema:
            del json_schema["title"]
        return json_schema

    def get_schema_from_definitions(
        self, json_ref
    ) -> pydantic.json_schema.JsonSchemaValue | None:
        """
        This function removes the "title" key from a JSON schema object that is
        generated from PyDAntic definitions.

        Args:
            json_ref (dict): The input `json_ref` is a JSON reference that passes
                a value of type 'json' to the `get_schema_from_definitions()`
                method of the object. This JSON reference can contain the schema
                data required to create an instance of Pydantic JSON Schema Value
                and is referenced inside the function to extract relevant fields
                needed by getting a new modified instance created through superclass
                functions without a title within its schema..

        Returns:
            pydantic.json_schema.JsonSchemaValue | None: The output of the given
            function is `pydantic.json_schema.JsonSchemaValue`.

        """
        json_schema = super().get_schema_from_definitions(json_ref)
        if json_schema and "title" in json_schema:
            del json_schema["title"]
        return json_schema

    def field_title_should_be_set(self, schema) -> bool:
        """
        This function takes a schema as input and returns a Boolean value indicating
        whether the field title should be set or not. It always returns false.

        Args:
            schema (): The input parameter 'schema' is not used at all within the
                provided function (field_title_should_be_set). Thus it has no
                effect on the functions behavior and serves only as a formality
                to allow the function to take the parameter but otherwise disregarded.

        Returns:
            bool: The output of the function `field_title_should_be_set()` is `False`.

        """
        return False
