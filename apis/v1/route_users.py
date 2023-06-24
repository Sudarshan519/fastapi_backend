from fastapi import APIRouter, HTTPException,status
from sqlalchemy.orm import Session
from fastapi import Depends

from schemas.users import UserCreate
from db.session import get_db
from db.repository.users import create_new_user

router = APIRouter()


@router.post("/",)
def create_user(user : UserCreate,db: Session = Depends(get_db)):
    try:
        user = create_new_user(user=user,db=db)
        return user 
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Email already registered.")

