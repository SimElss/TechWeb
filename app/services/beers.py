from typing import Optional
from sqlalchemy import select, func


from ..schemas.beers import Beer
from ..database import Session
from ..models.models import Beers, Order, OrderItem, Users, CartItem, association_table


# Fonction pour sauvegarder les bières
def save_beers(new_beer: Beer):
    from app.database import Session, Beers
    with Session() as session:
        new_beer.id = new_beer.id.strip()
        new_beer.name = new_beer.name.strip()
        new_beer.brewery = new_beer.brewery.strip()
        new_beer.description = new_beer.description.strip()

        if not new_beer.id or not new_beer.name or not new_beer.brewery:
            return None

        new_beer_entity = Beers(
            id=new_beer.id,
            name=new_beer.name,
            brewery=new_beer.brewery,
            price=new_beer.price,
            stock=new_beer.stock,
            description=new_beer.description,
            image=new_beer.image
        )
        session.add(new_beer_entity)
        session.commit()
        return new_beer_entity

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


def delete_beer(beer_id: str):
    with Session() as session:
        statement = select(Beers).filter_by(id=beer_id)
        result = session.execute(statement)
        beer = result.fetchone()
        if beer is None:
            return None
        session.delete(beer[0])  # Accédez à la première colonne (0) qui contient l'objet Beer
        session.commit()
        return True
    
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
    
def modify_beer(beer_id: str, image: Optional[str], name: str, brewery: str, price: float, stock: int, description: Optional[str]):
    
    with Session() as session:
        statement = select(Beers).filter_by(id=beer_id)
        beer = session.scalar(statement)
        
        if beer is None:
            return 1  # No beer found with this ID
        
        # Update fields
        beer.name = name.strip() if name.strip() else beer.name
        beer.brewery = brewery.strip() if brewery.strip() else beer.brewery
        beer.price = price
        if description is not None:
            beer.description = description.strip()
        if image is not None:
            beer.image = image.strip()

        session.commit()
        return beer

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
    """with Session() as session:
        statement = select(Users).filter_by(id=user_id)
        user = session.scalar(statement)
        count = len(user.beers)
        return count
    """
    with Session() as session:
        # Query to sum the quantities of all beers in the user's cart
        total_quantity = session.query(func.sum(CartItem.quantity)).filter_by(user_id=user_id).scalar()

        # If total_quantity is None (no cart items), return 0, otherwise return the sum
        return total_quantity or 0

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
        # Query to find the cart item
        cart_item = session.query(CartItem).filter_by(beer_id=beer_id, user_id=user_id).first()

        # If cart item exists, delete it
        if cart_item:
            # Delete the cart item
            session.delete(cart_item)
            session.commit()
            
            # Also delete the association from the association table
            association_entry = association_table.delete().where(
                (association_table.c.user_id == user_id) & (association_table.c.beer_id == beer_id)
            )
            session.execute(association_entry)
            session.commit()
            
            return True

    return False

def update_cart_item_quantity(beer_id: str, user_id: str, quantity: int) -> bool:
    with Session() as session:
        # Récupérer l'article du panier correspondant
        cart_item = session.query(CartItem).filter_by(user_id=user_id, beer_id=beer_id).first()

        if cart_item is None:
            return False

        # Mettre à jour la quantité
        cart_item.quantity = quantity
        session.commit()
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
        
        # Supprimer les enregistrements de la table d'association
        session.execute(association_table.delete().where(association_table.c.user_id == user_id))
        
        
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
        print(orders_data)
        return orders_data

def get_order_details_by_id(user_id: str, order_id: str) -> dict:
    """
    Get the details of a specific order for a user.

    Parameters:
    -----------
    user_id : str
        The ID of the user.
    order_id : str
        The ID of the order.

    Returns:
    --------
    order_details : dict or None
        A dictionary containing order details if found, else None.
    """
    with Session() as session:
        order = session.query(Order).filter_by(id=order_id, user_id=user_id).first()
        
        if order is None:
            return None
        
        order_details = {
            "order_id": order.id,
            "total_price": order.total_price,
            "created_at": order.created_at,
            "items": [
                {
                    "beer_name": item.beer.name,
                    "quantity": item.quantity,
                    "price": item.price
                }
                for item in order.order_items
            ]
        }
        return order_details