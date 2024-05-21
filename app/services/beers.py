from sqlalchemy import select, func


from ..schemas.beers import Beer
from ..database import Session
from ..models.models import Beers, Order, OrderItem, Users, CartItem, association_table


def save_beers(new_beer: Beers, user_id: str):
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
                brewery=beer.brewery,
                price=beer.price,
                stock=beer.stock,
                description=beer.description,
                image=beer.image
            )
    return None

def get_all_beers() -> list[Beer]:
    """
    This function returns the list of the beers

    Return :
    --------
    beers_data : thz list of beers (list of Object Beer)
    """
    with Session() as session:
        statement = select(Beers) #Model Beer
        beers_data = session.scalars(statement).unique().all()
        #Schema Beers
        return [
            Beer(
                id=beer.id,
                name=beer.name,
                brewery = beer.brewery,
                price=beer.price,
                stock=beer.stock,
                description=beer.description,
                image=beer.image,
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

def modify_beer(beer_id: str, name:str = None, brewery:str = None, price:float = None):
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
    if name != None and brewery != None and price != None:
        name = name.strip(" ")
        name = name.strip('\t')
        brewery = brewery.strip(" ")
        brewery = brewery.strip('\t')
        if name == "" or brewery == "":
            return None
        with Session() as session:
            statement = select(Beers).filter_by(id=beer_id)
            beer = session.scalar(statement)
            if beer is not None:
                beer.name=name
                beer.brewery=brewery
                beer.price=price

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
        count = len(user.beers)
        return count

def get_beer_by_user(user_id: str) -> list[dict]:
    """
    This function returns the list of beers and their quantities in the cart of a user.

    Parameters:
    -----------
    user_id : the id of the user (str)

    Return :
    --------
    beers_data : the list of beers with their quantities (list of dict)
    """
    with Session() as session:
        statement = select(Users).filter_by(id=user_id)
        user = session.scalar(statement)
        cart_items = session.query(CartItem).filter_by(user_id=user_id).all()

        beers_data = [
            {
                "beer": session.query(Beers).filter_by(id=item.beer_id).first(),
                "quantity": item.quantity
            } for item in cart_items
        ]

        return beers_data
    
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
        beer.users.append(user)
        session.commit()
        return True
def drop_beer_panier(beer_id,user_id):
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
    with Session() as session:
        # Requête pour récupérer la bière
        statement = select(Beers).filter_by(id=beer_id)
        beer = session.scalar(statement)
        # Requête pour récupérer l'utilisateur
        statement = select(Users).filter_by(id=user_id)
        user = session.scalar(statement)
        
        # Vérifie que la bière et l'utilisateur existent
        if beer is not None and user is not None:
            # Supprime l'utilisateur de la liste des utilisateurs de la bière
            if user in beer.users:
                beer.users.remove(user)
                session.commit()
                return True
        return True

def add_to_cart(beer_id: str, user_id: str):
    """
    This function adds a beer to the user's cart.
    
    Parameters:
    -----------
    beer_id : str
        The ID of the beer.
    user_id : str
        The ID of the user.
    """
    with Session() as session:
        try:
            # Check if the cart item already exists
            statement = select(CartItem).filter_by(beer_id=beer_id, user_id=user_id)
            cart_item = session.scalar(statement)
            if cart_item:
                # If the item already exists, you might want to update the quantity or notify the user
                print("Beer already in cart.")
                return False
            
            # Create a new cart item
            new_cart_item = CartItem(beer_id=beer_id, user_id=user_id, quantity=1)
            session.add(new_cart_item)
            session.commit()
            return True
        except Exception as e:
            print(f"Error adding beer to cart: {e}")
            session.rollback()
            return False

def is_beer_in_cart(beer_id: str, user_id: str) -> bool:
    """
    Check if the given beer is already in the user's cart.

    Parameters:
    -----------
    beer_id : str
        The ID of the beer to check.
    user_id : str
        The ID of the user whose cart to check.

    Returns:
    --------
    bool
        True if the beer is in the user's cart, False otherwise.
    """
    with Session() as session:
        # Query the association table to check if the beer is in the user's cart
        statement = select(association_table).filter_by(user_id=user_id, beer_id=beer_id)
        result = session.execute(statement)
        return result.scalar() is not None
    
def get_price_cart(user_id: str) -> float:
    """
    This function returns the total price of beers owned by a user

    Parameters:
    -----------
    user_id : the id of the user (str)

    Return :
    --------
    total_price : the total price of the user's beers (float)
    """
    with Session() as session:
        statement = select(Users).filter_by(id=user_id)
        user = session.scalar(statement)
        total_price = sum(beer.price for beer in user.beers)
        return total_price
    
def paid_cart(user_id: str):
    """
    Cette fonction gère le paiement du panier et ajoute la commande à l'historique.

    Paramètres :
    ------------
    user_id : str
        L'ID de l'utilisateur.

    Retour :
    --------
    bool
        True si le paiement est réussi, False sinon.
    """
    with Session() as session:
        # Récupérer les articles du panier de l'utilisateur
        cart_items = session.query(CartItem).filter_by(user_id=user_id).all()
        
        if not cart_items:
            return False
        
        # Calculer le prix total
        total_price = sum(item.quantity * item.beer.price for item in cart_items)
        
        # Créer une nouvelle commande
        new_order = Order(user_id=user_id, total_price=total_price)
        session.add(new_order)
        session.commit()
        session.refresh(new_order)
        
        # Ajouter les articles de la commande
        for item in cart_items:
            order_item = OrderItem(
                order_id=new_order.id,
                beer_id=item.beer_id,
                quantity=item.quantity,
                price=item.beer.price
            )
            session.add(order_item)
        
        # Supprimer les articles du panier
        for item in cart_items:
            session.delete(item)
        
        session.commit()
        
        return True
    
def get_orders_by_user(user_id: str) -> list[dict]:
    """
    Cette fonction retourne la liste des commandes et leurs articles pour un utilisateur donné.

    Paramètres:
    -----------
    user_id : str
        L'ID de l'utilisateur.

    Retour:
    -------
    orders_data : list[dict]
        La liste des commandes avec leurs articles et quantités.
    """
    with Session() as session:
        # Requête pour récupérer l'utilisateur et ses commandes
        statement = select(Users).filter_by(id=user_id)
        user = session.scalar(statement)
        
        if user is None:
            return []
        
        orders = user.orders
        orders_data = [
            {
                "order_id": order.id,
                "total_price": order.total_price,
                "created_at": order.created_at,
                "items": [
                    {
                        "beer_id": item.beer_id,
                        "beer_name": item.beer.name,
                        "quantity": item.quantity,
                        "price": item.price
                    }
                    for item in order.order_items
                ]
            }
            for order in orders
        ]
        
        return orders_data