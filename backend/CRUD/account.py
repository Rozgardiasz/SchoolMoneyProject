# Create a new Account
from sqlalchemy.orm import Session

from models import Account


def create_account(db: Session, account_number: str, balance: float, child_id: int) -> Account:
    db_account = Account(account_number=account_number, balance=balance, child_id=child_id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

# Get an Account by ID
def get_account(db: Session, account_id: int) -> Account:
    return db.query(Account).filter(Account.id == account_id).first()

# Update an Account's details
def update_account(db: Session, account_id: int, balance: float) -> Account:
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if db_account:
        db_account.balance = balance
        db.commit()
        db.refresh(db_account)
        return db_account
    else:
        return None

# Delete an Account
def delete_account(db: Session, account_id: int):
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if db_account:
        db.delete(db_account)
        db.commit()
