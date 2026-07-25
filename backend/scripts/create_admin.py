"""
One-off CLI to create (or promote) an Admin account, run directly against
the database — never through the public API.

Why this exists: POST /auth/register deliberately refuses to create Admin
accounts (see NON_SELF_REGISTRABLE_ROLE_NAMES in app/api/routes/auth.py),
and POST /users requires an existing Admin's token to call. That's correct
for day-to-day operation, but it means the very first Admin has to be
created some other way. This script is that "other way": it's meant to be
run by someone with direct database/deploy access, not exposed as an HTTP
endpoint.

Usage:
    cd backend
    python -m scripts.create_admin --username chief_admin
    python -m scripts.create_admin --username chief_admin --promote  # if user exists

Password is never taken as a CLI argument (it would end up in shell
history / process listings) — it's always prompted for via getpass.
"""
from __future__ import annotations

import argparse
import getpass
import sys
import uuid

from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.role import Role
from app.models.user import User

ADMIN_ROLE_NAME = "Admin"
MIN_PASSWORD_LENGTH = 8


def _generate_user_id() -> str:
    return f"U{uuid.uuid4().hex[:9].upper()}"


def _prompt_password() -> str:
    while True:
        password = getpass.getpass("Password: ")
        if len(password) < MIN_PASSWORD_LENGTH:
            print(f"Password must be at least {MIN_PASSWORD_LENGTH} characters.", file=sys.stderr)
            continue
        confirm = getpass.getpass("Confirm password: ")
        if password != confirm:
            print("Passwords did not match, try again.", file=sys.stderr)
            continue
        return password


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or promote the first Admin account.")
    parser.add_argument("--username", required=True, help="Username for the Admin account.")
    parser.add_argument(
        "--promote",
        action="store_true",
        help="If the username already exists, promote it to Admin instead of failing.",
    )
    args = parser.parse_args()

    db = SessionLocal()
    try:
        admin_role = db.execute(select(Role).where(Role.role_name == ADMIN_ROLE_NAME)).scalar_one_or_none()
        if admin_role is None:
            print(
                f"No role named {ADMIN_ROLE_NAME!r} exists in the roles table yet. "
                "Seed the roles table first (see app/models/role.py for the expected columns).",
                file=sys.stderr,
            )
            return 1

        existing = db.execute(select(User).where(User.username == args.username)).scalar_one_or_none()

        if existing is not None and not args.promote:
            print(
                f"User {args.username!r} already exists (role_id={existing.role_id}). "
                "Re-run with --promote to change their role to Admin instead.",
                file=sys.stderr,
            )
            return 1

        if existing is not None:
            existing.role_id = admin_role.role_id
            existing.status = "Active"
            db.commit()
            print(f"Promoted existing user {args.username!r} (user_id={existing.user_id}) to Admin.")
            return 0

        password = _prompt_password()
        user = User(
            user_id=_generate_user_id(),
            username=args.username,
            hashed_password=hash_password(password),
            role_id=admin_role.role_id,
            status="Active",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Created Admin user {user.username!r} (user_id={user.user_id}). You can now log in.")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())