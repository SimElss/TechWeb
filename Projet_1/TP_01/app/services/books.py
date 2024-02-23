from app.schemas import Book
from app.database import database


def save_books(new_book: Book) -> Book:
    database["books"].append(new_book)
    return new_book


def get_all_books() -> list[Book]:
    books_data = database["books"]
    books = [Book.model_validate(data) for data in books_data]
    return books


def delete_book(book_id: str) -> None:
    for index, book in enumerate(database["books"]):
        if book["id"] == book_id:
            database["books"].pop(index)
            break

def modify_book(book_id: str, new_book: Book) -> Book:
    for index, book in enumerate(database["books"]):
        if book["id"] == book_id:
            database["books"][index] = new_book.dict()
            return new_book
    return None

def get_number_books() -> int:
    return "Il y a ",len(database["books"])

    
