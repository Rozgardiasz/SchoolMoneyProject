# Create a new Financial Transaction
from sqlalchemy.orm import Session

from models import FinancialTransaction


def create_transaction(db: Session, account_id: int, amount: float, transaction_type: str) -> FinancialTransaction:
    db_transaction = FinancialTransaction(account_id=account_id, amount=amount, transaction_type=transaction_type)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# Get a Financial Transaction by ID
def get_transaction(db: Session, transaction_id: int) -> FinancialTransaction:
    return db.query(FinancialTransaction).filter(FinancialTransaction.id == transaction_id).first()

# Delete a Financial Transaction
def delete_transaction(db: Session, transaction_id: int):
    db_transaction = db.query(FinancialTransaction).filter(FinancialTransaction.id == transaction_id).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
