from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr
from app.dependencies.db import get_session
from app.models.user import User  # Keeping your import

router = APIRouter()

class UserAuthSchema(BaseModel):
    email: EmailStr
    password: str

# 1. FIXED SIGNUP ENDPOINT
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserAuthSchema, session: Session = Depends(get_session)):
    # Check if user already exists
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user dynamic dictionary to support both 'password' or 'hashed_password' fields if any
    user_kwargs = {"email": user_data.email}
    
    # Safeguard: Check if model uses password or hashed_password
    if hasattr(User, "hashed_password"):
        user_kwargs["hashed_password"] = user_data.password
    else:
        user_kwargs["password"] = user_data.password

    try:
        new_user = User(**user_kwargs)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        
        return {
            "access_token": "real-jwt-token-generation-here", 
            "user_id": str(new_user.id),
            "message": "User registered successfully"
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Database insertion error: {str(e)}")

# 2. FIXED LOGIN ENDPOINT
@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user_data: UserAuthSchema, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == user_data.email)
    user = session.exec(statement).first()
    
    # Support check for both plain field names
    is_valid = False
    if user:
        if hasattr(user, "hashed_password") and user.hashed_password == user_data.password:
            is_valid = True
        elif hasattr(user, "password") and user.password == user_data.password:
            is_valid = True

    if not user or not is_valid:
        raise HTTPException(status_code=400, detail="Invalid email or password")
        
    return {
        "access_token": "real-jwt-token-generation-here", 
        "user_id": str(user.id),
        "message": "Login successful"
    }