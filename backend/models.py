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
    memberships = relationship("ClassMembership", back_populates="parent")
    created_collections = relationship("Collection", back_populates="creator")

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

    # Relationships
    accounts = relationship("Account", back_populates="child")

# Class model
class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    treasurer_id = Column(Integer, ForeignKey("users.id"))  # Managed by Skarbnik
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    treasurer = relationship("User", back_populates="classes_managed")
    memberships = relationship("ClassMembership", back_populates="class_")
    collections = relationship("Collection", back_populates="class_")

# ClassMembership model
class ClassMembership(Base):
    __tablename__ = "class_memberships"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("users.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))

    # Relationships
    parent = relationship("User", back_populates="memberships")
    class_ = relationship("Class", back_populates="memberships")

# Account model
class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, nullable=False)  # Unique account number
    balance = Column(Float, default=0.0)

    # Foreign key to child
    child_id = Column(Integer, ForeignKey("children.id"))
    child = relationship("Child", back_populates="accounts")

    # Add the relationship for transactions
    transactions = relationship("FinancialTransaction", back_populates="account")


class FinancialTransaction(Base):
    __tablename__ = "financial_transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)  # 'deposit' or 'withdrawal'
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    account = relationship("Account", back_populates="transactions")

# Collection model
class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    logo = Column(String, nullable=True)  # Path to logo image
    description = Column(Text, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    # Foreign keys
    class_id = Column(Integer, ForeignKey("classes.id"))
    creator_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    class_ = relationship("Class", back_populates="collections")
    creator = relationship("User", back_populates="created_collections")
    contributions = relationship("Contribution", back_populates="collection")
    payouts = relationship("Payout", back_populates="collection")

# Contribution model
class Contribution(Base):
    __tablename__ = "contributions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    contributor_id = Column(Integer, ForeignKey("users.id"))
    collection_id = Column(Integer, ForeignKey("collections.id"))
    paid_for_child_id = Column(Integer, ForeignKey("children.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    contributor = relationship("User")
    collection = relationship("Collection", back_populates="contributions")
    paid_for_child = relationship("Child")

# Payout model
class Payout(Base):
    __tablename__ = "payouts"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    collection_id = Column(Integer, ForeignKey("collections.id"))
    recipient_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    collection = relationship("Collection", back_populates="payouts")
    recipient = relationship("User")
