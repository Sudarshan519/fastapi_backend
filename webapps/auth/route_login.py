
from apis.v1.route_login import login_for_access_token
from db.repository.jobs import list_jobs
from db.session import get_db
from fastapi import APIRouter, Response
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request,responses,status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from webapps.auth.forms import LoginForm


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/login/")
def login(request: Request):
            token = request.cookies.get("access_token")
            if token is not None:
                # return templates.TemplateResponse('general_pages/homepage.html', {"request": request,"name":"Welcome"+request.cookies.get('name')})
                return responses.RedirectResponse(
                f"/", status_code=status.HTTP_302_FOUND
            ) 
            # scheme, param = get_authorization_scheme_param(
            #     token
            # )  # scheme will hold "Bearer" and param will hold actual token value
            # current_user: User = get_current_user_from_token(token=param, db=db)
            print(request.cookies)
            return templates.TemplateResponse("auth/login.html", {"request": request })


@router.post("/login/")
async def login(request: Request, db: Session = Depends(get_db)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful :)")
            form.__dict__.update(name=form.username)
            jobs = list_jobs(db=db)
            form.__dict__.update(jobs=jobs)
            response = templates.TemplateResponse("/general_pages/homepage.html", form.__dict__,)
            login_for_access_token(response=response, form_data=form, db=db)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("auth/login.html", form.__dict__)
    return templates.TemplateResponse("auth/login.html", form.__dict__)

@router.get('/logout/')
async def logout(request:Request,response:Response): 
    # Also tried following two comment lines
    # response.set_cookie(key="access_token", value="", max_age=1)
    # response.delete_cookie("access_token", domain="localhost")
    response=responses.RedirectResponse(
                f"/", status_code=status.HTTP_302_FOUND
            ) 
    # response = templates.TemplateResponse("auth/login.html", {"request": request, "title": "Login"})
    response.delete_cookie("access_token")
    response.delete_cookie("name")
    return response