from typing import Optional, Union
from fastapi import APIRouter
from fastapi import Request,Depends,responses,status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from webapps.jobs.forms import InterviewCreateForm
from db.repository.jobs import all_applications
from db.repository.jobs import delete_job_by_id 

from db.repository.jobs import list_jobs, search_job,filter_jobs ,all_interviews,add_interviews
from db.repository.users import create_new_user
from db.session import get_db
from db.repository.jobs import retreive_job
from schemas.users import UserCreate  #new
from webapps.users.forms import UserCreateForm
from sqlalchemy.exc import IntegrityError
from fastapi.security.utils import get_authorization_scheme_param

from webapps.jobs.forms import JobCreateForm
from schemas.jobs import JobCreate
from schemas.interviews import InterviewCreate

from db.models.users import User  
from apis.v1.route_login import get_current_user_from_token
from db.repository.jobs import create_new_job
from webapps.utils import auth_required

templates=Jinja2Templates(directory='templates')
router =APIRouter(include_in_schema=False)

@router.get("/")
# @auth_required
async def home(request: Request, db: Session = Depends(get_db),msg:str = None):   #new
    jobs = list_jobs(db=db)
    cookie_exist=True if request.cookies.get('name') is not None else False
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "jobs": jobs,"msg":msg,"name": "Welcome "+request.cookies.get('name')} if cookie_exist else {"request": request, "jobs": jobs,"msg":msg,}  #new
    )



@router.get("/details/{id}")   
@auth_required          #new
def job_detail(id:int,request: Request,db:Session = Depends(get_db)): 
    job = retreive_job(id=id, db=db)
    
    # print(job)
    
    cookie_exist=True if request.cookies.get('name') is not None else False
    return templates.TemplateResponse(
    "jobs/detail.html", {"request": request,"job":job,"name": "Welcome "+request.cookies.get('name')} if cookie_exist else {"request": request, "job":job }
    )



@router.get("/post-a-job/")       #new 
def create_job(request: Request, db: Session = Depends(get_db)):
    print(request.cookies)
    tok=request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(
                tok
            ) 
    print(param)
    user=get_current_user_from_token(token=param,db=db)
    return templates.TemplateResponse("jobs/create_job.html", {"request": request})


@router.post("/post-a-job/")    #new
async def create_job(request: Request, db: Session = Depends(get_db) ):
    form = JobCreateForm(request)
 
    # print( request.cookies.get("access_token"))
    await form.load_data()
    if form.is_valid():
        try:
            token = request.cookies.get("access_token")
            print(token)
            scheme, param = get_authorization_scheme_param(
                token
            )  # scheme will hold "Bearer" and param will hold actual token value
            print(token)
            current_user: User = get_current_user_from_token(token=param, db=db)
            # print(current_user)
            job = InterviewCreate(**form.__dict__)
            job = create_new_job(job=job, db=db, owner_id=current_user.id)
            return responses.RedirectResponse(
                f"/details/{job.id}", status_code=status.HTTP_302_FOUND
            )
        except Exception as e:
            form.__dict__.get("errors").append(
                "You might not be logged in, In case problem persists please contact us."
            )
            return templates.TemplateResponse("jobs/create_job.html", form.__dict__)
    return templates.TemplateResponse("jobs/create_job.html", form.__dict__)


@router.get("/delete-job/")
def show_jobs_to_delete(request: Request, db: Session = Depends(get_db)):
    # jobs = list_jobs(db=db)
    cookie_exist=True if request.cookies.get('name') is not None else False
    token = request.cookies.get("access_token")
             
    scheme, param = get_authorization_scheme_param(
                token
            )  # scheme will hold "Bearer" and param will hold actual token value
    print(token)
    current_user: User = get_current_user_from_token(token=param, db=db)
    jobs=filter_jobs(db=db,ownerId=current_user.id)

    dict={"request": request, "jobs": jobs}

    dict['name']= request.cookies.get('name') if cookie_exist else dict
    return templates.TemplateResponse(
        "jobs/show_jobs_to_delete.html",dict
    )
@router.post("/delete-job/{id}")
def delete_jobs(id:int,request:Request,db:Session=Depends(get_db)):
    delete_job_by_id(id=id )
    return  

@router.get("/search/")
def search(
    request: Request, db: Session = Depends(get_db), query: Optional[str] = None
):
    jobs = search_job(query, db=db)
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "jobs": jobs}
    )


@router.get("/applications/")
@auth_required   
def allAplication(request: Request, db: Session = Depends(get_db), query: Optional[str] = None):
    applications=all_applications(db=db)
    return templates.TemplateResponse(
        "jobs/applications.html", {"request": request, "applications": applications}
    )


@router.get("/interviews/")
@auth_required   
def allAplication(request: Request, db: Session = Depends(get_db), query: Optional[str] = None):
    applications=all_interviews(db=db)
    return templates.TemplateResponse(
        "jobs/interview.html", {"request": request, "applications": applications}
    )

@router.get('/request-interview/{id}')
@auth_required
def request_interview(request: Request, db: Session = Depends(get_db), query: Optional[str] = None):
    applications=all_interviews(db=db)
    return templates.TemplateResponse(
        "jobs/request_interview.html", {"request": request, "applications": applications}
    )


@router.post('/request-interview/{id}')
# @auth_required
async def schedule_interview(id:int, request: Request, db: Session = Depends(get_db), query: Optional[str] = None): 
    form=InterviewCreateForm(request)
    await form.load_data()

    if form.is_valid():
        try:
            print(form.__dict__)
            interview = InterviewCreate(**form.__dict__)
            print(interview)
    #         # job = create_new_job(job=job, db=db, owner_id=current_user.id)
        except Exception as e:
            print(e)
            form.__dict__.get("errors").append(
                "You might not be logged in, In case problem persists please contact us."
            )
            print(form.__dict__)
            return templates.TemplateResponse("jobs/request_interview.html", form.__dict__)
 
    return templates.TemplateResponse("jobs/request_interview.html", form.__dict__)