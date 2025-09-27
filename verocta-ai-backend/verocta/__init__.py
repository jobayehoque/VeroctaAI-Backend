"""Verocta package wrapper and organization surface.

This package exposes a stable import surface while the repository is
incrementally organized into subpackages. You can import components via the
new structure without breaking legacy entry points.

Quick usage:
    from verocta import create_app
    app = create_app()

Subpackages (shimmed to legacy modules until full migration):
- verocta.app: Flask app entry
- verocta.api: HTTP routes and API blueprints
- verocta.auth: Authentication helpers
- verocta.db: Database services/adapters
- verocta.analysis: Analysis engines, parsers, generators
- verocta.common: Shared utilities and config
"""
from typing import Optional

def create_app():
    """Return an existing Flask app from the top-level `app` module if present,
    otherwise create a minimal Flask app for compatibility and testing.
    """
    try:
        # Prefer the existing top-level app (keeps existing entrypoint working)
        import app as top_app
        return getattr(top_app, 'app')
    except Exception:
        # Lazy import to avoid adding flask as a hard runtime dependency of this file
        try:
            from flask import Flask
        except Exception:
            raise RuntimeError("Flask is required to create an application. Install requirements.txt")
        app = Flask(__name__)
        return app

__all__ = ["create_app"]
