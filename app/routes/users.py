from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from ..services.users import add_user, get_all_users, get_user_by_id, set_user_group, set_user_whitelist, get_user_by_email, change_user_password, modifify_user_profile
from ..services.beers import get_beer_by_user, get_number_beers_of_user, get_price_cart
from fastapi import status, Depends, Form
from ..login_manager import login_manager
from fastapi.responses import RedirectResponse
from ..schemas.users import UserSchema
from typing import Annotated
from uuid import uuid4
import hashlib

# Define APIRouter instance for user routes
user_router = APIRouter()

# Setup Jinja2Templates for HTML rendering
templates = Jinja2Templates(directory="templates")

# Route for user login page
@user_router.get("/login")
def login(request: Request, message: str = "None"):
    # Render the login page
    return templates.TemplateResponse(
        "login.html", 
        context={'request': request, 'message': message}
    )

# Route for handling user login
@user_router.post("/login")
def login_route(
        email: Annotated[str, Form()],
        password: Annotated[str, Form()],
):
    # Check if user exists and password matches
    user = get_user_by_email(email)
    # Hash the password and verify if the hash corresponds to the hashed password stored in the database
    encoded_password = password.encode()
    hashed_password = hashlib.sha3_256(encoded_password).hexdigest()
    if user is None or user.password != hashed_password:
        error = status.HTTP_401_UNAUTHORIZED
        description = f"Error {error}: Incorrect username or password."
        return RedirectResponse(url=f"/error/{description}/login", status_code=302)
    
    # Check if user is whitelisted
    if not user.whitelist:
        error = status.HTTP_403_FORBIDDEN
        description = f"Error {error}: User blocked."
        return RedirectResponse(url=f"/error/{description}/login", status_code=302)
        
    # Create access token and set cookie
    access_token = login_manager.create_access_token(data={'sub': user.id})
    response = RedirectResponse(url="/liste", status_code=302)
    response.set_cookie(key=login_manager.cookie_name, value=access_token, httponly=True)
    return response

# Route for user logout
@user_router.post('/logout')
def logout(request: Request):
    # Render the logout page and delete the cookie
    response = templates.TemplateResponse(
        "login.html", 
        context={'request': request, 'message': "You have been logged out!"}
    )
    response.delete_cookie(key=login_manager.cookie_name, httponly=True)
    return response

# Route for user registration page
@user_router.get('/register')
def register(request: Request):
    # Render the registration page
    return templates.TemplateResponse(
        "register.html", 
        context={'request': request}
    )

# Route for handling user registration
@user_router.post('/register')
def register_route(request: Request, username: Annotated[str, Form()], name: Annotated[str, Form()], surname: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()], password_confirm: Annotated[str, Form()],
):
    # Check if user with given email already exists
    user = get_user_by_email(email)
    if user is not None:
        error = status.HTTP_409_CONFLICT
        description = f"Error {error}: Email already in use."
        return RedirectResponse(url=f"/error/{description}/register", status_code=302)
    
    # Check if passwords match
    if password != password_confirm:
        error = status.HTTP_400_BAD_REQUEST
        description = f"Error {error}: Passwords do not match."
        return RedirectResponse(url=f"/error/{description}/register", status_code=302)
    
    # Add user to database
    new_user = {
        "id": str(uuid4()),
        "username": username,
        "name": name,
        "surname": surname,
        "password": password,
        "email": email,
        "group": "client",
        "whitelist": True
    }
    new_user = UserSchema.model_validate(new_user)
    # If an exception is raised it will be caught by the app event listener (see app.py)
    add_user(new_user)
    success_message = f"User {username} successfully added!"
    return templates.TemplateResponse(
        "login.html",
        context={'request': request, 'message': success_message}
    )

# Route for password reset page
@user_router.get('/new_mdp')
def new_mdp(request: Request, user: UserSchema = Depends(login_manager.optional)):
    required = user is not None
    return templates.TemplateResponse(
        "new_mdp.html", 
        context={'request': request, 'current_user': user, 'required': required}
    )

# Route for handling password reset
@user_router.post('/new_mdp')
def new_mdp_route(request: Request, old_pwd: Annotated[str, Form()], new_pwd: Annotated[str, Form()], new_pwd_confirm: Annotated[str, Form()], user: UserSchema = Depends(login_manager.optional), email: Annotated[str, Form()] = None,
):
    if user is None:
        target_user = get_user_by_email(email)
        # Check if user exists
        if target_user is None:
            error = status.HTTP_404_NOT_FOUND
            description = f"Error {error}: User not found."
            return RedirectResponse(url=f"/error/{description}/new_mdp", status_code=302)
    else:
        target_user = user

    # Check if old password is correct
    encoded_password = old_pwd.encode()
    old_hashed_password = hashlib.sha3_256(encoded_password).hexdigest()
    if target_user.password != old_hashed_password:
        error = status.HTTP_400_BAD_REQUEST
        description = f"Error {error}: Old password is incorrect."
        return RedirectResponse(url=f"/error/{description}/new_mdp", status_code=302)
    
    # Check if new passwords match
    if new_pwd != new_pwd_confirm:
        error = status.HTTP_400_BAD_REQUEST
        description = f"Error {error}: Passwords do not match."
        return RedirectResponse(url=f"/error/{description}/new_mdp", status_code=302)

    # Update password
    change_user_password(target_user.id, new_pwd)

    # Redirect to login page
    success_message = f"Password successfully updated!"
    return templates.TemplateResponse(
        "login.html",
        context={'request': request, 'message': success_message}
    )

# Route for administration page
@user_router.get('/administration')
def administration(request: Request, user: UserSchema = Depends(login_manager)):
    # Check if user is connected
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    # Check if user is admin
    if user.group != "admin":
        error = status.HTTP_403_FORBIDDEN
        description = f"Error {error}: Access forbidden."
        return RedirectResponse(url=f"/error/{description}/liste", status_code=302)
    # Check if user is not blocked
    if not user.whitelist:
        error = status.HTTP_403_FORBIDDEN
        description = f"Error {error}: User blocked."
        return RedirectResponse(url=f"/error/{description}/login", status_code=302)
    
    # Get all users for administration
    users = get_all_users()
    return templates.TemplateResponse(
        "administration.html", 
        context={'request': request, 'users': users}
    )

# Route for promoting/demoting users
@user_router.post('/promote/{user_id}')
def promotion(user_id: str, user: UserSchema = Depends(login_manager)):
    # Get the user to promote/demote
    affected_user = get_user_by_id(user_id)

    # Verify if the user ID is valid
    if affected_user is None:
        error = status.HTTP_404_NOT_FOUND
        description = f"Error {error}: User not found."
        return RedirectResponse(url=f"/error/{description}/administration", status_code=302)
    
    # Change the user group
    if affected_user.group == "admin":
        set_user_group(user_id, "client")
    else:
        set_user_group(user_id, "admin")
    
    # Redirect based on the user group
    if user.group == "admin":
        return RedirectResponse(url="/administration", status_code=302)
    else:
        return RedirectResponse(url="/liste", status_code=302)

# Route for blocking/unblocking users
@user_router.post('/block/{user_id}')
def block(user_id: str):
    affected_user = get_user_by_id(user_id)
    # Verify if the user ID is valid
    if affected_user is None:
        error = status.HTTP_404_NOT_FOUND
        description = f"Error {error}: User not found."
        return RedirectResponse(url=f"/error/{description}/administration", status_code=302)
    
    # Change the user's whitelist status
    set_user_whitelist(user_id, not affected_user.whitelist)
    return RedirectResponse(url="/administration", status_code=302)

# Route for user profile page
@user_router.get('/profile')
def profile(request: Request, user: UserSchema = Depends(login_manager)):
    nbUser = get_number_beers_of_user(user.id)
    # Check if user is connected

    if user is None:
        return RedirectResponse(url="/liste", status_code=302)
    # Check if user is not blocked
    if not user.whitelist:
        error = status.HTTP_403_FORBIDDEN
        description = f"Error {error}: User blocked."
        return RedirectResponse(url=f"/error/{description}/login", status_code=302)
    
    profile = True
    return templates.TemplateResponse(
        "profile.html", 
        context={'request': request, 'current_user': user, 'in_profile': profile, 'nb': nbUser}
    )

# Route for the cart page
@user_router.get('/panier')
def panier(request: Request, user: UserSchema = Depends(login_manager)):
    # Check if user is connected
    if user is None:
        return RedirectResponse(url="/liste", status_code=302)
    # Check if user is not blocked
    if not user.whitelist:
        error = status.HTTP_403_FORBIDDEN
        description = f"Error {error}: User blocked."
        return RedirectResponse(url=f"/error/{description}/login", status_code=302)
    
    profile = True
    beers = get_beer_by_user(user.id)
    nb = get_number_beers_of_user(user.id)
    cart = get_price_cart(user.id)

    return templates.TemplateResponse(
        "panier.html", 
        context={'request': request, 'current_user': user, 'cart': cart, 'beers': beers, 'in_profile': profile, 'nb': nb}
    )

# Route for modifying profile (POST request)
@user_router.post('/profile')
def modify_profile_route(request: Request, name: Annotated[str, Form()], surname: Annotated[str, Form()], username: Annotated[str, Form()], user: UserSchema = Depends(login_manager),
):
    # Check if user is connected
    if user is None:
        return RedirectResponse(url="/liste", status_code=302)
    # Check if user is not blocked
    if not user.whitelist:
        error = status.HTTP_403_FORBIDDEN
        description = f"Error {error}: User blocked."
        return RedirectResponse(url=f"/error/{description}/login", status_code=302)
    
    new_user = modifify_user_profile(user.id, name, surname, username)
    if new_user is None:
        error = status.HTTP_400_BAD_REQUEST
        description = f"Error {error}: Invalid information provided."
        return RedirectResponse(url=f"/error/{description}/profile", status_code=302)
    
    return RedirectResponse(url="/profile", status_code=302)
