from sqlalchemy import select, func


from ..schemas.beers import Beer
from ..database import Session
from ..models.models import Beers, Users


def save_beers(new_beer: Beer, user_id: str):
    """
    This function is used to save beers

    Parameters :
    ------------
    new_beer : the beer object which will be saved in database (Object beer)

    Return :
    --------
    None : If informations ar invalid (NoneTypeObject)
    new_beer : the beer saved  (Object Beer)
    """
    with Session() as session:
        #We strip if a user includes tab or space at the end or the begining not on purpose 
        new_beer.id = new_beer.id.strip('\t')
        new_beer.id= new_beer.id.strip(" ")
        new_beer.name= new_beer.name.strip('\t')
        new_beer.name= new_beer.name.strip(" ")
        new_beer.Author= new_beer.Author.strip('\t')
        new_beer.Author= new_beer.Author.strip(" ")

        #Check if Editor has a value (cause optionam)
        if new_beer.Editor != None:
            new_beer.Editor= new_beer.Editor.strip('\t')
            new_beer.Editor= new_beer.Editor.strip(" ")

        #Check if informations are valid
        if new_beer.id == "" or new_beer.name == "" or new_beer.Author == "":
            return None
        
        #On remplit le modèle
        new_beer_entity = Beers(
            id=new_beer.id,
            name=new_beer.name,
            Author = new_beer.Author, 
            Editor = new_beer.Editor,
            price = new_beer.price,
            bought = new_beer.bought,
            new_owner_id = new_beer.new_owner_id
        )
        session.add(new_beer_entity)#add beer to database

        user = session.query(Users).filter_by(id=user_id).first()
        user.beer.append(new_beer_entity)

        session.commit()
        return True

def get_beer_by_id(id: str):
    """"
    This function returns a beer object using it id

    Parameters :
    ------------
    id: id of the beer (str)

    Return :
    --------
    Beer.model_validate(beer) : the found beer (Object Beer)
    None : If no beer has benn found (NoneTypeObject)
    """
    with Session() as session:
        statement = select(Beers).filter_by(id=id)
        beer = session.scalar(statement) 
        if beer is not None:
            return Beer(
                id=beer.id,
                name=beer.name,
                Author=beer.Author,
                Editor=beer.Editor,
                price=beer.price,
                bought=beer.bought
            )
    return None

def get_all_beers() -> list[Beer]:
    """
    This function returns the list of the beers

    Return :
    --------
    beers_data : teh list of beers (list of Object Beer)
    """
    with Session() as session:
        statement = select(Beers) #Model Beer
        beers_data = session.scalars(statement).unique().all()
        #Schema Beers
        return [
            Beer(
                id=beer.id,
                name=beer.name,
                Author=beer.Author,
                Editor=beer.Editor,
                price=beer.price,
            )
            for beer in beers_data
        ]


def delete_beer(beer_id: str) -> None:
    """
    This function delete the beer corresponding to id

    Parameters:
    -----------
    beer_id : the id of the beer which will be deleted (str)

    Return :
    --------
    1 : to check if the beer has been deleted (int)
    None : if we find no beer corresponding to the id (NoneTypeObject)
    """
    beer_id = beer_id.strip(" ")
    beer_id = beer_id.strip('\t')
    with Session() as session:
         statement = select(Beers).filter_by(id=beer_id)
         beer = session.scalar(statement)
         if beer is not None:
            session.delete(beer)
            session.commit()
            return True
    return None

def modify_beer(beer_id: str, bought:bool, name:str = None, Author:str = None, Editor:str = None, price:float = None):
    """
    This function modifies a beer

    Parameters:
    -----------
    beer_id : the id of the beer which will be modified (str)
    name : new name of the beer (str)
    Author : new Author of the beer
    Editor : new Editor  of the beer | values "" if no Editor | str

    Return:
    -------
    None : if informations are invalid (NoneTypeObject)
    0 : if beer has been modified (int)
    1 : if no beer has been find using beer_id
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
            statement = select(Beers).filter_by(id=beer_id)
            beer = session.scalar(statement)
            if beer is not None:
                beer.name=name
                beer.Author=Author
                beer.Editor=Editor
                beer.price=price

                session.commit()
                return 0
    else:
        with Session() as session:
            statement = select(Beers).filter_by(id=beer_id)
            beer = session.scalar(statement)
            if beer is not None:
                beer.bought = bought
                session.commit()
                return 0
    return 1

def get_number_beers() -> int:
    """
    This function returns the current number of beers by id

    Return :
    --------
    count : the number of beers (int) 
    """
    with Session() as session:
        statement = select(func.count(Beers.id))
        count = session.scalar(statement)
        return count
    
def get_number_beers_client() -> int:
    """
    This function return the beers of the client view so only the beers which are not bought and by id

    Return :
    --------
    count : the number of beers (int)
    """

    with Session() as session:
        statement = select(func.count(Beers.id)).filter_by(bought=False)
        count = session.scalar(statement)
        return count
    


def get_number_beers_of_user(user_id: str) -> int:
    """
    This function returns the number of beers of a user

    Parameters:
    -----------
    user_id : the id of the user (str)

    Return :
    --------
    count : the number of beers of the user (int)
    """
    with Session() as session:
        statement = select(Users).filter_by(id=user_id)
        user = session.scalar(statement)
        count = len(user.beer)
        return count

def get_beer_by_user(user_id: str) -> list[Beer]:
    """
    This function returns the list of beers of a user

    Parameters:
    -----------
    user_id : the id of the user (str)

    Return :
    --------
    beers_data : the list of beers of the user (list of Object Beer)
    """
    with Session() as session:
        statement = select(Users).filter_by(id=user_id)
        user = session.scalar(statement)
        
        beers = user.beer

        return beers
    
def add_owner(beer_id, user_id):
    """
    This function adds an owner to a beer
    We don't delete the previous owner because he can view his sold beers

    Parameters:
    -----------
    beer_id : the id of the beer (str)
    user_id : the id of the user (str)
    """
    with Session() as session:
        statement = select(Beers).filter_by(id=beer_id)
        beer = session.scalar(statement)
        statement = select(Users).filter_by(id=user_id)
        user = session.scalar(statement)
        beer.user.append(user)
        beer.new_owner_id = user_id
        session.commit()
        return True