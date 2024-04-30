from sqlalchemy import select, func


from ..schemas.books import Book
from ..database import Session
from ..models.models import Books, Users


def save_books(new_book: Book, user_id: str):
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
    with Session() as session:
        #We strip if a user includes tab or space at the end or the begining not on purpose 
        new_book.id = new_book.id.strip('\t')
        new_book.id= new_book.id.strip(" ")
        new_book.name= new_book.name.strip('\t')
        new_book.name= new_book.name.strip(" ")
        new_book.Author= new_book.Author.strip('\t')
        new_book.Author= new_book.Author.strip(" ")

        #Check if Editor has a value (cause optionam)
        if new_book.Editor != None:
            new_book.Editor= new_book.Editor.strip('\t')
            new_book.Editor= new_book.Editor.strip(" ")

        #Check if informations are valid
        if new_book.id == "" or new_book.name == "" or new_book.Author == "":
            return None
        
        #On remplit le modèle
        new_book_entity = Books(
            id=new_book.id,
            name=new_book.name,
            Author = new_book.Author, 
            Editor = new_book.Editor,
            price = new_book.price,
            bought = new_book.bought,
            new_owner_id = new_book.new_owner_id
        )
        session.add(new_book_entity)#add book to database

        user = session.query(Users).filter_by(id=user_id).first()
        user.book.append(new_book_entity)

        session.commit()
        return True

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
    with Session() as session:
        statement = select(Books).filter_by(id=id)
        book = session.scalar(statement) 
        if book is not None:
            return Book(
                id=book.id,
                name=book.name,
                Author=book.Author,
                Editor=book.Editor,
                price=book.price,
                bought=book.bought
            )
    return None

def get_all_books() -> list[Book]:
    """
    This function returns the list of the books

    Return :
    --------
    books_data : teh list of books (list of Object Book)
    """
    with Session() as session:
        statement = select(Books) #Model Book
        books_data = session.scalars(statement).unique().all()
        #Schema Books
        return [
            Book(
                id=book.id,
                name=book.name,
                Author=book.Author,
                Editor=book.Editor,
                price=book.price,
            )
            for book in books_data
        ]


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
    book_id = book_id.strip(" ")
    book_id = book_id.strip('\t')
    with Session() as session:
         statement = select(Books).filter_by(id=book_id)
         book = session.scalar(statement)
         if book is not None:
            session.delete(book)
            session.commit()
            return True
    return None

def modify_book(book_id: str, bought:bool, name:str = None, Author:str = None, Editor:str = None, price:float = None):
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
    if name != None and Author != None and price != None:
        name = name.strip(" ")
        name = name.strip('\t')
        Author = Author.strip(" ")
        Author = Author.strip('\t')
        if name == "" or Author == "":
            return None
        if Editor != None:
            Editor = Editor.strip(" ")
            Editor = Editor.strip('\t')
        with Session() as session:
            statement = select(Books).filter_by(id=book_id)
            book = session.scalar(statement)
            if book is not None:
                book.name=name
                book.Author=Author
                book.Editor=Editor
                book.price=price

                session.commit()
                return 0
    else:
        with Session() as session:
            statement = select(Books).filter_by(id=book_id)
            book = session.scalar(statement)
            if book is not None:
                book.bought = bought
                session.commit()
                return 0
    return 1

def get_number_books() -> int:
    """
    This function returns the current number of books by id

    Return :
    --------
    count : the number of books (int) 
    """
    with Session() as session:
        statement = select(func.count(Books.id))
        count = session.scalar(statement)
        return count
    
def get_number_books_client() -> int:
    """
    This function return the books of the client view so only the books which are not bought and by id

    Return :
    --------
    count : the number of books (int)
    """

    with Session() as session:
        statement = select(func.count(Books.id)).filter_by(bought=False)
        count = session.scalar(statement)
        return count
    


def get_number_books_of_user(user_id: str) -> int:
    """
    This function returns the number of books of a user

    Parameters:
    -----------
    user_id : the id of the user (str)

    Return :
    --------
    count : the number of books of the user (int)
    """
    with Session() as session:
        statement = select(Users).filter_by(id=user_id)
        user = session.scalar(statement)
        count = len(user.book)
        return count

def get_book_by_user(user_id: str) -> list[Book]:
    """
    This function returns the list of books of a user

    Parameters:
    -----------
    user_id : the id of the user (str)

    Return :
    --------
    books_data : the list of books of the user (list of Object Book)
    """
    with Session() as session:
        statement = select(Users).filter_by(id=user_id)
        user = session.scalar(statement)
        
        books = user.book

        return books
    
def add_owner(book_id, user_id):
    """
    This function adds an owner to a book
    We don't delete the previous owner because he can view his sold books

    Parameters:
    -----------
    book_id : the id of the book (str)
    user_id : the id of the user (str)
    """
    with Session() as session:
        statement = select(Books).filter_by(id=book_id)
        book = session.scalar(statement)
        statement = select(Users).filter_by(id=user_id)
        user = session.scalar(statement)
        book.user.append(user)
        book.new_owner_id = user_id
        session.commit()
        return True