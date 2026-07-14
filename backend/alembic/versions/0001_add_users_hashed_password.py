"""add users.hashed_password

Assumes dataset/seed/schema.sql has already been applied (that file is the
source of truth for the initial schema — see backend/README.md). This is
the first alembic migration and only adds the one column the demo dataset
doesn't ship with: a credential store for the login flow in
app/core/security.py + app/api/routes/auth.py. Everything else in
app.models mirrors schema.sql exactly.

Revision ID: 0001_add_users_hashed_password
Revises:
Create Date: 2026-07-14

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001_add_users_hashed_password"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("hashed_password", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "hashed_password")
