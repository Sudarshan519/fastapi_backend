from functools import wraps
from fastapi import HTTPException, Request,status
from fastapi.templating import Jinja2Templates

from db.repository.jobs import list_jobs
templates=Jinja2Templates(directory='templates')

def auth_required(handler):
    @wraps(handler)
    async def wrapper( *args, **kwargs):
        # do_something_with_request_object(request)
        request=(kwargs.get('request'))
        db=(kwargs.get('db'))
        token=request.cookies.get("access_token")
        if token is None:
            jobs = list_jobs(db=db)
            return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "jobs": jobs,"msg":"Not authenticated. Please login to continue..."},#"name": "Welcome "+request.cookies.get('name')} if cookie_exist else {"request": request, "jobs": jobs,"msg":msg,}  #new
    )
        return   handler(*args, **kwargs)
    return wrapper

def requires_employee(handler):
    @wraps(handler)
    async def wrapper(*args,**kwargs):
        user=(kwargs.get('current_user'))
        db=(kwargs.get('db'))
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not permitted!!!!")
        else:
            if user.is_employer is False:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not permitted!!!!")
            
        return wrapper
        
        

 