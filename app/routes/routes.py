from typing import Annotated, Optional
from uuid import uuid4
from fastapi import APIRouter, status, Depends
from ..login_manager import login_manager
from ..services.beers import get_all_beers, delete_beer, modify_beer, save_beers, get_number_beers, get_beer_by_id, add_owner, get_number_beers_client
from ..services.users import get_beer_owners, get_user_by_beer
from ..schemas.users import UserSchema
from ..schemas.beers import Beer
from fastapi import APIRouter, status, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

# Create APIRouter instance for beer-related routes
router = APIRouter()

# Setup Jinja2Templates for HTML rendering
templates = Jinja2Templates(directory="templates")

# Route for redirecting to login page on root access
@router.get("/")
def home():
    return RedirectResponse(url="/login", status_code=302)

# Temporary route to handle user session management
@router.get("/tmp")
def tmp(request: Request, user: UserSchema = Depends(login_manager.optional)):
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    else:
        return RedirectResponse(url="/liste", status_code=302)

# Route to display error message
@router.get("/error/{description}/{url}")
def error(request: Request, description: str, url: str):
    return templates.TemplateResponse(
        "error.html", 
        context={'request': request, 'description': description, 'url': url}
    )

# Route to display list of beers
@router.get("/liste")
def list_beers(request: Request, user: UserSchema = Depends(login_manager.optional)):
    beers = get_all_beers()
    nb = get_number_beers()
    return templates.TemplateResponse(
        "beers.html", 
        context={'request': request,'Nombre': nb, 'current_user': user, 'beers': beers}
    )

# Route to delete a beer
@router.post("/delete/{id}")
def delete(id: str):
    response = delete_beer(id)
    if response is None:
        error = status.HTTP_404_NOT_FOUND
        description = f"Error {error} : No beer found with this ID"
        return RedirectResponse(url=f"/error/{description}/liste", status_code=302)
    return RedirectResponse(url="/liste", status_code=302)

# Route to modify a beer
@router.get("/modify/{id}")
def modify(request: Request, id: str, user: UserSchema = Depends(login_manager.optional)):
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    #check if user is admin -> only admin can modify beer
    owner = get_user_by_beer(id)
    if owner is None:
        error = status.HTTP_404_NOT_FOUND
        description = f"Error {error}: No beer found with this ID"
        return RedirectResponse(url=f"/error/{description}/liste", status_code=302)
    if user.group != "admin" and owner.id != user.id:
        error = status.HTTP_403_FORBIDDEN
        description = f"Error {error}: Access forbidden."
        return RedirectResponse(url=f"/error/{description}/liste", status_code=302)
    beer = get_beer_by_id(id)
    nb = get_number_beers()
    return templates.TemplateResponse(
        "modify.html", 
        context={'request': request, 'Nombre': nb, 'beer': beer}
    )

# Route to modify a beer (POST request)
@router.post("/modify/{id}")
def modify(id: str, name: Annotated[str, Form()], Author: Annotated[str, Form()], price:Annotated[float, Form()], Editor: Annotated[Optional[str], Form()] = None):
    response = modify_beer(id, None, name, Author, Editor, price)
    #if None user had just enter spaces in one of the field (not optional one)
    if response is None:
        error = status.HTTP_400_BAD_REQUEST
        description = f"Error {error}: Invalid information provided."
        return RedirectResponse(url=f"/error/{description}/modify", status_code=302)
    #Check if the id is valid
    if response == 1:
        error = status.HTTP_400_BAD_REQUEST
        description = f"Error {error}: No beer found with this ID"
        return RedirectResponse(url=f"/error/{description}/modify", status_code=302)
    return RedirectResponse(url="/liste", status_code=302)

# Route to add a new beer
@router.get("/save")
def save(request: Request, user: UserSchema = Depends(login_manager.optional)):
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    # check if user is admin -> only admin can modify beer
    return templates.TemplateResponse(
        "save_beers.html", 
        context={'request': request, 'current_user': user}
    )

# Route to add a new beer (POST request)
@router.post("/save")
def save(name: Annotated[str, Form()], Author: Annotated[str, Form()],price:Annotated[float, Form()], Editor: Annotated[Optional[str], Form()] = None, user = Depends(login_manager.optional)):
    new_beer = {
        "id" : str(uuid4()),
        "name" : name,
        "Author" : Author,
        "Editor": Editor,
        "price": price,
        "bought": False,
        "new_owner_id": None
        }
    new_beer = Beer.model_validate(new_beer)
    saved_beers = save_beers(new_beer, user.id)
    #if None user had just enter spaces in one of the field (not optional one)
    if saved_beers is None:
        error = status.HTTP_404_NOT_FOUND
        description = f"Error {error}: Invalid information provided."
        return RedirectResponse(url=f"/error/{description}/save", status_code=302)
    return RedirectResponse(url="/profile", status_code=302)

# Route to but the beer (POST request)
@router.post("/buy/{id}")
def buy(id: str, user = Depends(login_manager.optional)):
    #We verify that the user is connected
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    #We verify that the beer exists
    beer = get_beer_by_id(id)
    if beer is None:
        error = status.HTTP_404_NOT_FOUND
        description = f"Error {error}: No beer found with this ID"
        return RedirectResponse(url=f"/error/{description}/liste", status_code=302)
    #change the status of the beer to bought
    modify_beer(id, True)
    #add the user as owner of the beer
    add_owner(id, user.id)
    return RedirectResponse(url="/liste", status_code=302)