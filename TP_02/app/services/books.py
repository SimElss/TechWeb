from ..schemas.books import Book
from ..database import database


def save_books(new_book: Book) -> Book:
    """
    This function is used to save books

    Parameters :
    ------------
    new_book : the book object which will be saved in database (Object Book)

    Return :
    --------
    None : If informations ar invalid (NoneTypeObject)
    new_book : the book saved  (Object Book)
    """
    #We strip if a user includes tab or space at the end or the begining not on purpose 
    new_book["id"] = new_book["id"].strip('\t')
    new_book["id"]= new_book["id"].strip(" ")
    new_book["name"]= new_book["name"].strip('\t')
    new_book["name"]= new_book["name"].strip(" ")
    new_book["Author"]= new_book["Author"].strip('\t')
    new_book["Author"]= new_book["Author"].strip(" ")

    #Check if Editor has a value (cause optionam)
    if new_book["Editor"] != None:
        new_book["Editor"]= new_book["Editor"].strip('\t')
        new_book["Editor"]= new_book["Editor"].strip(" ")

    #Check if informations are valid
    if new_book["id"] == "" or new_book["name"] == "" or new_book["Author"] == "":
        return None
    database["books"].append(new_book) #add book to database
    return new_book

def get_book_by_id(id: str):
    """"
    This function returns a book object using it id

    Parameters :
    ------------
    id: id of the book (str)

    Return :
    --------
    Book.model_validate(book) : the found book (Object Book)
    None : If no book has benn found (NoneTypeObject)
    """
    for book in database['books']:
        if book['id'] == id:
            return Book.model_validate(book)
    return None

def get_all_books() -> list[Book]:
    """
    This function returns the list of the books

    Return :
    --------
    books_data : teh list of books (list of Object Book)
    """
    #Uqing key books to retrieve list of books
    books_data = database["books"]
    return books_data


def delete_book(book_id: str) -> None:
    """
    This function delete the book corresponding to id

    Parameters:
    -----------
    book_id : the id of the book which will be deleted (str)

    Return :
    --------
    1 : to check if the book has been deleted (int)
    None : if we find no book corresponding to the id (NoneTypeObject)
    """
    for index, book in enumerate(database["books"]):
        book_id = book_id.strip('\t')
        if book["id"] == book_id.strip(" "):
            database["books"].pop(index)
            return 1
    return None

def modify_book(book_id: str, name:str, Author:str, Editor:str):
    """
    This function modifies a book

    Parameters:
    -----------
    book_id : the id of the book which will be modified (str)
    name : new name of the book (str)
    Author : new Author of the book
    Editor : new Editor  of the book | values "" if no Editor | str

    Return:
    -------
    None : if informations are invalid (NoneTypeObject)
    0 : if book has been modified (int)
    1 : if no book has been find using book_id
    """
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
    """
    This function returns the current number of books

    Return :
    --------
    len(database["books"]) : the number of books (int) 
    """
    return len(database["books"])

    
