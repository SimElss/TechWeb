from ..schemas.books import Book
from ..database import database


def save_books(new_book: Book) -> Book:
    new_book["id"]= new_book["id"].strip(" ")
    new_book["name"]= new_book["name"].strip(" ")
    new_book["Author"]= new_book["Author"].strip(" ")
    new_book["Editor"]= new_book["Editor"].strip(" ")
    if new_book["id"] == "" or new_book["name"] == "" or new_book["Author"] == "" or new_book["Editor"] == "":
        return None
    database["books"].append(new_book)
    return new_book


def get_all_books() -> list[Book]:
    books_data = database["books"]
    return books_data


def delete_book(book_id: str) -> None:
    for index, book in enumerate(database["books"]):
        if book["id"] == book_id:
            database["books"].pop(index)
            return 1
    return None

def modify_book(book_id: str, new_book: Book) -> Book:
    for index, book in enumerate(database["books"]):
        if book["id"] == book_id:
            new_book["id"]= new_book["id"].strip(" ")
            new_book["name"]= new_book["name"].strip(" ")
            new_book["Author"]= new_book["Author"].strip(" ")
            new_book["Editor"]= new_book["Editor"].strip(" ")
            if new_book["id"] == "" or new_book["name"] == "" or new_book["Author"] == "" or new_book["Editor"] == "":
                return None
            database["books"][index] = new_book
            return new_book
    return 1

def get_number_books() -> int:
    return len(database["books"])

    
