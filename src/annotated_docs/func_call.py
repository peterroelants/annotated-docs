from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

from .json_schema import get_parameter_model

P = ParamSpec("P")
R = TypeVar("R")


def call_with_json(func: Callable[P, R], parameters_json: dict[str, Any]) -> R:
    """
    Call the given function with the given parameters.
    Parameters are converted from JSON to Python using the function's parameter model.
    """
    parameter_model = get_parameter_model(func)
    # Validation: Convert JSON to Python using the parameter model
    parameters = parameter_model.model_validate(parameters_json)
    # Call with first layer of parameters as keyword arguments
    return func(**dict(parameters))
