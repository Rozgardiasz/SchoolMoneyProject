# Create a new Child
from typing import List, Any

from sqlalchemy.orm import Session

from models import Child


def create_child(db: Session, first_name: str, last_name: str, birth_date: str, parent_id: int) -> Child:
    db_child = Child(first_name=first_name, last_name=last_name, birth_date=birth_date, parent_id=parent_id)
    db.add(db_child)
    db.commit()
    db.refresh(db_child)
    return db_child


# Get a Child by ID
def get_child(db: Session, child_id: int) -> Child:
    return db.query(Child).filter(Child.id == child_id).first()


def get_children(db: Session, parent_id: int) -> List[Child]:
    return db.query(Child).filter(Child.parent_id == parent_id).all()


# Update a Child's details
def update_child(db: Session, child_id: int, first_name: str, last_name: str, birth_date: str, parent_id: int) -> Any | None:
    db_child = db.query(Child).filter(Child.id == child_id).first()
    if db_child:
        db_child.first_name = first_name
        db_child.last_name = last_name
        db_child.birth_date = birth_date
        db_child.parent_id = parent_id
        db.commit()
        db.refresh(db_child)
        return db_child
    else:
        return None


# Delete a Child
def delete_child(db: Session, child_id: int):
    db_child = db.query(Child).filter(Child.id == child_id).first()
    if db_child:
        db.delete(db_child)
        db.commit()
        return True
    else:
        return False
