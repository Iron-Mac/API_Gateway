from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from passlib.context import CryptContext

# Create a password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_admin_user(db: Session, username: str, password: str, phone_number: str):
    hashed_password = pwd_context.hash(password)
    admin_user = User(username=username, password_hash=hashed_password, phone_number=phone_number, is_admin=True, is_registerer=True, is_verified=True)
    db.add(admin_user)
    db.commit()


def main():
    db = SessionLocal()

    # Take admin username and password from the user
    admin_username = input("Enter admin username: ")
    admin_password = input("Enter admin password: ")
    admin_phone_number = input("Enter admin phone_number: ")

    create_admin_user(db, admin_username, admin_password, admin_phone_number)
    db.close()
    print(f"Admin user '{admin_username}' created successfully.")


if __name__ == "__main__":
    main()
