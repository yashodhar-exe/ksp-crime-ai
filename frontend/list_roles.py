import sqlalchemy
from sqlalchemy import create_engine, text

url = "postgresql://neondb_owner:npg_LsmV1DQP8FXc@ep-frosty-fog-azsfh9vh-pooler.c-3.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

try:
    engine = create_engine(url)
    with engine.connect() as conn:
        res = conn.execute(text("SELECT role_id, role_name FROM roles"))
        for row in res.fetchall():
            print(row)
except Exception as e:
    import traceback
    traceback.print_exc()
