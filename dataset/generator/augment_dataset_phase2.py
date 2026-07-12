"""
Phase-2 additions (targeted, per second review):

1. cases.csv           -> `pattern_id` column linking each case to a row in
                           crime_patterns.csv (where the crime_type has a
                           matching pattern), so a Similar-Case engine can
                           join on pattern instead of just crime_type string.
2. digital_evidence.csv -> `extracted_entities` column: a compact string of
                           phone/email/UPI-style identifiers pulled out of
                           that evidence record, simulating what an
                           OCR/NER pipeline would populate later.

Skipped intentionally (per reviewer's own "freeze the dataset" call and the
project's own priorities): latitude/longitude, courts/prisons/Aadhaar data.
"""

import pandas as pd
import numpy as np
import random

random.seed(7)
np.random.seed(7)

OUT = "output"

cases = pd.read_csv(f"{OUT}/cases.csv")
crime_patterns = pd.read_csv(f"{OUT}/crime_patterns.csv", keep_default_na=False, na_values=[""])
digital_evidence = pd.read_csv(f"{OUT}/digital_evidence.csv")

# ---------------------------------------------------------------------------
# 1. pattern_id on cases.csv
# ---------------------------------------------------------------------------
patterns_by_type = crime_patterns.groupby("crime_type")["pattern_id"].apply(list).to_dict()

def pick_pattern(ct):
    options = patterns_by_type.get(ct)
    if not options:
        return None
    return random.choice(options)

cases["pattern_id"] = cases["crime_type"].apply(pick_pattern)
cases.to_csv(f"{OUT}/cases.csv", index=False)

matched = cases["pattern_id"].notna().sum()
print(f"✅ cases.csv: pattern_id added ({matched}/{len(cases)} cases matched to a known pattern; "
      f"the rest are crime types with no defined pattern in crime_patterns.csv, e.g. Assault/UPI Fraud/ATM Fraud/Mobile Theft/Online Scam/Domestic Violence)")

# ---------------------------------------------------------------------------
# 2. extracted_entities on digital_evidence.csv
# ---------------------------------------------------------------------------
UPI_HANDLES = ["okaxis", "okhdfcbank", "oksbi", "ybl", "paytm", "ibl"]

def build_entities(row):
    parts = []
    if pd.notna(row.get("phone_number")):
        parts.append(f"Phone: {row['phone_number']}")
    if pd.notna(row.get("email")):
        parts.append(f"Email: {row['email']}")
    if pd.notna(row.get("ip_address")):
        parts.append(f"IP: {row['ip_address']}")
    # simulate an occasional UPI ID extracted from bank-statement/screenshot type evidence
    if row.get("file_type") in ("Bank Statement", "Screenshot", "Chat Log") and random.random() < 0.5:
        uname = str(row.get("email", "user")).split("@")[0] if pd.notna(row.get("email")) else "user"
        parts.append(f"UPI: {uname}@{random.choice(UPI_HANDLES)}")
    return "; ".join(parts) if parts else None

digital_evidence["extracted_entities"] = digital_evidence.apply(build_entities, axis=1)
digital_evidence.to_csv(f"{OUT}/digital_evidence.csv", index=False)

print(f"✅ digital_evidence.csv: extracted_entities added "
      f"({digital_evidence['extracted_entities'].notna().sum()}/{len(digital_evidence)} rows populated)")

print("\nPhase-2 additions applied. Dataset frozen after this per roadmap.")
