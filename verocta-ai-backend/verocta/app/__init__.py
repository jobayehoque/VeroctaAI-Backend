"""Application entry shims.

Provides access to the top-level Flask app without moving files yet.
Later, app factory and blueprints can live here.
"""

try:
    # Re-export the existing Flask app instance
    from app import app  # type: ignore
except Exception:
    app = None  # Will be created via `verocta.create_app()` as fallback

__all__ = ["app"]



