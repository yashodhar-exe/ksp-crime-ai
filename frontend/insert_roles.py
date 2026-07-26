import sqlalchemy
from sqlalchemy import create_engine, text

url = "postgresql://neondb_owner:npg_LsmV1DQP8FXc@ep-frosty-fog-azsfh9vh-pooler.c-3.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

roles = [
  {"role_id": "R2", "role_name": "SP", "level": 2, "can_view_all_districts": True, "can_export": True, "can_edit_case": True, "can_manage_users": False},
  {"role_id": "R3", "role_name": "DSP", "level": 3, "can_view_all_districts": False, "can_export": True, "can_edit_case": True, "can_manage_users": False},
  {"role_id": "R4", "role_name": "Inspector", "level": 4, "can_view_all_districts": False, "can_export": True, "can_edit_case": True, "can_manage_users": False},
  {"role_id": "R5", "role_name": "Sub Inspector", "level": 5, "can_view_all_districts": False, "can_export": False, "can_edit_case": True, "can_manage_users": False},
  {"role_id": "R6", "role_name": "Constable", "level": 6, "can_view_all_districts": False, "can_export": False, "can_edit_case": False, "can_manage_users": False},
]

try:
    engine = create_engine(url)
    with engine.connect() as conn:
        with conn.begin():
            print("Connected!")
            for role in roles:
                res = conn.execute(text("SELECT role_id FROM roles WHERE role_id = :r"), {"r": role["role_id"]})
                if not res.fetchone():
                    print(f"Inserting {role['role_name']}")
                    conn.execute(
                        text("INSERT INTO roles (role_id, role_name, level, can_view_all_districts, can_export, can_edit_case, can_manage_users) VALUES (:role_id, :role_name, :level, :can_view_all_districts, :can_export, :can_edit_case, :can_manage_users)"), 
                        role
                    )
                else:
                    print(f"Role {role['role_name']} already exists")
    print("Done!")
except Exception as e:
    import traceback
    traceback.print_exc()
