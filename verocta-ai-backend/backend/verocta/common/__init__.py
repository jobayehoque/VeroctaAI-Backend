"""Common utilities and configuration shims."""

try:
    from verocta.config import get_env, is_production  # noqa: F401
except Exception:
    from ._compat import get_env, is_production  # type: ignore

try:
    from verocta.utils import *  # noqa: F401,F403
except Exception:
    pass

__all__ = [
    "get_env",
    "is_production",
]



