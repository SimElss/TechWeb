from typing import Annotated
from uuid import uuid4
from fastapi import APIRouter, status, Depends
from ..login_manager import login_manager
from ..services.books import get_all_books, delete_book, modify_book, save_books, get_number_books
from ..schemas.users import UserSchema
from fastapi import APIRouter, status, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def home():
    return RedirectResponse(url="/login", status_code=302)

@router.get("/error/{description}")
def error(request : Request, description: str):
    return templates.TemplateResponse(
        "error.html", 
        context={'request':request, 'description': description}
    )

@router.get("/liste")
def list_books(request : Request, user: UserSchema = Depends(login_manager.optional)):
    nb = get_number_books()
    books = get_all_books()
    return templates.TemplateResponse(
        "books.html", 
        context={'request':request,'books': books, 'Nombre':nb, 'current_user': user}
    )

@router.post("/liste")
def delete(id: Annotated[str, Form()]):
    response = delete_book(id)
    if response is None:
        error = status.HTTP_404_NOT_FOUND
        description = f"Error {error} : pas de livre trouvé avec cet ID"
        return RedirectResponse(url=f"/error/{description}", status_code=302)
    return RedirectResponse(url="/liste", status_code=302)

@router.get("/modify")
def modify(request : Request):
    nb = get_number_books()
    books = get_all_books()
    return templates.TemplateResponse(
        "modify.html", 
        context={'request': request, 'books':books, 'Nombre':nb}
    )

@router.post("/modify")
def modify(id: Annotated[str, Form()], name: Annotated[str, Form()], Author: Annotated[str, Form()], Editor: Annotated[str, Form()]):
    response = modify_book(id, {
        "id" : id,
        "name" : name,
        "Author" : Author,
        "Editor": Editor,
    })
    if response is None:
        error = status.HTTP_404_NOT_FOUND
        description = f"Erreur {error} : Informations invalides données."
        return RedirectResponse(url=f"/error/{description}", status_code=302)
    elif response == 1:
        error = status.HTTP_404_NOT_FOUND
        description = f"Erreur {error} : pas de livre trouvé avec cet ID"
        return RedirectResponse(url=f"/error/{description}", status_code=302)
    return RedirectResponse(url="/liste", status_code=302)

@router.get("/save")
def save(request : Request):
    nb = get_number_books()
    return templates.TemplateResponse(
        "save_book.html", 
        context={'request': request, 'Nombre':nb}
    )

@router.post("/save")
def save(name: Annotated[str, Form()], Author: Annotated[str, Form()], Editor: Annotated[str, Form()]):
    print(0)
    new_book = save_books({
        "id" : str(uuid4()),
        "name" : name,
        "Author" : Author,
        "Editor": Editor,
        })
    if new_book is None:
        error = status.HTTP_404_NOT_FOUND
        description = f"Erreur {error} : Informations invalides données."
        return RedirectResponse(url=f"/error?description={description}", status_code=302)
    return RedirectResponse(url="/liste", status_code=302)