from fastapi import APIRouter
from ..services.books import get_all_books, delete_book, modify_book, save_books, get_number_books

router = APIRouter()

@router.get("/")
def index():
    return {"message": "Hello, World!"}

@router.get("/liste")
def list_books():
    books = get_all_books()
    return books

@router.get("/modify")
def modify():
    new_book = modify_book("1", {"id" : "1", "name" : "New_name_modify", "author" : "New auhor", "editor": "New editor"})
    return new_book

@router.get("/number")
def get_number():
    Nb = get_number_books()
    return Nb

@router.get("/delete")
def delete():
    id = "1"
    delete_book(id)
    return "Book {id} has been deleted" 

@router.get("/save")
def save():
    save_books({"id" : "1", "name" : "New_name", "author" : "New auhor", "editor": "New editor"})
    return "Book added to list !"