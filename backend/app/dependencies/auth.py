from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Optional
from uuid import UUID

from app.core.config import settings
JWT_SECRET_KEY = settings.JWT_SECRET_KEY

# Better Auth frontend se token bhejta hai, hum yahan use verify karte hain
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_jwt_token(token: str = Depends(oauth2_scheme)) -> UUID:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # JWT decode karne ke liye HS256 algorithm aur shared secret use hota hai
        payload = jwt.decode(token, str(JWT_SECRET_KEY), algorithms=["HS256"])
        
        # Better Auth mein user_id 'sub' ya 'user_id' dono mein ho sakti hai
        user_id: str = payload.get("sub") or payload.get("user_id")
        
        if user_id is None:
            raise credentials_exception
            
        return UUID(user_id)
    except (JWTError, ValueError):
        # Agar token expire ho ya signature galat ho toh error aayega
        raise credentials_exception

def get_current_user_id(user_id: UUID = Depends(verify_jwt_token)) -> UUID:
    # Ye function routes mein current authenticated user ki ID provide karta hai
    return user_id