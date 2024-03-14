import importlib.metadata

from .func_call import call_with_json
from .json_schema import as_json_schema, doc

__version__ = importlib.metadata.version("annotated-docs")
