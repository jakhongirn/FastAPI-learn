from typing import Generator, Optional
from pydantic import BaseModel
from app.db.session import SessionLocal

from fastapi import Depends, HTTPException, status
from app.core.auth import oauth2_scheme
from sqlalchemy.orm.session import Session
from app.models.user import User
from jose import jwt, JWTError
from app.core.config import settings

class TokenData(BaseModel):
    username: Optional[str] = None

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
    
def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user
        