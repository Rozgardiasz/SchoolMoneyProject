from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import timedelta, datetime
from typing import Optional

SECRET_KEY = "your-secret-key"  # Change this to a more secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 6*60  # Token expires in 6 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Create JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default expiry time of 15 mins
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Decode JWT token
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None




def create_invite_token(class_id: int, expiration_minutes: int = 60):
    payload = {
        "class_id": class_id,
        "exp": datetime.utcnow() + timedelta(minutes=expiration_minutes),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
