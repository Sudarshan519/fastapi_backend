from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from typing import List        #new
from db.session import get_db
from db.models.jobs import Job
from schemas.jobs import JobCreate,ShowJob
from db.repository.jobs import create_new_job,retreive_job ,list_jobs  #new #new import retrieve_job

router = APIRouter()


@router.post("/create-job/",response_model=ShowJob)
def create_job(job: JobCreate,db: Session = Depends(get_db)):
    current_user = 1
    job = create_new_job(job=job,db=db,owner_id=current_user)
    return job


#new function
@router.get("/get/{id}",response_model=ShowJob) # if we keep just "{id}" . it would stat catching all routes
def read_job(id:int,db:Session = Depends(get_db)):
    job = retreive_job(id=id,db=db)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Job with this id {id} does not exist")
    return job


@router.get("/all",response_model=List[ShowJob]) #new
def read_jobs(db:Session = Depends(get_db)):
    jobs = list_jobs(db=db)
    return jobs


@router.put("/update/{id}")   #new
def update_job(id: int,job: JobCreate,db: Session = Depends(get_db)):
    current_user = 1
    message = update_job_by_id(id=id,job=job,db=db,owner_id=current_user)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Job with id {id} not found")
    return {"msg":"Successfully updated data."}