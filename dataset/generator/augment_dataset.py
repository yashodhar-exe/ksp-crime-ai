"""
Phase-1 dataset improvements for the KSP Crime DB hackathon prototype.

1. search_index.csv  -> rebuilt so entity_value genuinely links to a real case_id
2. cases.csv          -> new `complaint_text` column with realistic FIR-style narratives
3. users.csv          -> login/user accounts for officers, tied to a role
4. roles.csv          -> Admin, SP, DSP, Inspector, Sub Inspector, Constable
5. audit_logs.csv     -> Viewed / Downloaded / Updated / Searched events
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

OUT = "output"

cases = pd.read_csv(f"{OUT}/cases.csv")
citizens = pd.read_csv(f"{OUT}/citizens.csv")
officers = pd.read_csv(f"{OUT}/officers.csv")
stations = pd.read_csv(f"{OUT}/police_stations.csv")
suspects = pd.read_csv(f"{OUT}/suspects.csv")
victims = pd.read_csv(f"{OUT}/victims.csv")
phones = pd.read_csv(f"{OUT}/phones.csv")
vehicles = pd.read_csv(f"{OUT}/vehicles.csv")
bank_accounts = pd.read_csv(f"{OUT}/bank_accounts.csv")
crime_patterns = pd.read_csv(f"{OUT}/crime_patterns.csv", keep_default_na=False, na_values=[""])

# ---------------------------------------------------------------------------
# 2. complaint_text for cases.csv
# ---------------------------------------------------------------------------
pattern_by_type = (
    crime_patterns.drop_duplicates(subset="crime_type", keep="first")
    .set_index("crime_type")
    .to_dict(orient="index")
)

FIRST_LINES = {
    "Cyber Fraud": "The complainant reported being contacted by an unknown person offering {mo}.",
    "UPI Fraud": "The complainant received a suspicious {comm} message regarding a UPI transaction.",
    "ATM Fraud": "The complainant noticed unauthorised withdrawals from their bank account after visiting an ATM.",
    "Online Scam": "The complainant was approached via {comm} with an offer related to {mo}.",
    "Identity Theft": "The complainant discovered that their personal documents were being misused to open new accounts.",
    "Chain Snatching": "The complainant was walking near {city} when two persons on a motorbike snatched their gold chain.",
    "Mobile Theft": "The complainant's mobile phone was stolen while travelling in {city}.",
    "Vehicle Theft": "The complainant reported that their vehicle was stolen from outside their residence in {city}.",
    "Burglary": "The complainant returned home in {city} to find the house broken into and valuables missing.",
    "Assault": "The complainant reported being physically assaulted following a dispute in {city}.",
    "Domestic Violence": "The complainant reported repeated harassment and assault by a family member.",
    "Drug Trafficking": "Acting on a tip-off, police intercepted a suspect near {city} in possession of contraband.",
    "Kidnapping": "The complainant reported that a family member went missing under suspicious circumstances near {city}.",
    "Missing Person": "The complainant reported that a family member has been missing since the incident date.",
    "Murder": "Police received information regarding the death of a person under suspicious circumstances in {city}.",
}

def make_complaint_text(row):
    ct = row["crime_type"]
    city = row["city"]
    pat = pattern_by_type.get(ct)
    template = FIRST_LINES.get(ct, "The complainant filed a complaint regarding a {ct} incident in {city}.")

    comm = pat["communication"] if pat and pat["communication"] not in ("None", "") else None
    mo = pat["modus_operandi"] if pat else ct.lower()
    line1 = template.format(mo=mo, comm=comm or "an unknown channel", city=city, ct=ct)

    lines = [line1]

    if pat:
        payment = pat["payment_method"]
        loss = row["estimated_loss"]
        fraud_types = ("Cyber Fraud", "UPI Fraud", "ATM Fraud", "Online Scam", "Identity Theft")
        if payment not in ("None", "") and ct in fraud_types:
            lines.append(
                f"The complainant suffered an estimated loss of approximately Rs. {loss:,}, "
                f"paid via {payment}."
            )
        elif payment not in ("None", "") and loss:
            lines.append(
                f"The estimated value of property/cash lost is Rs. {loss:,} ({payment} involved)."
            )
        elif loss and ct in ("Burglary", "Vehicle Theft", "Mobile Theft", "Chain Snatching"):
            lines.append(f"The estimated value of property lost/stolen is Rs. {loss:,}.")

        if comm:
            lines.append(
                f"The accused primarily communicated with the victim via {comm} and is suspected to be "
                f"linked to a {pat['risk_level'].lower()}-risk {ct.lower()} network."
            )
        else:
            lines.append(
                f"This case matches a known {pat['risk_level'].lower()}-risk {ct.lower()} pattern "
                f"('{pat['modus_operandi']}')."
            )
    else:
        if row["estimated_loss"] and ct in ("Burglary", "Vehicle Theft", "Mobile Theft"):
            lines.append(f"The estimated value of property lost/stolen is Rs. {row['estimated_loss']:,}.")

    lines.append(
        f"A First Information Report ({row['fir_number']}) was registered at {row['city']} and the case "
        f"was marked as {row['priority'].lower()} priority. Investigation is currently {row['status'].lower()}."
    )
    return " ".join(lines)

cases["complaint_text"] = cases.apply(make_complaint_text, axis=1)
cases.to_csv(f"{OUT}/cases.csv", index=False)
print("✅ cases.csv updated with complaint_text")

# ---------------------------------------------------------------------------
# 1. Rebuild search_index.csv with real linkages
# ---------------------------------------------------------------------------
victim_case = victims.groupby("citizen_id")["case_id"].apply(list).to_dict()
suspect_case = suspects.groupby("citizen_id")["case_id"].apply(list).to_dict()

def citizen_cases(cid):
    return victim_case.get(cid, []) + suspect_case.get(cid, [])

officer_case = cases.groupby("officer_id")["case_id"].apply(list).to_dict()

records = []
idx = 1

def add_record(entity_type, entity_value, case_id):
    global idx
    if case_id is None:
        return
    records.append({
        "search_id": f"SRCH{idx:06}",
        "entity_type": entity_type,
        "entity_value": entity_value,
        "case_id": case_id,
    })
    idx += 1

all_citizen_cases = {}
for cid in set(list(victim_case.keys()) + list(suspect_case.keys())):
    all_citizen_cases[cid] = citizen_cases(cid)

for cid, cs in all_citizen_cases.items():
    if cs:
        add_record("Citizen", cid, random.choice(cs))

for _, r in phones.iterrows():
    cs = all_citizen_cases.get(r["citizen_id"])
    if cs:
        add_record("Phone", r["phone_number"], random.choice(cs))

for _, r in vehicles.iterrows():
    cs = all_citizen_cases.get(r["citizen_id"])
    if cs:
        add_record("Vehicle", r["vehicle_number"], random.choice(cs))

for _, r in bank_accounts.iterrows():
    cs = all_citizen_cases.get(r["citizen_id"])
    if cs:
        add_record("Bank", r["account_number"], random.choice(cs))

for oid, cs in officer_case.items():
    if cs:
        add_record("Officer", oid, random.choice(cs))

for _, r in cases.iterrows():
    add_record("Case", r["case_id"], r["case_id"])
    add_record("Case", r["fir_number"], r["case_id"])

search_index = pd.DataFrame(records)
search_index = search_index.drop_duplicates(subset=["entity_type", "entity_value"])
if len(search_index) > 40000:
    search_index = search_index.sample(40000, random_state=42).reset_index(drop=True)
search_index["search_id"] = [f"SRCH{i+1:06}" for i in range(len(search_index))]
search_index.to_csv(f"{OUT}/search_index.csv", index=False)
print(f"✅ search_index.csv rebuilt with real linkages ({len(search_index)} rows)")

# ---------------------------------------------------------------------------
# 4. roles.csv
# ---------------------------------------------------------------------------
roles = pd.DataFrame([
    {"role_id": "ROLE01", "role_name": "Admin",         "level": 1, "can_view_all_districts": True,  "can_export": True,  "can_edit_case": True,  "can_manage_users": True},
    {"role_id": "ROLE02", "role_name": "SP",             "level": 2, "can_view_all_districts": True,  "can_export": True,  "can_edit_case": True,  "can_manage_users": False},
    {"role_id": "ROLE03", "role_name": "DSP",            "level": 3, "can_view_all_districts": False, "can_export": True,  "can_edit_case": True,  "can_manage_users": False},
    {"role_id": "ROLE04", "role_name": "Inspector",      "level": 4, "can_view_all_districts": False, "can_export": True,  "can_edit_case": True,  "can_manage_users": False},
    {"role_id": "ROLE05", "role_name": "Sub Inspector",  "level": 5, "can_view_all_districts": False, "can_export": False, "can_edit_case": True,  "can_manage_users": False},
    {"role_id": "ROLE06", "role_name": "Constable",      "level": 6, "can_view_all_districts": False, "can_export": False, "can_edit_case": False, "can_manage_users": False},
])
roles.to_csv(f"{OUT}/roles.csv", index=False)
print("✅ roles.csv created")

rank_to_role = {
    "Inspector": "ROLE04",
    "ACP": "ROLE03",
    "Sub Inspector": "ROLE05",
    "Constable": "ROLE06",
    "Head Constable": "ROLE06",
}

# ---------------------------------------------------------------------------
# 3. users.csv
# ---------------------------------------------------------------------------
sample_officers = officers.sample(min(30, len(officers)), random_state=42).copy()
users = []
for i, (_, r) in enumerate(sample_officers.iterrows(), start=1):
    role_id = rank_to_role.get(r["rank"], "ROLE06")
    users.append({
        "user_id": f"USR{i:04}",
        "officer_id": r["officer_id"],
        "username": r["email"].split("@")[0],
        "role_id": role_id,
        "station_id": r["station_id"],
        "status": "Active",
        "last_login": (datetime(2026, 7, 1) - timedelta(days=random.randint(0, 20))).strftime("%Y-%m-%d"),
    })

for i, (uname, role) in enumerate(
    [("admin.scrb", "ROLE01"), ("sp.blr.city", "ROLE02"), ("dsp.mysuru", "ROLE03")],
    start=len(users) + 1,
):
    users.append({
        "user_id": f"USR{i:04}",
        "officer_id": None,
        "username": uname,
        "role_id": role,
        "station_id": None,
        "status": "Active",
        "last_login": "2026-07-10",
    })

users_df = pd.DataFrame(users)
users_df.to_csv(f"{OUT}/users.csv", index=False)
print(f"✅ users.csv created ({len(users_df)} rows)")

# ---------------------------------------------------------------------------
# 5. audit_logs.csv
# ---------------------------------------------------------------------------
ACTIONS = ["Viewed Case", "Downloaded Report", "Updated Evidence", "Searched Entity", "Viewed Suspect Profile"]
log_rows = []
sample_cases = cases.sample(min(2000, len(cases)), random_state=1)["case_id"].tolist()

start = datetime(2026, 6, 1)
user_ids = users_df["user_id"].tolist()
for i in range(1, 6001):
    uid = random.choice(user_ids)
    action = random.choice(ACTIONS)
    ts = start + timedelta(
        days=random.randint(0, 40),
        hours=random.randint(8, 20),
        minutes=random.randint(0, 59),
    )
    log_rows.append({
        "log_id": f"LOG{i:06}",
        "user_id": uid,
        "action": action,
        "case_id": random.choice(sample_cases) if action != "Searched Entity" else None,
        "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
        "ip_address": f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
    })

audit_logs = pd.DataFrame(log_rows).sort_values("timestamp").reset_index(drop=True)
audit_logs.to_csv(f"{OUT}/audit_logs.csv", index=False)
print(f"✅ audit_logs.csv created ({len(audit_logs)} rows)")

print("\nAll Phase-1 improvements applied.")
