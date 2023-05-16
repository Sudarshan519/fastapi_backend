from typing import Optional, Union
from fastapi import APIRouter
from fastapi import Request,Depends,responses,status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session 

from db.repository.jobs import list_jobs, search_job
from db.repository.users import create_new_user
from db.session import get_db
from db.repository.jobs import retreive_job
from schemas.users import UserCreate  #new
from webapps.users.forms import UserCreateForm
from sqlalchemy.exc import IntegrityError
from fastapi.security.utils import get_authorization_scheme_param

from webapps.jobs.forms import JobCreateForm
from schemas.jobs import JobCreate

from db.models.users import User  
from apis.v1.route_login import get_current_user_from_token
from db.repository.jobs import create_new_job

templates=Jinja2Templates(directory='templates')
router =APIRouter(include_in_schema=False)

@router.get("/")
async def home(request: Request, db: Session = Depends(get_db),msg:str = None):   #new
    jobs = list_jobs(db=db)
    print(request.cookies)
    cookie_exist=True if request.cookies.get('name') is not None else False
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "jobs": jobs,"msg":msg,"name": "Welcome "+request.cookies.get('name')} if cookie_exist else {"request": request, "jobs": jobs,"msg":msg,}  #new
    )



@router.get("/details/{id}")             #new
def job_detail(id:int,request: Request,db:Session = Depends(get_db)): 
    job = retreive_job(id=id, db=db)
    
    # print(job)
    
    cookie_exist=True if request.cookies.get('name') is not None else False
    return templates.TemplateResponse(
        "jobs/detail.html", {"request": request,"job":job,"name": "Welcome "+request.cookies.get('name')} if cookie_exist else {"request": request,  }
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
            job = JobCreate(**form.__dict__)
            job = create_new_job(job=job, db=db, owner_id=current_user.id)
            return responses.RedirectResponse(
                f"/details/{job.id}", status_code=status.HTTP_302_FOUND
            )
        except Exception as e:
            print(e)
            form.__dict__.get("errors").append(
                "You might not be logged in, In case problem persists please contact us."
            )
            return templates.TemplateResponse("jobs/create_job.html", form.__dict__)
    return templates.TemplateResponse("jobs/create_job.html", form.__dict__)


@router.get("/delete-job/")
def show_jobs_to_delete(request: Request, db: Session = Depends(get_db),user:User= Depends(get_current_user_from_token)):
    jobs = list_jobs(db=db)
    return templates.TemplateResponse(
        "jobs/show_jobs_to_delete.html", {"request": request, "jobs": jobs}
    )


@router.get("/search/")
def search(
    request: Request, db: Session = Depends(get_db), query: Optional[str] = None
):
    jobs = search_job(query, db=db)
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "jobs": jobs}
    )