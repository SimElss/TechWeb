from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from ..services.users import get_user_by_username
from fastapi import HTTPException, status, Depends, Form
from fastapi.responses import JSONResponse
from ..login_manager import login_manager
from fastapi.responses import RedirectResponse
from ..schemas.users import UserSchema
from typing import Annotated

user_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@user_router.get("/login")
def login(request : Request):
    return templates.TemplateResponse(
        "login.html", 
        context={'request':request}
    )

@user_router.post("/login")
def login_route(
        username: Annotated[str, Form()],
        password: Annotated[str, Form()],
):
    user = get_user_by_username(username)
    if user is None or user.password != password:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bad credentials."
        )
    access_token = login_manager.create_access_token(
        data={'sub': user.id}
    )
    
    response = JSONResponse({"status": "success"})
    response.set_cookie(
        key=login_manager.cookie_name,
        value=access_token,
        httponly=True
    )

    return RedirectResponse(url="/liste", status_code=302), response

@user_router.post('/logout')
def logout_route():
    response = JSONResponse({'status': 'success'})
    response.delete_cookie(
        key=login_manager.cookie_name,
        httponly=True
    )
    return response


@user_router.get("/me")
def current_user_route(
    user: UserSchema = Depends(login_manager),
):
    return user
