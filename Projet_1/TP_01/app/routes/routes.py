from fastapi import APIRouter, HTTPException, status
from ..services.books import get_all_books, delete_book, modify_book, save_books, get_number_books

router = APIRouter()

@router.get("/")
def index():
    return "Index page"

@router.get("/liste")
def list_books():
    books = get_all_books()
    return books

@router.get("/modify")
def modify():
    new_book = modify_book("1", {"id" : "1", "name" : "New_name_modify", "author" : "New auhor", "editor": "New editor"})
    if new_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No task found with this ID.",
        )
    return new_book

@router.get("/number")
def get_number():
    Nb = get_number_books()
    return Nb

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

@router.get("/save")
def save():
    response = save_books({"id" : "1", "name" : "New_name", "author" : "New auhor", "editor": "New editor"})
    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Please provide all the information for the book. (no empty field)",
        )
    return "Book added to list !"