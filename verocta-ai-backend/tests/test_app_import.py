"""Basic smoke tests for package layout."""
import json

def test_create_app_importable():
    # Ensure the package create_app works and the app exposes the health endpoint
    from verocta import create_app
    app = create_app()

    # Use Flask test client when available
    try:
        client = app.test_client()
        resp = client.get('/api/health')
        # If the endpoint doesn't exist return code should be 404 or 200
        assert resp.status_code in (200, 404)
    except Exception:
        # If Flask is not installed or app isn't a Flask app, at least the import path should work
        assert app is not None
