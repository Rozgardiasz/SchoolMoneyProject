import uuid
from datetime import timedelta
from typing import List
from apscheduler.schedulers.background import BackgroundScheduler

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
from sqlalchemy import or_

import CRUD.child
import auth
import models
from auth import verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, decode_access_token, hash_password
from models import *
from schemas import Token, UserResponse, UserCreate, LoginRequest, ChildResponse, ChildCreate, ClassResponse, \
    ClassCreate, ChildModify, ClassModify, AddChildToClass, CollectionResponse, CollectionCreate, AccountResponse, \
    FinancialTransactionCreate, FinancialTransactionResponse, ProcessInviteRequest, CreateInviteRequest, \
    CollectionModify

app = FastAPI(debug=True)
scheduler = BackgroundScheduler()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

from database import engine, SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    models.Base.metadata.create_all(bind=engine)

from sqlalchemy.orm import Session
from datetime import datetime
from models import Collection, Account, FinancialTransaction
from fastapi import HTTPException

def transfer_funds_on_collection_end():
    # Get the current date
    current_date = datetime.utcnow()
    db: Session = SessionLocal()


    # Fetch all collections that have ended
    collections_to_process = db.query(Collection).filter(Collection.end_date <= current_date).all()

    for collection in collections_to_process:
        # Ensure the collection has funds
        if collection.account.balance > 0:
            # Get the creator of the collection
            creator_account = db.query(Account).filter(Account.user_id == collection.creator_id).first()

            if not creator_account:
                raise HTTPException(status_code=404, detail="Creator account not found")

            # Get the amount to transfer
            transfer_amount = collection.account.balance

            # Transfer funds from the collection's account to the creator's account
            # Create a financial transaction
            transaction = FinancialTransaction(
                source_account_id=collection.account.id,
                destination_account_id=creator_account.id,
                amount=transfer_amount,
                description="Transfer of funds from collection to creator after collection end date",
                timestamp=datetime.utcnow(),
            )
            db.add(transaction)
            db.commit()

            # Update collection account balance to zero
            collection.account.balance = 0
            db.commit()


    return {"message": "Funds transfer process completed."}




@app.post("/register/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the email is already registered
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="email zajety")

    # Create the user with hashed password
    hashed_password = hash_password(user.password)
    db_user = User(
        first_name=user.first_name, last_name=user.last_name , email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    account_number = str(uuid.uuid4())  # Example: Unique identifier
    account = Account(
        account_number=account_number,
        balance=100.0,  # Initial balance is set to 0
        parent_id=db_user.id  # Link the account to the newly created user
    )

    # Step 5: Add the account to the database and commit
    db.add(account)
    db.commit()
    db.refresh(account)  # To get the latest data (e.g., auto-generated id)
    return UserResponse(
        id=db_user.id,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        email=db_user.email,
        created_at = db_user.created_at,
        account=AccountResponse.from_orm(account)  # Return AccountResponse instead of plain account
    )


# Login route to generate JWT token
@app.post("/login/", response_model=Token)
def login(user: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/get_user/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    # Query the database for the user with the given ID
    user = db.query(User).filter(User.id == user_id).first()

    # If user is not found, raise an HTTP exception
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Return the user data
    return UserResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        created_at = user.created_at,
        account=AccountResponse.from_orm(user.account)  # Convert related account to AccountResponse
    )


# Dependency to get the current logged-in user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_email = payload.get("sub")
    if user_email is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.email == user_email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# Protected route that requires a valid token
@app.get("/me/", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,
        created_at = current_user.created_at,
        account=AccountResponse.from_orm(current_user.account)  # Convert related account to AccountResponse
    )

@app.post("/children/", response_model=ChildResponse)
def create_child(
        child: ChildCreate,  # Input schema for creating a child
        current_user: User = Depends(get_current_user),  # Logged-in parent
        db: Session = Depends(get_db)
):
    return CRUD.child.create_child(db, child.first_name, child.last_name, child.birth_date.__str__(), current_user.id)


@app.get("/children/", response_model=List[ChildResponse])
def read_children(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return CRUD.child.get_children(db, current_user.id)


@app.put("/children/{child_id}", response_model=ChildResponse)
def update_child(
        child_id: int,
        child: ChildModify,  # Assuming this schema is used for child updates
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    result = CRUD.child.update_child(db, child_id, child.first_name, child.last_name, str(child.birth_date),
                                     current_user.id)
    if result is None:
        raise HTTPException(401, detail="Child not found or not owned by the current user")
    return result


@app.delete("/children/{child_id}", response_model=ChildResponse)
def delete_child(
        child_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if current_user.id != CRUD.child.get_child(db, child_id).parent_id:
        raise HTTPException(401, detail="Child not found or not owned by the current user")

    res = CRUD.child.delete_child(db, child_id)
    if not res:
        raise HTTPException(401, detail="Child not found or not owned by the current user")


@app.post("/class/", response_model=ClassResponse)
def create_class(
        class_data: ClassCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Create the class
    db_class = Class(name=class_data.name, treasurer_id=current_user.id)
    db.add(db_class)

    # Commit the transaction to save the class and generate its ID
    db.commit()


    return db_class


@app.get("/user_classes/", response_model=List[ClassResponse])
def get_user_classes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Join Class with Child to get the classes where the parent has a child
    return db.query(Class).join(Child, Child.class_id == Class.id, isouter=True).filter(
        or_(Child.parent_id == current_user.id, Class.treasurer_id == current_user.id)).all()


@app.get("/all_classes", response_model=List[ClassResponse])
def get_all_classes(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Class).all()


# NOTE this only modifies class name
@app.put("/class/{class_id}", response_model=ClassResponse)
def modify_class(
        class_id: int,
        class_data: ClassModify,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    # Fetch the class from the database
    db_class = db.query(Class).filter(Class.id == class_id).first()
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")

    # Check if the current user is the treasurer
    if current_user.id != db_class.treasurer_id:
        raise HTTPException(status_code=400, detail="User is not the treasurer of the class")

    # Update the class name
    db_class.name = class_data.name
    db.commit()
    db.refresh(db_class)

    return db_class


@app.get("/users/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if the current user is a treasurer of any class
    is_treasurer = (
        db.query(Class)
            .join(User)
            .filter(Class.treasurer_id == current_user.id)
            .first()
    )
    if not is_treasurer:
        raise HTTPException(
            status_code=403,  # Forbidden instead of Bad Request
            detail="Obecny użytkownik nie jest skarbnikiem w żadnej klasie. Tylko skarbnik może widzieć wszystkich użytkowników."
        )

    # Get all users except the current one
    users = db.query(User).filter(User.id != current_user.id).all()

    # Return the list of users as UserResponse models
    return [UserResponse.from_orm(user) for user in users]

@app.post("/add_child_to_class/")
def add_child_to_class(params : AddChildToClass, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Validate if the child belongs to the current user
    child = db.query(Child).filter(Child.id == params.child_id, Child.parent_id == current_user.id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child does not belong to the current user")

    # Validate if the class exists
    class_ = db.query(Class).filter(Class.id == params.class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")

    # Assign the child to the class
    child.class_id = class_.id  # Set the class_id to link the child to the class
    db.commit()  # Commit the changes to the database
    db.refresh(child)

    # Return the updated child object
    return child

@app.get("/get_class/{class_id}",response_model=ClassResponse)
def get_class_by_id(
        class_id : int,
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user)
):
    return db.query(Class).filter(Class.id == class_id).first()

@app.post("/create_collection/", response_model=CollectionResponse)
def create_collection(
        collection : CollectionCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Step 1: Validate if the current user is a treasurer for the given class
    class_ = db.query(Class).filter(Class.id == collection.class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")

    if class_.treasurer_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to create collections for this class")

    # Step 2: Create the new collection
    collection = Collection(
        title=collection.title,
        goal= collection.goal,
        description=collection.description,
        start_date=collection.start_date,
        end_date=collection.end_date,
        class_id=collection.class_id,
        creator_id=current_user.id  # Set the creator to the current user
    )

    # Step 3: Add the collection to the database and commit
    db.add(collection)
    db.commit()
    db.refresh(collection)  # To get the latest data (e.g., auto-generated id)


    account_number = str(uuid.uuid4())  # Example: Unique identifier
    account = Account(
        account_number=account_number,
        balance=0.0,  # Initial balance is set to 0
        collection_id=collection.id  # Link the account to the newly created collection
    )

    # Step 5: Add the account to the database and commit
    db.add(account)
    db.commit()
    db.refresh(account)  # To get the latest data (e.g., auto-generated id)

    # Step 4: Return the created collection
    return CollectionResponse(
        id=collection.id,
        goal= collection.goal,
        title=collection.title,
        description=collection.description,
        start_date=collection.start_date,
        end_date=collection.end_date,
        class_id=collection.class_id,
        creator_id=collection.creator_id,
        account=AccountResponse.from_orm(account)  # Return AccountResponse instead of plain account
    )

@app.put("/modify_collection/{collection_id}", response_model=CollectionResponse)
def modify_collection(
    collection_id: int,
    data: CollectionModify,
    db: Session = Depends(get_db),
    current_user : User = Depends(get_current_user)

):
    # Fetch the collection by ID
    collection = db.query(Collection).filter(Collection.id == collection_id).first()

    # Check if the collection exists
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    class_ = db.query(Class).filter(Class.id == collection.class_id).first()

    if not class_ or class_.treasurer_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to modify this collection")



    # Update only the fields provided in the request
    if data.goal is not None:
        collection.goal = data.goal
    if data.title is not None:
        collection.title = data.title
    if data.description is not None:
        collection.description = data.description
    if data.end_date is not None:
        if data.end_date > collection.end_date:
            collection.end_date = data.end_date
        else:
            raise HTTPException(status_code=402,detail="End date cannot be earlier than current end date")

    # Commit the changes
    db.commit()
    db.refresh(collection)

    # Return the updated collection
    return collection




@app.get("/get_children_in_class/{class_id}", response_model=List[ChildResponse])
def get_children_in_class(
        class_id : int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    is_authorized = (
        db.query(Class)
        .join(Child, Child.class_id == Class.id, isouter=True)
        .filter(
            Class.id == class_id,
            or_(
                Child.parent_id == current_user.id,
                Class.treasurer_id == current_user.id
            )
        )
        .first()
    )

    if not is_authorized:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to view this class."
        )

    # Retrieve children in the class
    children = db.query(Child).filter(Child.class_id == class_id).all()

    return children

@app.get("/get_collections_in_class/{class_id}", response_model=List[CollectionResponse])
def get_collections_in_class(
        class_id : int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    is_authorized = (
        db.query(Class)
        .join(Child, Child.class_id == Class.id, isouter=True)
        .filter(
            Class.id == class_id,
            or_(
                Child.parent_id == current_user.id,
                Class.treasurer_id == current_user.id
            )
        )
        .first()
    )

    if not is_authorized:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to view this class."
        )

    # Retrieve collections in the class
    children = db.query(Collection).filter(Collection.class_id == class_id).all()

    return children

@app.post("/deposit/{amount}", response_model=AccountResponse)
def add_virtual_money_to_user_account(
        amount: float,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # Validate the amount
    if amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="The deposit amount must be greater than 0."
        )


    # Update the user's account balance
    current_user.account.balance += amount
    db.add(current_user.account)  # Ensure the account update is tracked

    # Create a financial transaction with a null source_account_id
    transaction = FinancialTransaction(
        source_account_id=None,  # Null for deposits
        destination_account_id=current_user.account.id,
        amount=amount,
        description="Virtual money deposit"
    )
    db.add(transaction)  # Add the transaction to the database

    db.commit()  # Commit the changes
    db.refresh(current_user.account)

    return current_user.account


from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

@app.post("/transfer/", response_model=AccountResponse)
def make_transfer(
    data: FinancialTransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if data.child_id:
        child = db.query(Child).filter(Child.id == data.child_id, Child.parent_id == current_user.id).first()

        if not child:
            raise HTTPException(
            status_code=400,
            detail="The child with given id doesn't exist or doesn't belong to this user"
            )
      # Check if the transfer is related to a collection account, it should when request has child id
        collection = (
            db.query(Collection)
            .filter(Collection.class_id == child.class_id, Collection.account_id == data.account_id)
            .first()
        )

        if not collection:
            raise HTTPException(
                status_code=400,
                detail="The transfer is not associated with a valid collection account."
            )

        # Check if the collection is still valid
        if collection.end_date < datetime.utcnow():
            raise HTTPException(
                status_code=400,
                detail="The collection associated with this account has expired."
            )


    # Find the destination account by account number
    destination_account = db.query(Account).filter(Account.account_number == data.account_number).first()
    if not destination_account:
        raise HTTPException(
            status_code=404,
            detail="Destination account not found."
        )

    # Ensure sufficient balance in the source account
    if current_user.account.balance < data.amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient funds in your account."
        )

    # Update balances
    current_user.account.balance -= data.amount
    destination_account.balance += data.amount

    # Create a financial transaction record
    transaction = FinancialTransaction(
        source_account_id=current_user.account.id,
        destination_account_id=destination_account.id,
        amount=data.amount,
        description=data.description or "",
        child_id=data.child_id
    )
    db.add(transaction)
    db.commit()
    db.refresh(current_user.account)

    # Return the updated account
    return current_user.account


@app.get("/transactions_for_collection/{collection_id}", response_model=List[FinancialTransactionResponse])
def transactions_for_collection(
    collection_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
):
    # Fetch the collection
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    # Fetch transactions for the collection's account
    transactions = (
        db.query(FinancialTransaction)
        .filter(
            (FinancialTransaction.source_account_id == collection.account.id) |
            (FinancialTransaction.destination_account_id == collection.account.id)
        )
        .all()
    )

    # Map transactions to response model
    response = []
    for transaction in transactions:
        # Determine the source
        if transaction.source_account.collection:
            source = CollectionResponse(
                id=transaction.source_account.collection.id,
                goal=transaction.source_account.collection.goal,
                title=transaction.source_account.collection.title,
                description=transaction.source_account.collection.description,
                start_date=transaction.source_account.collection.start_date,
                end_date=transaction.source_account.collection.end_date,
                class_id=transaction.source_account.collection.class_id,
                creator_id=transaction.source_account.collection.creator_id,
                account=AccountResponse(
                    id=transaction.source_account.id,
                    account_number=transaction.source_account.account_number,
                ),
            )
        else:
            source = UserResponse(
                id=transaction.source_account.parent.id,
                first_name=transaction.source_account.parent.first_name,
                last_name=transaction.source_account.parent.last_name,
                email=transaction.source_account.parent.email,
                created_at=transaction.source_account.parent.created_at,
                account=AccountResponse(
                    id=transaction.source_account.id,
                    account_number=transaction.source_account.account_number,
                ),
            )

        # Determine the destination
        if transaction.destination_account.collection:
            destination = CollectionResponse(
                id=transaction.destination_account.collection.id,
                goal=transaction.destination_account.collection.goal,
                title=transaction.destination_account.collection.title,
                description=transaction.destination_account.collection.description,
                start_date=transaction.destination_account.collection.start_date,
                end_date=transaction.destination_account.collection.end_date,
                class_id=transaction.destination_account.collection.class_id,
                creator_id=transaction.destination_account.collection.creator_id,
                account=AccountResponse(
                    id=transaction.destination_account.id,
                    account_number=transaction.destination_account.account_number,
                ),
            )
        else:
            destination = UserResponse(
                id=transaction.destination_account.parent.id,
                first_name=transaction.destination_account.parent.first_name,
                last_name=transaction.destination_account.parent.last_name,
                email=transaction.destination_account.parent.email,
                created_at=transaction.destination_account.parent.created_at,
                account=AccountResponse(
                    id=transaction.destination_account.id,
                    account_number=transaction.destination_account.account_number,
                ),
            )

        # Check if the transaction has an associated child
        child = None
        if transaction.child_id:
            # Fetch the child data
            child = db.query(Child).filter(Child.id == transaction.child_id).first()
            if child:
                child_response = ChildResponse(
                    id=child.id,
                    first_name=child.first_name,
                    last_name=child.last_name,
                    birth_date=child.birth_date
                    # Add more child details as needed
                )
            else:
                child_response = None
        else:
            child_response = None

        # Create a transaction response
        response.append(
            FinancialTransactionResponse(
                source=source,
                destination=destination,
                amount=transaction.amount,
                description=transaction.description,
                timestamp=transaction.timestamp,
                child=child_response  # Add child information if it exists
            )
        )

    return response


@app.get("/transactions_for_user", response_model=List[FinancialTransactionResponse])
def transactions_for_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Fetch the user's accounts
    user_account = current_user.account
    if not user_account:
        raise HTTPException(status_code=404, detail="User does not have an associated account")

    # Find all collections managed by the user and their accounts
    managed_collections = db.query(Collection).filter(Collection.creator_id == current_user.id).all()
    collection_account_ids = [collection.account.id for collection in managed_collections if collection.account]

    # Collect all account IDs to filter by
    account_ids = [user_account.id] + collection_account_ids

    # Fetch transactions where user's accounts are involved
    transactions = (
        db.query(FinancialTransaction)
        .filter(
            (FinancialTransaction.source_account_id.in_(account_ids)) |
            (FinancialTransaction.destination_account_id.in_(account_ids))
        )
        .all()
    )

    # Map transactions to response model
    response = []
    for transaction in transactions:
        # Determine the source
        if transaction.source_account.collection:
            source = CollectionResponse(
                id=transaction.source_account.collection.id,
                goal=transaction.source_account.collection.goal,
                title=transaction.source_account.collection.title,
                description=transaction.source_account.collection.description,
                start_date=transaction.source_account.collection.start_date,
                end_date=transaction.source_account.collection.end_date,
                class_id=transaction.source_account.collection.class_id,
                creator_id=transaction.source_account.collection.creator_id,
                account=AccountResponse(
                    id=transaction.source_account.id,
                    account_number=transaction.source_account.account_number,
                ),
            )
        else:
            source = UserResponse(
                id=transaction.source_account.parent.id,
                first_name=transaction.source_account.parent.first_name,
                last_name=transaction.source_account.parent.last_name,
                email=transaction.source_account.parent.email,
                created_at=transaction.source_account.parent.created_at,
                account=AccountResponse(
                    id=transaction.source_account.id,
                    account_number=transaction.source_account.account_number,
                ),
            )

        # Determine the destination
        if transaction.destination_account.collection:
            destination = CollectionResponse(
                id=transaction.destination_account.collection.id,
                goal=transaction.destination_account.collection.goal,
                title=transaction.destination_account.collection.title,
                description=transaction.destination_account.collection.description,
                start_date=transaction.destination_account.collection.start_date,
                end_date=transaction.destination_account.collection.end_date,
                class_id=transaction.destination_account.collection.class_id,
                creator_id=transaction.destination_account.collection.creator_id,
                account=AccountResponse(
                    id=transaction.destination_account.id,
                    account_number=transaction.destination_account.account_number,
                ),
            )
        else:
            destination = UserResponse(
                id=transaction.destination_account.parent.id,
                first_name=transaction.destination_account.parent.first_name,
                last_name=transaction.destination_account.parent.last_name,
                email=transaction.destination_account.parent.email,
                created_at=transaction.destination_account.parent.created_at,
                account=AccountResponse(
                    id=transaction.destination_account.id,
                    account_number=transaction.destination_account.account_number,
                ),
            )

        # Check if the transaction has an associated child
        child_response = None
        if transaction.child:
            child_response = ChildResponse(
                id=transaction.child.id,
                first_name=transaction.child.first_name,
                last_name=transaction.child.last_name,
                birth_date=transaction.child.birth_date,
            )

        # Create a transaction response
        response.append(
            FinancialTransactionResponse(
                source=source,
                destination=destination,
                amount=transaction.amount,
                description=transaction.description,
                timestamp=transaction.timestamp,
                child=child_response,
            )
        )

    return response


@app.post("/create_invite/")
def create_invite_token(
    data : CreateInviteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Check if the class exists
    class_ = db.query(Class).filter(Class.id == data.class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")

    # Ensure the current user is the treasurer of the class
    if class_.treasurer_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to create an invite for this class")

    # Generate the invite token
    token = auth.create_invite_token(data.class_id, expiration_minutes=data.expiration_minutes)
    invite_url = f"/class/?token={token}"
    return {"invite_url": invite_url, "expires_in_minutes": data.expiration_minutes}


@app.post("/process_invite")
def process_invite(
    token: str,
    request: ProcessInviteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Decode and validate the token
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=["HS256"])
        class_id = payload.get("class_id")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Invite token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid invite token")

    # Ensure the class exists
    class_ = db.query(Class).filter(Class.id == class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")

    # Validate the child
    child = db.query(Child).filter(Child.id == request.child_id, Child.parent_id == current_user.id).first()
    if not child:
        raise HTTPException(status_code=400, detail="Invalid child or child does not belong to you")

    # Associate the child with the class
    child.class_id = class_id
    db.add(child)
    db.commit()

    return {"message": "Invite successfully processed and child added to the class"}


if __name__ == "main":

    init_db()
    print("Tables created successfully!")
    scheduler.add_job(transfer_funds_on_collection_end, 'interval', minutes=1)

    # Start the scheduler
    scheduler.start()
    print("scheduler started")


@app.on_event("shutdown")
def shutdown():
    scheduler.shutdown()