import inspect
from collections.abc import Callable
from typing import Any, TypeVar

import pydantic
import pydantic.json_schema

T = TypeVar("T")


def doc(description) -> Any:
    """Annotate a variable with a description."""
    return pydantic.Field(description=description)


def as_json_schema(func: Callable) -> dict[str, Any]:
    """
    Return a JSON schema for the given function.
    """
    parameter_model = as_parameter_model(func)
    parameters_schema = parameter_model.model_json_schema(
        schema_generator=GenerateJsonSchemaNoTitle,
        mode="validation",
    )
    description = None
    if func.__doc__:
        description = inspect.cleandoc(func.__doc__).strip()
    schema_dct = dict(name=func.__name__, parameters=parameters_schema)
    if description:
        schema_dct["description"] = description
    return schema_dct


def as_parameter_model(func: Callable) -> pydantic.BaseModel:
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


def call(func: Callable, parameters_json: dict) -> Any:
    """
    Call the given function with the given parameters.
    Parameters are converted from JSON to Python using the function's parameter model.
    """
    parameter_model = as_parameter_model(func)
    parameters = parameter_model.model_validate(parameters_json)
    return func(**dict(parameters))


class GenerateJsonSchemaNoTitle(pydantic.json_schema.GenerateJsonSchema):
    def generate(
        self, schema, mode="validation"
    ) -> pydantic.json_schema.JsonSchemaValue:
        """
        This function takes a schema and a mode as input and returns a pydantic
        json schema value. It first calls the super class's generate method then
        removes the title from the generated json schema if it is present.

        Args:
            schema (): The `schema` input parameter is the PyDantic schema object
                that the function modifies and returns as a new JsonSchemaValue object.
            mode (str): The input parameter 'mode' sets what the generated schema
                will look like:
                   - By default 'mode' is set to 'validation', generating just
                those fields needed for client-side validation (i.e., those necessary
                to fulfil type hints of object being instanciated) and skipping
                properties included here by title only as these need not be
                client-validation dependent
                    or

        Returns:
            pydantic.json_schema.JsonSchemaValue: The function "generate" produces
            "JsonSchemaValue".

        """
        json_schema = super().generate(schema, mode=mode)
        if "title" in json_schema:
            del json_schema["title"]
        return json_schema

    def get_schema_from_definitions(
        self, json_ref
    ) -> pydantic.json_schema.JsonSchemaValue | None:
        """
        This function takes a JSON reference and returns a JSON Schema value or
        None. It modifies the schema by removing the "title" key if present.

        Args:
            json_ref (dict): The `json_ref` parameter passed to this function is
                the reference to the JSON schema being examined; the purpose of
                the parameter is to define the JSON data upon which
                get_schema_from_definitions() operates.

        Returns:
            pydantic.json_schema.JsonSchemaValue | None: The function returns a
            `pydantic.json_schema.JsonSchemaValue` object.

        """
        json_schema = super().get_schema_from_definitions(json_ref)
        if json_schema and "title" in json_schema:
            del json_schema["title"]
        return json_schema

    def field_title_should_be_set(self, schema) -> bool:
        """
        The given function "field_title_should_be_set" checks if the "title" field
        should be set or not based on the provided schema and returns a boolean
        value indicating whether the field should be set or not.

        Args:
            schema (): The `schema` input parameter is not used within the
                `field_title_should_be_set()` function at all. Therefore it does
                nothing.

        Returns:
            bool: Based on the given code snippet. The output returned by the
            `field_title_should_be_set` function is `False`.

        """
        return False
