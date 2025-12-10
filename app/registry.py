# app/registry.py
from typing import Callable, Dict

TOOLS: Dict[str, Callable] = {}


def register_tool(name: str):
    """
    Decorator to register a function as a tool by name.
    """
    def decorator(fn: Callable):
        TOOLS[name] = fn
        return fn
    return decorator


def get_tool(name: str) -> Callable:
    """
    Retrieve a tool function by name.
    """
    if name not in TOOLS:
        raise KeyError(f"Tool '{name}' is not registered")
    return TOOLS[name]
