from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    Boolean,
    Float,
    Text,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# User account model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    profile_picture = Column(String, nullable=True)  # Path to avatar image
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    children = relationship("Child", back_populates="parent")
    classes_managed = relationship("Class", back_populates="treasurer")
    created_collections = relationship("Collection", back_populates="creator")
    account = relationship("Account", back_populates="parent", uselist=False)

# Child model
class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    avatar = Column(String, nullable=True)  # Path to avatar image

    # Foreign key to parent
    parent_id = Column(Integer, ForeignKey("users.id"))
    parent = relationship("User", back_populates="children")

    # Foreign key to class
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)
    class_ = relationship("Class", back_populates="children")

class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    treasurer_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Managed by the treasurer
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    treasurer = relationship("User", back_populates="classes_managed")
    collections = relationship("Collection", back_populates="class_")
    children = relationship("Child", back_populates="class_")  # One-to-many relationship with children


# Account model
class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, nullable=False)  # Unique account number
    balance = Column(Float, default=0.0)

    # Foreign keys
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Account owned by a parent
    collection_id = Column(Integer, ForeignKey("collections.id"), nullable=True)  # Account for a collection

    # Relationships
    parent = relationship("User", back_populates="account")
    collection = relationship("Collection", back_populates="account")

    # Transactions where this account is source or destination
    outgoing_transactions = relationship(
        "FinancialTransaction",
        back_populates="source_account",
        primaryjoin="Account.id == FinancialTransaction.source_account_id",
        foreign_keys="[FinancialTransaction.source_account_id]"
    )

    # Explicitly specifying the join condition for incoming transactions
    incoming_transactions = relationship(
        "FinancialTransaction",
        back_populates="destination_account",
        primaryjoin="Account.id == FinancialTransaction.destination_account_id",
        foreign_keys="[FinancialTransaction.destination_account_id]"

    )



class FinancialTransaction(Base):
    __tablename__ = "financial_transactions"

    id = Column(Integer, primary_key=True, index=True)
    source_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)  # Account sending the funds
    destination_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)  # Account receiving the funds
    amount = Column(Float, nullable=False)  # Transaction amount
    description = Column(Text, nullable=True)  # Optional description of the transaction
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    source_account = relationship("Account", back_populates="outgoing_transactions",foreign_keys=[source_account_id])
    destination_account = relationship("Account", back_populates="incoming_transactions",foreign_keys=[destination_account_id]
)


# Collection model
class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    goal = Column(Float,nullable = False)
    title = Column(String, nullable=False)
    logo = Column(String, nullable=True)  # Path to logo image
    description = Column(Text, nullable=False)  # Description provided by the treasurer
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    # Foreign keys
    class_id = Column(Integer, ForeignKey("classes.id"))  # Class this collection belongs to
    creator_id = Column(Integer, ForeignKey("users.id"))  # Treasurer who created the collection

    # Relationships
    class_ = relationship("Class", back_populates="collections")
    creator = relationship("User", back_populates="created_collections")
    account = relationship("Account", back_populates="collection", uselist=False)  # One account per collection
