# Create a new Collection
from sqlalchemy.orm import Session

from models import Collection


def create_collection(db: Session, title: str, description: str, start_date: str, end_date: str, class_id: int, creator_id: int) -> Collection:
    db_collection = Collection(title=title, description=description, start_date=start_date, end_date=end_date, class_id=class_id, creator_id=creator_id)
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection

# Get a Collection by ID
def get_collection(db: Session, collection_id: int) -> Collection:
    return db.query(Collection).filter(Collection.id == collection_id).first()

# Update a Collection's details
def update_collection(db: Session, collection_id: int, title: str, description: str, start_date: str, end_date: str) -> Collection:
    db_collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if db_collection:
        db_collection.title = title
        db_collection.description = description
        db_collection.start_date = start_date
        db_collection.end_date = end_date
        db.commit()
        db.refresh(db_collection)
        return db_collection
    else:
        return None

# Delete a Collection
def delete_collection(db: Session, collection_id: int):
    db_collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if db_collection:
        db.delete(db_collection)
        db.commit()
