from typing import Annotated
from uuid import uuid4
from fastapi import APIRouter, HTTPException, status
from ..services.books import get_all_books, delete_book, modify_book, save_books, get_number_books

from fastapi import APIRouter, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
def index():
    return templates.TemplateResponse(
        "index.html"
    )

@router.get("/liste")
def list_books():
    nb = get_number_books()
    books = get_all_books()
    return templates.TemplateResponse(
        "books.html", 
        context={"books": books, "Nombre":nb}
    )

@router.get("/modify")
def modify():
    new_book = modify_book("1", {"id" : "1", "name" : "New_name_modify", "author" : "New auhor", "editor": "New editor"})
    if new_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No task found with this ID.",
        )
    return new_book

@router.get("/delete")
def delete():
    id = "1"
    response = delete_book(id)
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No task found with this ID.",
        )
    return f"Book {id} has been deleted" 

@router.post("/save")
def save(name: Annotated[str, Form()], author: Annotated[str, Form()], editor: Annotated[str, Form()]):

    new_book = save_books({
        "id" : str(uuid4), 
        "name" : name, 
        "author" : author, 
        "editor": editor,
        })
    if new_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Please provide all the information for the book. (no empty field)",
        )
    return RedirectResponse(url="/liste", status_code=302)