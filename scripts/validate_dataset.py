"""
Integrity checks for dataset/processed/*.csv before loading into Postgres.
Run this after any change to the generator scripts.
"""
import pandas as pd
import os

BASE = os.path.join(os.path.dirname(__file__), "..", "dataset", "processed")

def load(name):
    return pd.read_csv(os.path.join(BASE, f"{name}.csv"))

def main():
    cases = load("cases")
    search_index = load("search_index")
    users = load("users")
    audit_logs = load("audit_logs")

    assert cases["case_id"].is_unique, "duplicate case_id in cases.csv"
    assert search_index["case_id"].isin(cases["case_id"]).all(), "search_index has case_id not in cases.csv"
    assert audit_logs["user_id"].isin(users["user_id"]).all(), "audit_logs has user_id not in users.csv"
    assert cases["complaint_text"].notna().all(), "cases.csv missing complaint_text values"

    print("All checks passed.")

if __name__ == "__main__":
    main()
