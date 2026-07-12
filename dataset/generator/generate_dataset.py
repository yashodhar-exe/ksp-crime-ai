import pandas as pd
import random
import os

os.makedirs("output", exist_ok=True)

records=[]

entity_types=[
    "Phone",
    "Citizen",
    "Vehicle",
    "Bank",
    "Officer",
    "Case"
]

for i in range(1,30001):

    entity=random.choice(entity_types)

    if entity=="Phone":
        value="9"+"".join(str(random.randint(0,9)) for _ in range(9))

    elif entity=="Citizen":
        value=f"CID{random.randint(1,10000):06}"

    elif entity=="Vehicle":
        value=f"KA{random.randint(1,99):02}AB{random.randint(1000,9999)}"

    elif entity=="Bank":
        value=str(random.randint(100000000000,999999999999))

    elif entity=="Officer":
        value=f"OFF{random.randint(1,500):05}"

    else:
        value=f"CASE{random.randint(1,10000):06}"

    records.append({

        "search_id":f"SRCH{i:06}",

        "entity_type":entity,

        "entity_value":value,

        "case_id":f"CASE{random.randint(1,10000):06}"
    })

df=pd.DataFrame(records)

df.to_csv("output/search_index.csv",index=False)

print("✅ search_index.csv Generated")