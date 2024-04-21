from typing import Annotated, Optional
from uuid import uuid4
from fastapi import APIRouter, status, Depends
from ..login_manager import login_manager
from ..services.books import get_all_books, delete_book, modify_book, save_books, get_number_books, get_book_by_id, add_owner, get_number_books_client
from ..services.users import get_book_owners, get_user_by_book
from ..schemas.users import UserSchema
from ..schemas.books import Book
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
    book_with_owner = get_book_owners()
    if user.group == "admin":
        nb = get_number_books()
    else:
        nb = get_number_books_client()
    profile = False
    return templates.TemplateResponse(
        "books.html", 
        context={'request': request,'Nombre': nb, 'current_user': user, 'book_with_owner': book_with_owner, 'in_profile': profile}
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
    #check if user is admin -> only admin can modify book
    owner = get_user_by_book(id)
    if owner is None:
        error = status.HTTP_404_NOT_FOUND
        description = f"Error {error}: No book found with this ID"
        return RedirectResponse(url=f"/error/{description}/liste", status_code=302)
    if user.group != "admin" and owner.id != user.id:
        error = status.HTTP_403_FORBIDDEN
        description = f"Error {error}: Access forbidden."
        return RedirectResponse(url=f"/error/{description}/liste", status_code=302)
    book = get_book_by_id(id)
    nb = get_number_books()
    return templates.TemplateResponse(
        "modify.html", 
        context={'request': request, 'Nombre': nb, 'book': book}
    )

# Route to modify a book (POST request)
@router.post("/modify/{id}")
def modify(id: str, name: Annotated[str, Form()], Author: Annotated[str, Form()], price:Annotated[float, Form()], Editor: Annotated[Optional[str], Form()] = None):
    response = modify_book(id, None, name, Author, Editor, price)
    #if None user had just enter spaces in one of the field (not optional one)
    if response is None:
        error = status.HTTP_400_BAD_REQUEST
        description = f"Error {error}: Invalid information provided."
        return RedirectResponse(url=f"/error/{description}/modify", status_code=302)
    #Check if the id is valid
    if response == 1:
        error = status.HTTP_400_BAD_REQUEST
        description = f"Error {error}: No book found with this ID"
        return RedirectResponse(url=f"/error/{description}/modify", status_code=302)
    return RedirectResponse(url="/liste", status_code=302)

# Route to add a new book
@router.get("/save")
def save(request: Request, user: UserSchema = Depends(login_manager.optional)):
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    # check if user is admin -> only admin can modify book
    return templates.TemplateResponse(
        "save_book.html", 
        context={'request': request, 'current_user': user}
    )

# Route to add a new book (POST request)
@router.post("/save")
def save(name: Annotated[str, Form()], Author: Annotated[str, Form()],price:Annotated[float, Form()], Editor: Annotated[Optional[str], Form()] = None, user = Depends(login_manager.optional)):
    new_book = {
        "id" : str(uuid4()),
        "name" : name,
        "Author" : Author,
        "Editor": Editor,
        "price": price,
        "bought": False,
        "new_owner_id": None
        }
    new_book = Book.model_validate(new_book)
    saved_book = save_books(new_book, user.id)
    #if None user had just enter spaces in one of the field (not optional one)
    if saved_book is None:
        error = status.HTTP_404_NOT_FOUND
        description = f"Error {error}: Invalid information provided."
        return RedirectResponse(url=f"/error/{description}/save", status_code=302)
    return RedirectResponse(url="/profile", status_code=302)

# Route to but the book (POST request)
@router.post("/buy/{id}")
def buy(id: str, user = Depends(login_manager.optional)):
    #We verify that the user is connected
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    #We verify that the book exists
    book = get_book_by_id(id)
    if book is None:
        error = status.HTTP_404_NOT_FOUND
        description = f"Error {error}: No book found with this ID"
        return RedirectResponse(url=f"/error/{description}/liste", status_code=302)
    #change the status of the book to bought
    modify_book(id, True)
    #add the user as owner of the book
    add_owner(id, user.id)
    return RedirectResponse(url="/liste", status_code=302)