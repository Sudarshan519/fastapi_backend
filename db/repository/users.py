from fastapi import HTTPException,status
from sqlalchemy.orm import Session

from schemas.users import UserCreate
from db.models.users import User
from core.hashing import Hasher


def create_new_user(user:UserCreate,db:Session):
    try:
        user = User(username=user.username,
            email = user.email,
            hashed_password=Hasher.get_password_hash(user.password),
            is_active=True,
            is_superuser=False
            )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Email already registered.")
    
def get_user_by_email(email:str,db:Session):             #new
    user = db.query(User).filter(User.email == email).first()
    return user