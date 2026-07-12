"""
Loads all CSVs from dataset/processed/ into Postgres.

Usage:
    export DATABASE_URL=postgresql://user:pass@localhost:5432/ksp_crime
    python load_database.py

Notes:
- Run schema.sql first to create tables with proper FKs/indexes.
- Load order matters (parents before children) to respect foreign keys.
- This is a straightforward pandas.to_sql loader; swap for COPY if you need
  it faster on the full dataset.
"""

import os
import pandas as pd
from sqlalchemy import create_engine, table

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5433/ksp_crime"
)
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "processed")

# Parents first, then children that reference them, per foreign keys.
LOAD_ORDER = [
    "police_stations",
    "roles",
    "citizens",
    "officers",
    "users",
    "crime_patterns",
    "cases",
    "suspects",
    "victims",
    "phones",
    "vehicles",
    "bank_accounts",
    "evidence",
    "digital_evidence",
    "criminal_relationships",
    "investigation_notes",
    "timeline",
    "search_index",
    "audit_logs",
]

def main():
    print("DATABASE_URL:", DATABASE_URL)

    engine = create_engine(DATABASE_URL)

    with engine.begin() as conn:
        for table in LOAD_ORDER:

            path = os.path.join(PROCESSED_DIR, f"{table}.csv")

            if not os.path.exists(path):
                print(f"Skip: {table}.csv not found")
                continue

            print(f"\nLoading {table}...")

            df = pd.read_csv(path)

            # Fix missing injury_level values
            # Victims
            if table == "victims":
                df["injury_level"] = df["injury_level"].fillna("Unknown")

# Criminal relationships
            if table == "criminal_relationships":
                df = df[df["citizen_1"] != df["citizen_2"]]

# Remove duplicate rows from every table
                df = df.drop_duplicates()
            try:
                df.to_sql(
                    table,
                    conn,
                    if_exists="append",
                    index=False,
                    method="multi",
                    chunksize=1000,
                )

                print(f"✅ Loaded {table}: {len(df)} rows")

            except Exception as e:
                print(f"\n❌ Failed while loading {table}")
                print(e)
                raise
if __name__ == "__main__":
    main()
