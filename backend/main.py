import uuid
from datetime import timedelta
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import or_
from sqlalchemy.orm import Session

import CRUD.child
import models
from auth import verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, decode_access_token, hash_password
from models import *
from schemas import Token, UserResponse, UserCreate, LoginRequest, ChildResponse, ChildCreate, ClassResponse, \
    ClassCreate, ChildModify, ClassModify, AddChildToClass, CollectionResponse, CollectionCreate, AccountResponse

app = FastAPI(debug=True)

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
        title=collection.title,
        description=collection.description,
        start_date=collection.start_date,
        end_date=collection.end_date,
        class_id=collection.class_id,
        creator_id=collection.creator_id,
        account=AccountResponse.from_orm(account)  # Return AccountResponse instead of plain account
    )

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


if __name__ == "main":
    # Initialize the database
    init_db()

    print("Tables created successfully!")
