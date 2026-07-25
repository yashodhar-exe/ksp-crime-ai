"""
Scaled-up dataset generator for KSP Crime AI — matches dataset/seed/schema.sql
exactly (column names/types) and reuses the same ID formats / enum pools as
the original dataset/processed/*.csv, just at a much larger volume.

This "mixes" the fast vectorized numpy/Faker approach used for the standalone
100k-row Police-FIR demo with this project's *real* schema, so the output
drops straight into dataset/processed/ and loads via dataset/seed/load_database.py
with zero code changes on that side.

Run: python3 generate_dataset_100k.py
Writes CSVs to dataset/processed/ (overwrites in place; originals are kept
as dataset/processed_original_backup/ the first time this runs).
"""
import os
import shutil
import numpy as np
import pandas as pd
from faker import Faker

np.random.seed(42)
fake = Faker()
Faker.seed(42)

HERE = os.path.dirname(os.path.abspath(__file__))
PROCESSED = os.path.join(HERE, "..", "processed")
BACKUP = os.path.join(HERE, "..", "processed_original_backup")

if os.path.isdir(PROCESSED) and not os.path.isdir(BACKUP):
    shutil.copytree(PROCESSED, BACKUP)
    print(f"Backed up original dataset -> {BACKUP}")
os.makedirs(PROCESSED, exist_ok=True)

def save(name, df):
    path = os.path.join(PROCESSED, f"{name}.csv")
    df.to_csv(path, index=False)
    print(f"{name:<24} {len(df):>8,} rows -> {path}")

def rand_choice(pool, n, p=None):
    return np.random.choice(pool, n, p=p)

def zpad(prefix, ids, width):
    return [f"{prefix}{i:0{width}d}" for i in ids]

# ---------------------------------------------------------------------------
# Reference pools (same values the original generator/augment scripts used)
# ---------------------------------------------------------------------------
CITIES = ["Mysuru", "Tumakuru", "Bengaluru", "Shivamogga", "Belagavi", "Hubballi", "Ballari", "Mangaluru"]
DISTRICTS = ["Belagavi", "Dakshina Kannada", "Shivamogga", "Tumakuru", "Dharwad", "Mysuru", "Bengaluru Urban", "Ballari"]
RANKS = ["Inspector", "ACP", "Sub Inspector", "Constable", "Head Constable"]
STATUSES = ["Pending", "Open", "Closed", "Under Investigation"]
PRIORITIES = ["Medium", "Low", "Critical", "High"]
CRIME_TYPES = ["Burglary", "Mobile Theft", "Domestic Violence", "Drug Trafficking", "Kidnapping",
               "UPI Fraud", "Murder", "Chain Snatching", "Identity Theft", "ATM Fraud",
               "Assault", "Missing Person", "Online Scam", "Cyber Fraud", "Vehicle Theft"]
SUSPECT_ROLES = ["Unknown Suspect", "Accomplice", "Gang Member", "Main Suspect"]
ARREST_STATUS = ["Absconding", "Under Surveillance", "Wanted", "Arrested"]
INJURY = ["Serious", "Critical", "Minor", None]
PROVIDERS = ["BSNL", "Airtel", "Vi", "Jio"]
VEHICLE_TYPES = ["Car", "Bike", "Truck", "Auto"]
BANKS = ["SBI", "Canara Bank", "HDFC Bank", "Union Bank", "Axis Bank", "Bank of Baroda", "ICICI Bank"]
BANK_CODE = {"SBI": "SBIN", "Canara Bank": "CNRB", "HDFC Bank": "HDFC", "Union Bank": "UBIN",
             "Axis Bank": "UTIB", "Bank of Baroda": "BARB", "ICICI Bank": "ICIC"}
EVIDENCE_TYPES = ["CCTV Footage", "Video", "Photo", "Call Records", "Weapon", "WhatsApp Chat",
                   "Bank Statement", "Mobile Phone", "Laptop", "Passport", "Fingerprint",
                   "SIM Card", "DNA Sample", "Vehicle", "Driving License"]
EVIDENCE_STATUS = ["Collected", "Pending Analysis", "Sent to FSL", "Verified"]
DE_TYPES = ["Bank Statement", "Laptop", "Photo", "SIM Card", "Email", "Mobile Phone",
            "CCTV", "Video", "WhatsApp Chat", "Call Records"]
DE_STATUS = ["Verified", "Collected", "Pending Analysis"]
REL_TYPES = ["Same Vehicle", "Money Transfer", "Same Phone", "Business Partner", "Gang Member",
             "Friend", "Brother", "Associate", "Same Bank Account"]
EVENTS = ["Witness Statement Recorded", "Forensic Report Received", "Suspect Arrested",
          "Evidence Collected", "FIR Registered", "Charge Sheet Filed",
          "Complaint Registered", "Suspect Identified"]
ACTIONS = ["Updated Evidence", "Downloaded Report", "Searched Entity", "Viewed Case", "Viewed Suspect Profile"]
GENDERS = ["Male", "Female", "Other"]

FIRST_LINES = {
    "Cyber Fraud": "The complainant reported being contacted by an unknown person offering {mo}.",
    "UPI Fraud": "The complainant received a suspicious message regarding a UPI transaction.",
    "ATM Fraud": "The complainant noticed unauthorised withdrawals from their bank account after visiting an ATM.",
    "Online Scam": "The complainant was approached online with a fraudulent offer.",
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

def dates_between(start, end, n):
    s = pd.Timestamp(start).value // 10**9
    e = pd.Timestamp(end).value // 10**9
    return pd.to_datetime(np.random.randint(s, e, size=n), unit="s")

first_names = np.array([fake.first_name() for _ in range(4000)])
last_names = np.array([fake.last_name() for _ in range(4000)])

def rand_names(n):
    return np.random.choice(first_names, n), np.random.choice(last_names, n)

# ============================================================
# Scale factors (core = cases; everything else scaled off the
# original dataset's real-world ratios to `cases`)
# ============================================================
N_CASES = 100_000
N_STATIONS = 300
N_OFFICERS = 3_000
N_USERS = 250
N_CITIZENS = 150_000
N_SUSPECTS = 50_000
N_VICTIMS = 80_000
N_PHONES = 124_000
N_VEHICLES = 59_000
N_BANK_ACCOUNTS = 85_000
N_EVIDENCE = 150_000
N_DIGITAL_EVIDENCE = 150_000
N_RELATIONSHIPS = 50_000
N_NOTES = 120_000
N_TIMELINE = 540_000
N_SEARCH_INDEX = 400_000
N_AUDIT_LOGS = 60_000

# ============================================================
# 1. police_stations
# ============================================================
st_ids = np.arange(1, N_STATIONS + 1)
st_district = rand_choice(DISTRICTS, N_STATIONS)
police_stations = pd.DataFrame({
    "station_id": zpad("ST", st_ids, 4),
    "station_name": [f"{d} Police Station {i}" for i, d in zip(st_ids, st_district)],
    "district": st_district,
    "city": [CITIES[DISTRICTS.index(d) % len(CITIES)] for d in st_district],
    "phone": [f"080{np.random.randint(1000000, 9999999)}" for _ in range(N_STATIONS)],
})
save("police_stations", police_stations)

# ============================================================
# 2. roles (fixed lookup, not scaled)
# ============================================================
roles = pd.DataFrame({
    "role_id": ["ROLE01", "ROLE02", "ROLE03", "ROLE04", "ROLE05", "ROLE06"],
    "role_name": ["Admin", "SP", "DSP", "Inspector", "Sub Inspector", "Constable"],
    "level": [1, 2, 3, 4, 5, 6],
    "can_view_all_districts": [True, True, False, False, False, False],
    "can_export": [True, True, True, True, False, False],
    "can_edit_case": [True, True, True, True, True, False],
    "can_manage_users": [True, False, False, False, False, False],
})
save("roles", roles)

# ============================================================
# 3. citizens
# ============================================================
cit_ids = np.arange(1, N_CITIZENS + 1)
f, l = rand_names(N_CITIZENS)
cit_district = rand_choice(DISTRICTS, N_CITIZENS)
citizens = pd.DataFrame({
    "citizen_id": zpad("CID", cit_ids, 6),
    "first_name": f,
    "last_name": l,
    "gender": rand_choice(GENDERS, N_CITIZENS, p=[0.55, 0.43, 0.02]),
    "age": np.random.randint(1, 90, N_CITIZENS),
    "phone": [f"9{np.random.randint(100000000, 999999999)}" for _ in range(N_CITIZENS)],
    "email": [f"{fn.lower()}{i}@example.org" for i, fn in zip(cit_ids, f)],
    "address": [fake.street_address().replace("\n", ", ") for _ in range(N_CITIZENS)],
    "city": [CITIES[DISTRICTS.index(d) % len(CITIES)] for d in cit_district],
    "district": cit_district,
    "demo_citizen_id": zpad("KSP", cit_ids, 8),
})
save("citizens", citizens)

# ============================================================
# 4. officers
# ============================================================
off_ids = np.arange(1, N_OFFICERS + 1)
of, ol = rand_names(N_OFFICERS)
officers = pd.DataFrame({
    "officer_id": zpad("OFF", off_ids, 5),
    "name": [f"{a} {b}" for a, b in zip(of, ol)],
    "rank": rand_choice(RANKS, N_OFFICERS),
    "station_id": rand_choice(police_stations["station_id"].values, N_OFFICERS),
    "phone": [f"9{np.random.randint(100000000, 999999999)}" for _ in range(N_OFFICERS)],
    "email": [f"officer{i}@ksp.gov.in" for i in off_ids],
})
save("officers", officers)

# ============================================================
# 5. users
# ============================================================
usr_ids = np.arange(1, N_USERS + 1)
user_officer = np.random.choice(officers["officer_id"].values, N_USERS, replace=False)
users = pd.DataFrame({
    "user_id": zpad("USR", usr_ids, 4),
    "officer_id": user_officer,
    "username": [f"officer{o[3:].lstrip('0') or '0'}" for o in user_officer],
    "role_id": rand_choice(roles["role_id"].values, N_USERS, p=[0.02, 0.03, 0.1, 0.25, 0.25, 0.35]),
    "station_id": rand_choice(police_stations["station_id"].values, N_USERS),
    "status": rand_choice(["Active", "Inactive"], N_USERS, p=[0.92, 0.08]),
    "last_login": dates_between("2026-01-01", "2026-07-01", N_USERS).date,
})
users = users.drop_duplicates(subset="username")
save("users", users)

# ============================================================
# 6. crime_patterns (fixed lookup, not scaled)
# ============================================================
crime_patterns = pd.DataFrame([
    ("PAT0001", "Cyber Fraud", "Fake Investment", "WhatsApp", "UPI", "High"),
    ("PAT0002", "Cyber Fraud", "Loan Scam", "Telegram", "Bank Transfer", "High"),
    ("PAT0003", "Cyber Fraud", "Phishing", "SMS", "UPI", "Medium"),
    ("PAT0004", "Cyber Fraud", "OTP Scam", "Phone Call", "UPI", "Low"),
    ("PAT0005", "Cyber Fraud", "Job Scam", "WhatsApp", "Bank Transfer", "Low"),
    ("PAT0006", "Cyber Fraud", "Crypto Scam", "Telegram", "Crypto", "High"),
    ("PAT0007", "Vehicle Theft", "Duplicate Key", "None", "None", "Critical"),
    ("PAT0008", "Vehicle Theft", "Tow Away", "None", "None", "Medium"),
    ("PAT0009", "Burglary", "Night Break-In", "None", "Cash", "High"),
    ("PAT0010", "Chain Snatching", "Bike Escape", "None", "None", "Low"),
    ("PAT0011", "Murder", "Personal Rivalry", "Phone Call", "None", "Critical"),
    ("PAT0012", "Drug Trafficking", "Courier Network", "Telegram", "Cash", "Critical"),
    ("PAT0013", "Identity Theft", "Fake Documents", "Email", "Bank", "Critical"),
    ("PAT0014", "Kidnapping", "Fake Offer", "Phone Call", "Cash", "Critical"),
    ("PAT0015", "Missing Person", "Unknown", "Phone Call", "None", "Low"),
], columns=["pattern_id", "crime_type", "modus_operandi", "communication", "payment_method", "risk_level"])
save("crime_patterns", crime_patterns)

# ============================================================
# 7. cases
# ============================================================
case_ids = np.arange(1, N_CASES + 1)
case_crime_type = rand_choice(CRIME_TYPES, N_CASES)
case_city = rand_choice(CITIES, N_CASES)
case_district = rand_choice(DISTRICTS, N_CASES)
case_status = rand_choice(STATUSES, N_CASES)
case_priority = rand_choice(PRIORITIES, N_CASES)
reg_date = dates_between("2024-01-01", "2026-07-01", N_CASES)
inc_date = reg_date - pd.to_timedelta(np.random.randint(0, 300, N_CASES), unit="D")
years = reg_date.year.values
fir_number = [f"FIR{y}{i:06d}" for y, i in zip(years, case_ids)]
loss = np.random.randint(0, 2_000_000, N_CASES)

pattern_by_type = crime_patterns.drop_duplicates(subset="crime_type", keep="first").set_index("crime_type").to_dict(orient="index")

def brief(ct, city, fir, priority, status, ls):
    template = FIRST_LINES.get(ct, f"The complainant filed a complaint regarding a {ct} incident in {city}.")
    pat = pattern_by_type.get(ct)
    line1 = template.format(mo=(pat["modus_operandi"] if pat else ct.lower()), city=city)
    lines = [line1]
    if ls:
        lines.append(f"The estimated value of property/cash lost is Rs. {ls:,}.")
    if pat:
        lines.append(f"This case matches a known {pat['risk_level'].lower()}-risk {ct.lower()} pattern ('{pat['modus_operandi']}').")
    lines.append(f"A First Information Report ({fir}) was registered at {city} and the case was marked as "
                  f"{priority.lower()} priority. Investigation is currently {status.lower()}.")
    return " ".join(lines)

complaint_text = [brief(ct, ci, fr, pr, st, ls) for ct, ci, fr, pr, st, ls in
                   zip(case_crime_type, case_city, fir_number, case_priority, case_status, loss)]

pattern_id_for_type = {row["crime_type"]: pid for pid, row in
                        crime_patterns.drop_duplicates(subset="crime_type", keep="first").set_index("pattern_id").iterrows()}
# map crime_type -> a pattern_id (or None) - build lookup
type_to_pattern = {}
for _, row in crime_patterns.iterrows():
    type_to_pattern.setdefault(row["crime_type"], row["pattern_id"])
case_pattern = [type_to_pattern.get(ct) for ct in case_crime_type]

cases = pd.DataFrame({
    "case_id": zpad("CASE", case_ids, 6),
    "fir_number": fir_number,
    "crime_type": case_crime_type,
    "station_id": rand_choice(police_stations["station_id"].values, N_CASES),
    "officer_id": rand_choice(officers["officer_id"].values, N_CASES),
    "status": case_status,
    "priority": case_priority,
    "incident_date": inc_date.date,
    "registered_date": reg_date.date,
    "city": case_city,
    "district": case_district,
    "description": [fake.sentence(nb_words=10) for _ in range(N_CASES)],
    "estimated_loss": loss,
    "complaint_text": complaint_text,
    "pattern_id": case_pattern,
})
save("cases", cases)

# ============================================================
# 8. suspects / 9. victims
# ============================================================
sus_ids = np.arange(1, N_SUSPECTS + 1)
suspects = pd.DataFrame({
    "suspect_id": zpad("SUS", sus_ids, 6),
    "case_id": rand_choice(cases["case_id"].values, N_SUSPECTS),
    "citizen_id": rand_choice(citizens["citizen_id"].values, N_SUSPECTS),
    "role": rand_choice(SUSPECT_ROLES, N_SUSPECTS),
    "arrest_status": rand_choice(ARREST_STATUS, N_SUSPECTS),
})
save("suspects", suspects)

vic_ids = np.arange(1, N_VICTIMS + 1)
victims = pd.DataFrame({
    "victim_id": zpad("VIC", vic_ids, 6),
    "case_id": rand_choice(cases["case_id"].values, N_VICTIMS),
    "citizen_id": rand_choice(citizens["citizen_id"].values, N_VICTIMS),
    "injury_level": rand_choice(pd.array(INJURY, dtype="object"), N_VICTIMS),
})
save("victims", victims)

# ============================================================
# 10. phones / 11. vehicles / 12. bank_accounts
# ============================================================
ph_ids = np.arange(1, N_PHONES + 1)
phones = pd.DataFrame({
    "phone_id": zpad("PH", ph_ids, 6),
    "citizen_id": rand_choice(citizens["citizen_id"].values, N_PHONES),
    "phone_number": [f"9{np.random.randint(100000000, 999999999)}" for _ in range(N_PHONES)],
    "provider": rand_choice(PROVIDERS, N_PHONES),
})
save("phones", phones)

vh_ids = np.arange(1, N_VEHICLES + 1)
vehicles = pd.DataFrame({
    "vehicle_id": zpad("VH", vh_ids, 6),
    "citizen_id": rand_choice(citizens["citizen_id"].values, N_VEHICLES),
    "vehicle_number": [f"KA{np.random.randint(1,99):02d}AB{np.random.randint(1000,9999)}" for _ in range(N_VEHICLES)],
    "vehicle_type": rand_choice(VEHICLE_TYPES, N_VEHICLES),
})
save("vehicles", vehicles)

acc_ids = np.arange(1, N_BANK_ACCOUNTS + 1)
acc_bank = rand_choice(BANKS, N_BANK_ACCOUNTS)
bank_accounts = pd.DataFrame({
    "account_id": zpad("ACC", acc_ids, 6),
    "citizen_id": rand_choice(citizens["citizen_id"].values, N_BANK_ACCOUNTS),
    "bank_name": acc_bank,
    "account_number": [str(np.random.randint(100000000000, 999999999999)) for _ in range(N_BANK_ACCOUNTS)],
    "ifsc": [f"{BANK_CODE[b]}{np.random.randint(100000,999999)}" for b in acc_bank],
})
save("bank_accounts", bank_accounts)

# ============================================================
# 13. evidence / 14. digital_evidence
# ============================================================
ev_ids = np.arange(1, N_EVIDENCE + 1)
evidence = pd.DataFrame({
    "evidence_id": zpad("EV", ev_ids, 6),
    "case_id": rand_choice(cases["case_id"].values, N_EVIDENCE),
    "evidence_type": rand_choice(EVIDENCE_TYPES, N_EVIDENCE),
    "description": [fake.sentence(nb_words=6) for _ in range(N_EVIDENCE)],
    "status": rand_choice(EVIDENCE_STATUS, N_EVIDENCE),
    "collected_by": rand_choice(officers["officer_id"].values, N_EVIDENCE),
})
save("evidence", evidence)

de_ids = np.arange(1, N_DIGITAL_EVIDENCE + 1)
de_phone = [f"9{np.random.randint(100000000, 999999999)}" for _ in range(N_DIGITAL_EVIDENCE)]
de_email = [f"{fake.user_name()}{i}@example.org" for i in de_ids]
de_ip = [fake.ipv4_public() for _ in range(N_DIGITAL_EVIDENCE)]
digital_evidence = pd.DataFrame({
    "digital_evidence_id": zpad("DE", de_ids, 6),
    "case_id": rand_choice(cases["case_id"].values, N_DIGITAL_EVIDENCE),
    "file_type": rand_choice(DE_TYPES, N_DIGITAL_EVIDENCE),
    "file_name": [f"{fake.word()}.{np.random.choice(['txt','csv','pdf','jpg'])}" for _ in range(N_DIGITAL_EVIDENCE)],
    "phone_number": de_phone,
    "email": de_email,
    "ip_address": de_ip,
    "uploaded_by": rand_choice(officers["officer_id"].values, N_DIGITAL_EVIDENCE),
    "status": rand_choice(DE_STATUS, N_DIGITAL_EVIDENCE),
    "extracted_entities": [f"Phone: {p}; Email: {e}; IP: {i}" for p, e, i in zip(de_phone, de_email, de_ip)],
})
save("digital_evidence", digital_evidence)

# ============================================================
# 15. criminal_relationships (citizen_1 != citizen_2)
# ============================================================
c1 = np.random.choice(citizens["citizen_id"].values, N_RELATIONSHIPS)
c2 = np.random.choice(citizens["citizen_id"].values, N_RELATIONSHIPS)
same = c1 == c2
while same.any():
    c2[same] = np.random.choice(citizens["citizen_id"].values, same.sum())
    same = c1 == c2
rel_ids = np.arange(1, N_RELATIONSHIPS + 1)
criminal_relationships = pd.DataFrame({
    "relationship_id": zpad("REL", rel_ids, 6),
    "citizen_1": c1,
    "citizen_2": c2,
    "relationship_type": rand_choice(REL_TYPES, N_RELATIONSHIPS),
})
save("criminal_relationships", criminal_relationships)

# ============================================================
# 16. investigation_notes / 17. timeline
# ============================================================
note_ids = np.arange(1, N_NOTES + 1)
investigation_notes = pd.DataFrame({
    "note_id": zpad("NOTE", note_ids, 6),
    "case_id": rand_choice(cases["case_id"].values, N_NOTES),
    "officer_id": rand_choice(officers["officer_id"].values, N_NOTES),
    "note": [fake.sentence(nb_words=8) for _ in range(N_NOTES)],
})
save("investigation_notes", investigation_notes)

tl_ids = np.arange(1, N_TIMELINE + 1)
timeline = pd.DataFrame({
    "event_id": zpad("TIME", tl_ids, 6),
    "case_id": rand_choice(cases["case_id"].values, N_TIMELINE),
    "event": rand_choice(EVENTS, N_TIMELINE),
})
save("timeline", timeline)

# ============================================================
# 18. search_index — genuinely linked to real entity values, like augment_dataset.py
# ============================================================
si_ids = np.arange(1, N_SEARCH_INDEX + 1)
entity_types = rand_choice(["Citizen", "Phone", "Vehicle", "Bank", "Officer", "Case"], N_SEARCH_INDEX)
entity_values = np.empty(N_SEARCH_INDEX, dtype=object)
si_case_id = np.empty(N_SEARCH_INDEX, dtype=object)

for et, pool_df, val_col, case_col in [
    ("Citizen", citizens, "citizen_id", None),
    ("Phone", phones, "phone_number", None),
    ("Vehicle", vehicles, "vehicle_number", None),
    ("Bank", bank_accounts, "account_number", None),
    ("Officer", officers, "officer_id", None),
    ("Case", cases, "fir_number", "case_id"),
]:
    mask = entity_types == et
    cnt = mask.sum()
    if cnt == 0:
        continue
    sample = pool_df.sample(n=cnt, replace=True, random_state=42)
    entity_values[mask] = sample[val_col].values
    if case_col:
        si_case_id[mask] = sample[case_col].values
    else:
        si_case_id[mask] = np.random.choice(cases["case_id"].values, cnt)

search_index = pd.DataFrame({
    "search_id": zpad("SRCH", si_ids, 6),
    "entity_type": entity_types,
    "entity_value": entity_values,
    "case_id": si_case_id,
})
save("search_index", search_index)

# ============================================================
# 19. audit_logs
# ============================================================
log_ids = np.arange(1, N_AUDIT_LOGS + 1)
audit_logs = pd.DataFrame({
    "log_id": zpad("LOG", log_ids, 6),
    "user_id": rand_choice(users["user_id"].values, N_AUDIT_LOGS),
    "action": rand_choice(ACTIONS, N_AUDIT_LOGS),
    "case_id": rand_choice(cases["case_id"].values, N_AUDIT_LOGS),
    "timestamp": dates_between("2026-06-01", "2026-07-21", N_AUDIT_LOGS),
    "ip_address": [fake.ipv4_private() for _ in range(N_AUDIT_LOGS)],
})
save("audit_logs", audit_logs)

print("\nDone. Total rows:", sum(len(x) for x in [
    police_stations, roles, citizens, officers, users, crime_patterns, cases,
    suspects, victims, phones, vehicles, bank_accounts, evidence, digital_evidence,
    criminal_relationships, investigation_notes, timeline, search_index, audit_logs
]))
