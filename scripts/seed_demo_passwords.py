"""
dataset/processed/users.csv (and users table) has no password column —
schema.sql's hashed_password column is nullable specifically so seeding
can be a separate, explicit step rather than baking a fixed password into
the dataset generator (which is meant to model realistic SCRB data, not
auth credentials).

Run this AFTER dataset/seed/load_database.py:

    export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ksp_crime
    python scripts/seed_demo_passwords.py

Sets the same demo password for every seeded user, grouped by role so
it's easy to remember and matches what README.md documents. This is a
hackathon demo credential, not a production secret — rotate before any
real deployment.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from sqlalchemy import create_engine, text
from app.core.security import hash_password

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ksp_crime"
)

DEMO_PASSWORD = "Demo@KSP2026"


def main():
    engine = create_engine(DATABASE_URL)
    hashed = hash_password(DEMO_PASSWORD)

    with engine.begin() as conn:
        result = conn.execute(
            text("UPDATE users SET hashed_password = :hashed"), {"hashed": hashed}
        )
        print(f"Set demo password on {result.rowcount} users.")

    print(f"\nDemo password for ALL seeded users: {DEMO_PASSWORD}")
    print("Log in with any username from dataset/processed/users.csv, e.g. admin.scrb, sp.blr.city, dsp.mysuru,")
    print("or any of the 30 officer-linked usernames (derived from officers.csv emails).")


if __name__ == "__main__":
    main()
