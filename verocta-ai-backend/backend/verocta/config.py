"""Application configuration helpers.

Move environment and config-related logic from `app.py` into this module
over time. For now it provides small helpers used by tests and by the
refactored package layout.
"""
import os

def get_env(key: str, default=None):
    return os.environ.get(key, default)

def is_production() -> bool:
    return os.environ.get('FLASK_ENV') == 'production'
