"""Authentication shims.

Re-export legacy auth helpers under the package namespace.
"""

try:
    from auth import (
        init_auth,
        revoke_token,
        is_token_revoked,
        validate_user,
        create_user,
        get_user_by_email,
        get_user_by_id,
        require_admin,
        get_current_user,
    )  # noqa: F401
except Exception:
    # Legacy module may not be present in some environments
    init_auth = None  # type: ignore

__all__ = [
    "init_auth",
    "revoke_token",
    "is_token_revoked",
    "validate_user",
    "create_user",
    "get_user_by_email",
    "get_user_by_id",
    "require_admin",
    "get_current_user",
]



