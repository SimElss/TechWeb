from typing import Annotated, Optional
from uuid import uuid4
from fastapi import APIRouter, status, Depends
from ..login_manager import login_manager
from ..services.books import get_all_books, delete_book, modify_book, save_books, get_number_books, get_book_by_id
from ..schemas.users import UserSchema
from fastapi import APIRouter, status, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

# Create APIRouter instance for book-related routes
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

# Route to display list of books
@router.get("/liste")
def list_books(request: Request, user: UserSchema = Depends(login_manager.optional)):
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    nb = get_number_books()
    books = get_all_books()
    return templates.TemplateResponse(
        "books.html", 
        context={'request': request,'books': books, 'Nombre': nb, 'current_user': user}
    )

# Route to delete a book
@router.post("/delete/{id}")
def delete(id: str):
    response = delete_book(id)
    if response is None:
        error = status.HTTP_404_NOT_FOUND
        description = f"Error {error} : No book found with this ID"
        return RedirectResponse(url=f"/error/{description}/liste", status_code=302)
    return RedirectResponse(url="/liste", status_code=302)

# Route to modify a book
@router.get("/modify/{id}")
def modify(request: Request, id: str, user: UserSchema = Depends(login_manager.optional)):
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    if user.group != "admin":
        error = status.HTTP_403_FORBIDDEN
        description = f"Error {error}: Access forbidden."
        return RedirectResponse(url=f"/error/{description}/liste", status_code=302)
    book = get_book_by_id(id)
    nb = get_number_books()
    books = get_all_books()
    return templates.TemplateResponse(
        "modify.html", 
        context={'request': request, 'books': books, 'Nombre': nb, 'book': book}
    )

# Route to modify a book (POST request)
@router.post("/modify/{id}")
def modify(id: str, name: Annotated[str, Form()], Author: Annotated[str, Form()], Editor: Annotated[Optional[str], Form()] = None):
    if Editor == None:
        Editor = ""
    response = modify_book(id, name, Author, Editor)
    if response is None:
        error = status.HTTP_404_NOT_FOUND
        description = f"Error {error}: Invalid information provided."
        return RedirectResponse(url=f"/error/{description}/modify", status_code=302)
    if response == 1:
        error = status.HTTP_404_NOT_FOUND
        description = f"Error {error}: No book found with this ID"
        return RedirectResponse(url=f"/error/{description}/modify", status_code=302)
    return RedirectResponse(url="/liste", status_code=302)

# Route to add a new book
@router.get("/save")
def save(request: Request, user: UserSchema = Depends(login_manager.optional)):
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    if user.group != "admin":
        error = status.HTTP_403_FORBIDDEN
        description = f"Error {error}: Access forbidden."
        return RedirectResponse(url=f"/error/{description}/liste", status_code=302)
    nb = get_number_books()
    return templates.TemplateResponse(
        "save_book.html", 
        context={'request': request, 'Nombre': nb, 'current_user': user}
    )

# Route to add a new book (POST request)
@router.post("/save")
def save(name: Annotated[str, Form()], Author: Annotated[str, Form()], Editor: Annotated[Optional[str], Form()] = None):
    if Editor == None:
        Editor = ""
    new_book = save_books({
        "id" : str(uuid4()),
        "name" : name,
        "Author" : Author,
        "Editor": Editor,
        })
    if new_book is None:
        error = status.HTTP_404_NOT_FOUND
        description = f"Error {error}: Invalid information provided."
        return RedirectResponse(url=f"/error/{description}/save", status_code=302)
    return RedirectResponse(url="/liste", status_code=302)
