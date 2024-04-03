from ..schemas.books import Book
from ..database import database


def save_books(new_book: Book) -> Book:
    new_book["id"] = new_book["id"].strip('\t')
    new_book["id"]= new_book["id"].strip(" ")
    new_book["name"]= new_book["name"].strip('\t')
    new_book["name"]= new_book["name"].strip(" ")
    new_book["Author"]= new_book["Author"].strip('\t')
    new_book["Author"]= new_book["Author"].strip(" ")

    if new_book["Editor"] != None:
        new_book["Editor"]= new_book["Editor"].strip('\t')
        new_book["Editor"]= new_book["Editor"].strip(" ")

    if new_book["id"] == "" or new_book["name"] == "" or new_book["Author"] == "":
        return None
    database["books"].append(new_book)
    return new_book

def get_book_by_id(id: str):
    for book in database['books']:
        if book['id'] == id:
            return Book.model_validate(book)
    return None

def get_all_books() -> list[Book]:
    books_data = database["books"]
    return books_data


def delete_book(book_id: str) -> None:
    for index, book in enumerate(database["books"]):
        book_id = book_id.strip('\t')
        if book["id"] == book_id.strip(" "):
            database["books"].pop(index)
            return 1
    return None

def modify_book(book_id: str, name:str, Author:str, Editor:str) -> Book:
    name = name.strip(" ")
    name = name.strip('\t')
    Author = Author.strip(" ")
    Author = Author.strip('\t')
    if name == "" or Author == "":
                return None
    for index, book in enumerate(database["books"]):
        if book["id"] == book_id:
            book["name"]= name
            book["Author"]= Author
            if Editor != None:
                Editor = Editor.strip(" ")
                Editor = Editor.strip('\t')
            book["Editor"]= Editor
            return 0
    return 1

def get_number_books() -> int:
    return len(database["books"])

    
