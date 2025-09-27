"""Small utility helpers used by the project.

Keep these lightweight to avoid coupling during initial refactor.
"""
from typing import Iterable

def ensure_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, Iterable):
        return list(value)
    return [value]
