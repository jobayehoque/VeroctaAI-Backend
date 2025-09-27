VeroctaAI - Backend
====================

This repository contains the backend API for VeroctaAI — an AI-powered
financial intelligence platform.

Recommended structure
---------------------

The repository is being organized toward this structure. Shims are provided so
you can start importing from the package paths immediately while we migrate
code incrementally.

```
VeroctaAI/
├─ app.py                     # Legacy entry (kept)
├─ routes.py                  # Legacy routes (kept)
├─ auth.py                    # Legacy auth (kept)
├─ database.py                # Legacy DB (kept)
├─ database_enhanced.py       # Enhanced DB (kept)
├─ csv_parser.py              # Legacy parser (kept)
├─ pdf_generator.py           # PDF generator (kept)
├─ dynamic_apis.py            # Demo/dynamic endpoints (kept)
├─ verocta/
│  ├─ __init__.py             # Stable import surface + create_app()
│  ├─ app/
│  │  └─ __init__.py          # `from verocta.app import app`
│  ├─ api/
│  │  └─ __init__.py          # `import verocta.api` (routes, dynamic APIs)
│  ├─ auth/
│  │  └─ __init__.py          # Auth helpers re-exported
│  ├─ db/
│  │  └─ __init__.py          # `enhanced_db`, `db_service`
│  ├─ analysis/
│  │  └─ __init__.py          # SpendScore engines, CSV parsing, PDF gen
│  └─ common/
│     └─ __init__.py          # Config + utils
└─ tests/
```

Import examples
---------------

- App entry: `from verocta.app import app`
- Routes: `import verocta.api  # side-effect registers routes`
- Auth: `from verocta.auth import validate_user`
- DB: `from verocta.db import enhanced_db, db_service`
- Analysis: `from verocta.analysis import get_enhanced_analysis`
- Common: `from verocta.common import get_env`

Quick start
-----------

1. Create a virtual environment and install requirements:

   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Run tests:

   pip install pytest
   pytest -q

Next steps
----------

- Gradually move modules under the respective `verocta/` subpackages.
- Update imports to use the package paths shown above.
- Once migrated, remove redundant shims and legacy duplicates.
