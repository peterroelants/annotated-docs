import inspect
from collections.abc import Callable
from typing import Any, Final, TypeVar

import pydantic
import pydantic.json_schema

RETURNS_KEY: Final[str] = "returns"

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
        schema_dct[RETURNS_KEY] = get_returns_schema(func)
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
    This function takes a function object as input and returns its return value
    schema as a dict using the models' JSON schema generation functionality to
    create it with no title.

    Args:
        func (Callable): The `func` input parameter is a callable that represents
            the Python function for which the schema is being generated.

    Returns:
        dict[str, Any]: The function returns a schema dictionary containing
        information about the expected inputs to and outputs from a Python function.
        Specifically it takes an func callable object as input and then retrieves
        info about its returns via gets Returns Model func calls the result which
        is just a standard SchemaModel object without its metadata attached as
        returned as dictionary object having 3 key-value pairs (pop ,__ and Iter)
        . Lastly required is removed and type removed only if of Object .

    """
    returns_model = get_returns_model(func)
    return_schema = returns_model.model_json_schema(
        schema_generator=GenerateJsonSchemaNoTitle,
        mode="validation",
    )
    properties = return_schema.pop("properties")
    return_schema |= properties[RETURNS_KEY]
    if "required" in return_schema:
        del return_schema["required"]
    if "type" in return_schema and return_schema["type"] == "object":
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
        RETURNS_KEY: (return_annotation, pydantic.Field(...))
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
        This function removes the "title" key from a JSON Schema generated by a
        superclass's `generate()` method with the specified mode.

        Args:
            schema (str): The `schema` input parameter takes a PyStruct schema as
                an argument and returns its parsed form for further generation of
                a JSON Schema file using PyDantic. It is utilized to specify the
                schema to be used for generation and provides necessary information
                to create a correct JSON Schema file based on provided structure
                and mode (either validation or full).
            mode (str): The mode input parameter is used to specify whether to run
                the schema generation with validation or not. By default it runs
                with "validation" but it can be set to none for example if we don't
                want any checks but only raw JSON generation.

        Returns:
            pydantic.json_schema.JsonSchemaValue: The output returned by this
            function is a Pydantic JSON SchemaValue object.

        """
        json_schema = super().generate(schema, mode=mode)
        if "title" in json_schema:
            del json_schema["title"]
        return json_schema

    def get_schema_from_definitions(
        self, json_ref
    ) -> pydantic.json_schema.JsonSchemaValue | None:
        """
        The function gets a JSON reference (json_ref) and uses super class
        functionality to obtain a JSON schema for that reference. It then removes
        the "title" field from the schema if it's present before returning it.

        Args:
            json_ref (dict): The `json_ref` input parameter is a JSON reference
                object that provides access to the definition of the schema being
                validated. The function uses it to fetch the JSON schema from the
                parent module's definitions.

        Returns:
            pydantic.json_schema.JsonSchemaValue | None: The function gets rid of
            title from the JSON schema obtained from a reference json file then
            returns whatever remaining JsonSchemaValue (possibly None) orNone .

        """
        json_schema = super().get_schema_from_definitions(json_ref)
        if json_schema and "title" in json_schema:
            del json_schema["title"]
        return json_schema

    def field_title_should_be_set(self, schema) -> bool:
        """
        This function checks if the title of a field should be set or not based
        on the given schema and returns a boolean value indicating whether it
        should be set or not.

        Args:
            schema (dict): The schema input parameter is not used within the body
                of the function at all. Thus the schema input will have no effect
                on the outcome of the functions output.

        Returns:
            bool: The output returned by this function is False.

        """
        return False
