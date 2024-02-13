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
    This function gets a schema for the returns of a Callable and creates a modified
    version of that schema without title or required fields and with the _RETURNS_KEY
    added.

    Args:
        func (Callable): The `func` parameter is the function being analyzed.

    Returns:
        dict[str, Any]: The output of the get_returns_schema function is a JSON
        schema that describes the structure of the returns value generated by the
        given Python callable.

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
        This function deletes the "title" key from the JSON schema object returned
        by super() and returns it.

        Args:
            schema (dict): The schema input parameter is the JSON Schema being
                used to generate the documentation for the API. It contains the
                definition of the API's endpoints and the parameters they expect.
                The function takes the schema as an argument and uses it to create
                the documentation for the API.
            mode (str): The `mode` input parameter determines whether to create a
                JSON schema for validation or not; one of two possible values can
                be passed as the argument value: "validation" or Nothing.

        Returns:
            pydantic.json_schema.JsonSchemaValue: The function generates a JSON
            schema without the 'title' key. The output is a JsonSchemaValue object.

        """
        json_schema = super().generate(schema, mode=mode)
        if "title" in json_schema:
            del json_schema["title"]
        return json_schema

    def get_schema_from_definitions(
        self, json_ref
    ) -> pydantic.json_schema.JsonSchemaValue | None:
        """
        This function takes a JSON reference and removes the "title" key from the
        resulting JSON schema generated by `pydantic.get_schema_from_definitions()`.
        It then returns the modified schema or `None` if no schema is found.

        Args:
            json_ref (): The `json_ref` parameter is a reference to a JSON object
                that contains the definitions for the Python module being described
                by the `pydantic.json_schema`. This object allows you to retrieve
                the schema from an external source instead of embedding it directly
                within the code.

        Returns:
            pydantic.json_schema.JsonSchemaValue | None: The output of this function
            will be the original `json_schema` without the `"title"` key.

        """
        json_schema = super().get_schema_from_definitions(json_ref)
        if json_schema and "title" in json_schema:
            del json_schema["title"]
        return json_schema

    def field_title_should_be_set(self, schema) -> bool:
        """
        This function checks if the field title should be set to false for a given
        schema. It returns False by default.

        Args:
            schema (None): The schema input parameter is ignored; the function
                always returns False regardless of what value it's passed.

        Returns:
            bool: Based on the code provided - the output would be 'False'

        """
        return False
