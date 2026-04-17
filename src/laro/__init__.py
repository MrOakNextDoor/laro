
# Determines what modules are imported when a wildcard import (i.e. "from laro import *") is done.
# NOTE: Modules that are added here must also be added to the stub file.
__all__ = (
    "misc", # type: ignore
    "game", # type: ignore
)
__version__: str = "0.1.0"

# Because of the lines below, we prevent modules from being imported when laro is used as a CLI.
from importlib import import_module

def __getattr__(name):
    if name in __all__:
        module = import_module(f".{name}", __name__)
        globals()[name] = module
        return module
    raise AttributeError(f"Module {__name__!r} has no attribute {name!r}.")
