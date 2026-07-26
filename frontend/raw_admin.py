import sqlalchemy
from sqlalchemy import create_engine, text

url = "postgresql://neondb_owner:npg_LsmV1DQP8FXc@ep-frosty-fog-azsfh9vh-pooler.c-3.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
hashed = "$2b$12$mngRqxKVqcurYiYWK2rDYOIApHRSxEVhTkg4ZoIDEq2BUDtpKVgsy"

try:
    engine = create_engine(url)
    with engine.connect() as conn:
        with conn.begin():
            print("Connected!")
            
            # 1. get admin role
            res = conn.execute(text("SELECT role_id FROM roles WHERE role_name = 'Admin'"))
            role_row = res.fetchone()
            if role_row:
                role_id = role_row[0]
            else:
                print("Inserting admin role")
                conn.execute(text("INSERT INTO roles (role_id, role_name, level, can_view_all_districts, can_export, can_edit_case, can_manage_users) VALUES ('R1', 'Admin', 1, true, true, true, true)"))
                role_id = 'R1'
                
            # 2. check if user exists
            res = conn.execute(text("SELECT user_id FROM users WHERE username = 'admin.ksp'"))
            user_row = res.fetchone()
            if user_row:
                print("Updating user")
                conn.execute(text("UPDATE users SET hashed_password = :h, role_id = :r, status = 'Active' WHERE username = 'admin.ksp'"), {"h": hashed, "r": role_id})
            else:
                print("Inserting user")
                import uuid
                u_id = f"U{uuid.uuid4().hex[:9].upper()}"
                conn.execute(text("INSERT INTO users (user_id, username, hashed_password, role_id, status) VALUES (:u, 'admin.ksp', :h, :r, 'Active')"), {"u": u_id, "h": hashed, "r": role_id})
                
    print("Done!")
except Exception as e:
    import traceback
    traceback.print_exc()
