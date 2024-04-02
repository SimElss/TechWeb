from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from ..services.users import get_user_by_username, add_user, get_all_users, get_user_by_id, set_user_group, set_user_whitelist, get_user_by_email
from fastapi import HTTPException, status, Depends, Form
from fastapi.responses import JSONResponse
from ..login_manager import login_manager
from fastapi.responses import RedirectResponse
from ..schemas.users import UserSchema
from typing import Annotated
from uuid import uuid4
from ..database import database

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
        email: Annotated[str, Form()],
        password: Annotated[str, Form()],
):
    user = get_user_by_email(email)
    if user is None or user.password != password:
        error=status.HTTP_401_UNAUTHORIZED
        description=f"Erreur {error} : Mauvais mot de passe ou nom d'utilisateur."
        return RedirectResponse(url=f"/error/{description}/login", status_code=302)
    if not user.whitelist:
        error=status.HTTP_403_FORBIDDEN
        description=f"Erreur {error} : Utilisateur bloqué."
        return RedirectResponse(url=f"/error/{description}/login", status_code=302)
        
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

@user_router.post('/logout')
def logout(request: Request):
    response = templates.TemplateResponse(
        "login.html", 
        context={'request':request, 'message':"Vous avez été déconnecté !"}
    )
    response.delete_cookie(
        key=login_manager.cookie_name,
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
    user = get_user_by_email(email)
    if user is not None:
        error=status.HTTP_409_CONFLICT
        description=f"Erreur {error} : Email déjà utilisé."
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
        "group":"user",
        "whitelist": True
    })
    success_message = f"Utilisateur {username} ajouté avec succès !"
    return templates.TemplateResponse(
        "login.html",
        context={'request':request, 'message':success_message}
    )

@user_router.get('/administration')
def administration(request : Request, user: UserSchema = Depends(login_manager)):
    if user is None :
        return RedirectResponse(url="/login", status_code=302)
    if user.group != "admin":
        error=status.HTTP_403_FORBIDDEN
        description=f"Erreur {error} : Accès interdit."
        return RedirectResponse(url=f"/error/{description}/liste", status_code=302)
    if user.whitelist != True:
        error=status.HTTP_403_FORBIDDEN
        description=f"Erreur {error} : Utilisateur bloqué."
        return RedirectResponse(url=f"/error/{description}/login", status_code=302)

    users = get_all_users()
    return templates.TemplateResponse(
        "administration.html", 
        context={'request':request, 'users':users}
    )

@user_router.post('/promote/{user_id}')
def promotion(user_id: str, user: UserSchema = Depends(login_manager)):
    affected_user = get_user_by_id(user_id)
    if affected_user is None:
        error=status.HTTP_404_NOT_FOUND
        description=f"Erreur {error} : Utilisateur non trouvé."
        return RedirectResponse(url=f"/error/{description}/administration", status_code=302)
    if affected_user.group == "admin":
        set_user_group(user_id, "client")
    else:
        set_user_group(user_id, "admin")
    if user.group == "admin":
        return RedirectResponse(url="/administration", status_code=302)
    else:
        return RedirectResponse(url="/liste", status_code=302)

@user_router.post('/block/{user_id}')
def block(user_id: str, user: UserSchema = Depends(login_manager)):
    affected_user = get_user_by_id(user_id)
    if affected_user is None:
        error=status.HTTP_404_NOT_FOUND
        description=f"Erreur {error} : Utilisateur non trouvé."
        return RedirectResponse(url=f"/error/{description}/administration", status_code=302)
    if affected_user.whitelist == True:
        set_user_whitelist(user_id, False)
    else:
        set_user_whitelist(user_id, True)
    return RedirectResponse(url = "/administration", status_code=302)