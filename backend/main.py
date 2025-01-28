from datetime import timedelta
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import CRUD.child
import models
from auth import verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, decode_access_token, hash_password
from models import *
from schemas import Token, UserResponse, UserCreate, LoginRequest, ChildResponse, ChildCreate, ClassResponse, \
    ClassCreate, ChildModify, ClassModify, AddChildToClass

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
    return db_user


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
    return user


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
    return current_user


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
    return db.query(Class).join(Child).filter(Child.parent_id == current_user.id).all()


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
        raise HTTPException(400,
                            "obecny uzytkownik nie jest skarbnikiem w zadnej klasie. Tylko skarbnik moze widziec wszystkich uzytkownikow")

    return db.query(User).filter(User.id != current_user.id).all()

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

if __name__ == "main":
    # Initialize the database
    init_db()

    print("Tables created successfully!")
