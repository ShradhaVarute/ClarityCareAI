"""
One-off script to create the first admin account, run manually against a
real database. Needed because the API's own admin-creation endpoint
(POST /admin/users) requires an existing admin to call it — this script is
how you create that first admin.

Usage (from backend/):
    DATABASE_URL=postgresql://... python -m scripts.create_admin
"""
import getpass
import sys

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User


def main() -> None:
    email = input("Admin email: ").strip()
    password = getpass.getpass("Admin password (min 8 chars): ")
    if len(password) < 8:
        print("Password must be at least 8 characters.", file=sys.stderr)
        sys.exit(1)

    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"A user with email {email!r} already exists (role={existing.role}).", file=sys.stderr)
            sys.exit(1)

        admin = User(email=email, hashed_password=hash_password(password), role="admin")
        db.add(admin)
        db.commit()
        print(f"Created admin user: {email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
