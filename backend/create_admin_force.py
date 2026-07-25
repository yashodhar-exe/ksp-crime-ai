from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.role import Role
from app.models.user import User
import uuid

def _generate_user_id() -> str:
    return f"U{uuid.uuid4().hex[:9].upper()}"

db = SessionLocal()
try:
    admin_role = db.query(Role).filter(Role.role_name == "Admin").first()
    if not admin_role:
        print("Admin role not found! Creating it...")
        admin_role = Role(
            role_id="R1", 
            role_name="Admin", 
            level=1, 
            can_view_all_districts=True, 
            can_export=True, 
            can_edit_case=True, 
            can_manage_users=True
        )
        db.add(admin_role)
        db.commit()
    
    username = "admin.ksp"
    password = "ksp@2026" # Admin password
    
    # Demote all other admins to ensure there is a single admin
    other_admins = db.query(User).filter(User.role_id == admin_role.role_id, User.username != username).all()
    for o_admin in other_admins:
        o_admin.status = "Inactive"

    
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        existing.role_id = admin_role.role_id
        existing.status = "Active"
        existing.hashed_password = hash_password(password)
        print(f"Updated {username} password to {password}")
    else:
        user = User(
            user_id=_generate_user_id(),
            username=username,
            hashed_password=hash_password(password),
            role_id=admin_role.role_id,
            status="Active",
        )
        db.add(user)
        print(f"Created {username} password to {password}")
    db.commit()
finally:
    db.close()
