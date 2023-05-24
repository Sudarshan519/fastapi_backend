import math
from fastapi import APIRouter, Query, Request
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from typing import List, Optional 
from db.models.jobs import JobApplication
from db.repository.application import ApplicationRepository
from db.repository.jobs import add_application
from schemas.base import PageResponse, ResponseSchema
from schemas.job_application import JobApplicationCreate        #new
from db.session import get_db
from db.models.jobs import Job
from db.models.users import User
from schemas.jobs import JobCreate,ShowJob
from db.repository.jobs import create_new_job,retreive_job ,list_jobs, search_job,update_job_by_id,update_application_by_id  #new #new import retrieve_job
from apis.v1.route_login import get_current_user_from_token  #new
from fastapi_pagination import LimitOffsetPage, add_pagination, paginate
router = APIRouter()


@router.post("/create-job/",response_model=ShowJob)
def create_job(job: JobCreate,db: Session = Depends(get_db),current_user:User = Depends(get_current_user_from_token)):  #new dependency here):
    job = create_new_job(job=job,db=db,owner_id=current_user.id)
    return job


#new function
@router.get("/get/{id}",response_model=ShowJob) # if we keep just "{id}" . it would stat catching all routes
def read_job(id:int,db:Session = Depends(get_db)):
    job = retreive_job(id=id,db=db)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Job with this id {id} does not exist")
    return job


@router.get("/all",response_model=LimitOffsetPage[List[ShowJob]]) #new
def read_jobs(db:Session = Depends(get_db)):
    jobs = list_jobs(db=db)
    return jobs or [] 


@router.put("/update/{id}")   #new
def update_job(id: int,job: JobCreate,db: Session = Depends(get_db)):
    current_user = 1
    message = update_job_by_id(id=id,job=job,db=db,owner_id=current_user)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Job with id {id} not found")
    return {"msg":"Successfully updated data."}

from db.repository.jobs import delete_job_by_id

@router.delete("/delete/{id}")
def delete_job(id: int,request:Request,db: Session = Depends(get_db),current_user: User = Depends(get_current_user_from_token)):
    # current_user_id = 1
    print(request.cookies)
    print(current_user)
    job=retreive_job(id=id,db=db)
    if not job:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Job with {id} does not exist")
    print(job.owner_id,current_user.id,current_user.is_superuser)
    if job.owner_id== current_user.id or current_user.is_superuser:
        delete_job_by_id(id=id,db=db,owner_id=current_user.id)
        # return {"msg":"Successfully deleted."}
        return {"detail": "Successfully deleted."} 
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not permitted!!!!")
    # message = delete_job_by_id(id=id,db=db,owner_id=current_user_id)
    # if not message:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Job with id {id} not found")
    # return {"msg":"Successfully deleted."}



@router.get("/autocomplete")
def autocomplete(term: Optional[str] = None, db: Session = Depends(get_db)):
    jobs = search_job(term, db=db)
    job_titles = []
    for job in jobs:
        job_titles.append(job.title)
    return job_titles



@router.get('/interviews',tags=['Interview'])
def all_interview(db: Session = Depends(get_db),current_user: User = Depends(get_current_user_from_token)):
    return[]

@router.post('/post-application/')
def post_application(application: JobApplicationCreate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user_from_token)):
    job=retreive_job(id= application.job_id,db=db)
    if not job: 
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Job with {application.job_id} does not exist")
    else:
        application=add_application(db=db,application=application )
        return application


@router.post('/request-interview')
def accept_application(application_id:int,application: JobApplicationCreate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user_from_token)):
    application=update_application_by_id(id=application_id,application=application,db=db)
    return application
from sqlalchemy.sql import select
@router.get('/applications/',response_model=ResponseSchema, response_model_exclude_none=True)
async def all_applications( page: int = 1,
        limit: int = 10,
        columns: str = Query(None, alias="columns"),
        sort: str = Query(None, alias="sort"),
        filter: str = Query(None, alias="filter"),db:Session=Depends(get_db),):
    # all=await ApplicationRepository.get_all()

        count = db.query(func.count(JobApplication.id)).scalar()
        print(count)
        
        # count query
        # coun/t_query = select(func.count(1)).select_from(qr)
        offset_page = page - 1
        # pagination
        pages = (db.offset(offset_page * limit).limit(limit))

        # # total record
        # total_record = (await db.execute(count_query)).scalar() or 0

        # # total page
        # total_page = math.ceil(total_record / limit)
        # all=qr
        all= db.query(JobApplication).all()
        pageres=PageResponse( page_number=page,
            page_size=limit,
            total_pages=1,
            total_record=2,
            content=all)
        return ResponseSchema(detail='Success fetching applications.',result=pageres)