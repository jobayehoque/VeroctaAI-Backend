"""Database service shims.

Expose legacy database services through the package namespace.
"""

try:
    from database_enhanced import enhanced_db  # noqa: F401
except Exception:
    enhanced_db = None  # type: ignore

try:
    from database import db_service  # noqa: F401
except Exception:
    db_service = None  # type: ignore

__all__ = ["enhanced_db", "db_service"]



