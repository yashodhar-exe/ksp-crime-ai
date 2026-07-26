import os
import subprocess

os.environ["DATABASE_URL"] = "postgresql://neondb_owner:npg_LsmV1DQP8FXc@ep-frosty-fog-azsfh9vh-pooler.c-3.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
subprocess.run(["python", "create_admin_force.py"])
