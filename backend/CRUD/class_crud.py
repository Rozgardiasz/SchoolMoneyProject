# Create a new Class
from sqlalchemy.orm import Session

from models import Class


def create_class(db: Session, name: str, treasurer_id: int) -> Class:
    db_class = Class(name=name, treasurer_id=treasurer_id)
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

# Get a Class by ID
def get_class(db: Session, class_id: int) -> Class:
    return db.query(Class).filter(Class.id == class_id).first()

# Update a Class' details
def update_class(db: Session, class_id: int, name: str, school_name: str, treasurer_id: int) -> Class:
    db_class = db.query(Class).filter(Class.id == class_id).first()
    if db_class:
        db_class.name = name
        db_class.school_name = school_name
        db_class.treasurer_id = treasurer_id
        db.commit()
        db.refresh(db_class)
        return db_class
    else:
        return None

# Delete a Class
def delete_class(db: Session, class_id: int):
    db_class = db.query(Class).filter(Class.id == class_id).first()
    if db_class:
        db.delete(db_class)
        db.commit()
