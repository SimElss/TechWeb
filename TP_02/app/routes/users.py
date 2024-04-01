from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from ..services.users import get_user_by_username, add_user
from fastapi import HTTPException, status, Depends, Form
from fastapi.responses import JSONResponse
from ..login_manager import login_manager
from fastapi.responses import RedirectResponse
from ..schemas.users import UserSchema
from typing import Annotated
from uuid import uuid4

user_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@user_router.get("/login")
def login(request : Request, message: str = "None"):
    return templates.TemplateResponse(
        "login.html", 
        context={'request':request, 'message':message}
    )

@user_router.post("/login")
def login_route(
        username: Annotated[str, Form()],
        password: Annotated[str, Form()],
):
    user = get_user_by_username(username)
    if user is None or user.password != password:
        error=status.HTTP_401_UNAUTHORIZED
        description=f"Erreur {error} : Mauvais mot de passe ou nom d'utilisateur."
        return RedirectResponse(url=f"/error/{description}", status_code=302)
        
    access_token = login_manager.create_access_token(
        data={'sub': user.id}
    )
    
    response = RedirectResponse(url="/liste", status_code=302)
    response.set_cookie(
        key=login_manager.cookie_name,
        value=access_token,
        httponly=True
    )

    return response

@user_router.get('/register')
def register(request : Request):
    return templates.TemplateResponse(
        "register.html", 
        context={'request':request}
    )

@user_router.post('/register')
def register_route(
    request : Request,
    username: Annotated[str, Form()],
    name: Annotated[str, Form()],
    surname: Annotated[str, Form()],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    password_confirm: Annotated[str, Form()],
):
    user = get_user_by_username(username)
    if user is not None:
        error=status.HTTP_409_CONFLICT
        description=f"Erreur {error} : Nom d'utilisateur déjà utilisé."
        return RedirectResponse(url=f"/error/{description}", status_code=302)
    if password != password_confirm:
        error=status.HTTP_400_BAD_REQUEST
        description=f"Erreur {error} : Les mots de passe ne correspondent pas."
        return RedirectResponse(url=f"/error/{description}", status_code=302)
    add_user({
        "id": str(uuid4()),
        "username": username,
        "name": name,
        "surname": surname,
        "password": password,
        "email": email,
        "group":"user"
    })
    success_message = f"Utilisateur {username} ajouté avec succès"
    return templates.TemplateResponse(
        "login.html",
        context={'request':request, 'message':success_message}
    )

@user_router.get('/administration')
def administration(request : Request):
    return templates.TemplateResponse(
        "administration.html", 
        context={'request':request}
    )