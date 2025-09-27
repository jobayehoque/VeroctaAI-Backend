"""API routes shims.

Expose existing route modules through the package namespace.
"""

try:
    # Primary REST API routes
    from routes import *  # noqa: F401,F403
except Exception:
    # No routes available in legacy layout
    pass

try:
    # Dynamic demo APIs
    import dynamic_apis as dynamic  # noqa: F401
except Exception:
    dynamic = None

__all__ = []



