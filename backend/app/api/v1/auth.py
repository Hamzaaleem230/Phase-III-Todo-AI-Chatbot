from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from uuid import UUID
from typing import Optional
from app.schemas.user import UserCreate, AuthResponse
from app.models.user import User
from app.dependencies.db import get_db
from app.core.config import settings
JWT_SECRET_KEY = settings.JWT_SECRET_KEY
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

auth_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=1440)  # 24 hours
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, str(JWT_SECRET_KEY), algorithm="HS256")
    return encoded_jwt

@auth_router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def signup_user(user_create: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.exec(select(User).where(User.email == user_create.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(user_create.password)
    user = User(email=user_create.email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(data={"user_id": str(user.id), "email": user.email})
    return AuthResponse(access_token=access_token, user_id=user.id, email=user.email)

@auth_router.post("/login", response_model=AuthResponse)
def login_user(user_login: UserCreate, db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.email == user_login.email)).first()
    if not user or not pwd_context.verify(user_login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"user_id": str(user.id), "email": user.email})
    return AuthResponse(access_token=access_token, user_id=user.id, email=user.email)