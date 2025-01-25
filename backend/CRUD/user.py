from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

# Create a new User
from models import User


def create_user(db: Session, name: str, email: str, hashed_password: str, role: str) -> User:
    db_user = User(name=name, email=email, hashed_password=hashed_password, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get a User by ID
def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

# Update a User's details
def update_user(db: Session, user_id: int, name: str, email: str, hashed_password: str, role: str) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.name = name
        db_user.email = email
        db_user.hashed_password = hashed_password
        db_user.role = role
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        return None

# Delete a User
def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
