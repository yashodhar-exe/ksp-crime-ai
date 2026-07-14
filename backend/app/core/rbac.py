"""
Thin wrapper around the boolean permission columns on `roles`
(can_view_all_districts, can_export, can_edit_case, can_manage_users).
Kept separate from api/deps.py so permission *logic* lives in one place
even though the FastAPI `Depends()` wiring lives in deps.py.
"""
from app.models.role import Role


PERMISSION_FIELDS = (
    "can_view_all_districts",
    "can_export",
    "can_edit_case",
    "can_manage_users",
)


def has_permission(role: Role, permission: str) -> bool:
    if permission not in PERMISSION_FIELDS:
        raise ValueError(f"Unknown permission: {permission}")
    return bool(getattr(role, permission, False))


def scoped_district(role: Role, user_district: str | None) -> str | None:
    """
    Returns the district a user's queries should be filtered to, or None
    if they can see all districts (e.g. Admin / SP roles). Callers apply
    this as a WHERE clause on district-scoped tables (cases, citizens).
    """
    if has_permission(role, "can_view_all_districts"):
        return None
    return user_district
