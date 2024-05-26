from typing import Optional
from sqlalchemy import select, func
from ..schemas.beers import Beer
from ..database import Session
from ..models.models import Beers, Order, OrderItem, Users, CartItem, association_table

def save_beers(new_beer: Beer):
    """
    This function saves a new beer in the database.

    Parameters:
    -----------
    new_beer : Beer
        An instance of the Beer schema representing the new beer to be saved.

    Returns:
    --------
    Beers
        The newly created Beers entity.
    None
        If the new beer data is invalid.
    """
    from app.database import Session, Beers
    with Session() as session:
        # Clean up the input data
        new_beer.id = new_beer.id.strip()
        new_beer.name = new_beer.name.strip()
        new_beer.brewery = new_beer.brewery.strip()
        new_beer.description = new_beer.description.strip()

        if not new_beer.id or not new_beer.name or not new_beer.brewery:
            return None

        # Create a new Beers entity
        new_beer_entity = Beers(
            id=new_beer.id,
            name=new_beer.name,
            brewery=new_beer.brewery,
            price=new_beer.price,
            stock=new_beer.stock,
            description=new_beer.description,
            image=new_beer.image,
            isdeleted=False
        )
        session.add(new_beer_entity)
        session.commit()
        return new_beer_entity
    
def get_beer_by_id(id: str):
    """
    This function returns a beer object using its id.

    Parameters :
    ------------
    id: str
        The ID of the beer.

    Returns :
    --------
    Beer
        The found beer.
    None
        If no beer has been found.
    """
    with Session() as session:
        statement = select(Beers).filter_by(id=id, isdeleted=False)
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
    This function returns the list of all non-deleted beers.

    Returns :
    --------
    list[Beer]
        The list of beers.
    """
    with Session() as session:
        statement = select(Beers).filter_by(isdeleted=False)
        beers_data = session.scalars(statement).unique().all()
        return [
            Beer(
                id=beer.id,
                name=beer.name,
                brewery=beer.brewery,
                price=beer.price,
                stock=beer.stock,
                description=beer.description,
                image=beer.image,
            )
            for beer in beers_data
        ]

def delete_beer(beer_id: str):
    """
    This function marks a beer as deleted.

    Parameters:
    -----------
    beer_id : str
        The ID of the beer to be deleted.

    Returns:
    --------
    bool
        True if the beer was successfully marked as deleted, False otherwise.
    """
    with Session() as session:
        statement = select(Beers).filter_by(id=beer_id)
        result = session.execute(statement)
        beer = result.fetchone()
        
        if beer is None:
            return None
        
        # Mark the beer as deleted
        beer[0].isdeleted = True
        session.commit()
        
        return True
    
def add_owner(beer_id: str, user_id: str):
    """
    This function adds an owner to a beer.

    Parameters:
    -----------
    beer_id : str
        The ID of the beer.
    user_id : str
        The ID of the user.
    """
    with Session() as session:
        beer = session.scalar(select(Beers).filter_by(id=beer_id))
        user = session.scalar(select(Users).filter_by(id=user_id))
        if beer and user:
            beer.users.append(user)
            session.commit()
            return True
        return False
    
def modify_beer(beer_id: str, image: Optional[str], name: str, brewery: str, price: float, stock: int, description: Optional[str]):
    """
    This function modifies the details of a beer.

    Parameters:
    -----------
    beer_id : str
        The ID of the beer to be modified.
    image : Optional[str]
        The new image URL of the beer (optional).
    name : str
        The new name of the beer.
    brewery : str
        The new brewery of the beer.
    price : float
        The new price of the beer.
    stock : int
        The new stock quantity of the beer.
    description : Optional[str]
        The new description of the beer (optional).

    Returns:
    --------
    Beers
        The modified beer entity.
    int
        1 if no beer was found with the given ID.
    """
    with Session() as session:
        beer = session.scalar(select(Beers).filter_by(id=beer_id))
        
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

def get_active_beers():
    """
    This function returns all active (non-deleted) beers.

    Returns:
    --------
    list[Beers]
        The list of active beers.
    """
    with Session() as session:
        statement = select(Beers).filter_by(isdeleted=False)
        result = session.execute(statement).scalars().all()
        return result

def get_number_beers() -> int:
    """
    This function returns the current number of beers.

    Returns:
    --------
    int
        The number of beers.
    """
    with Session() as session:
        statement = select(func.count(Beers.id))
        count = session.scalar(statement)
        return count
    
def get_number_beers_of_user(user_id: str) -> int:
    """
    This function returns the number of beers in a user's cart.

    Parameters:
    -----------
    user_id : str
        The ID of the user.

    Returns:
    --------
    int
        The number of beers in the user's cart.
    """
    with Session() as session:
        total_quantity = session.query(func.sum(CartItem.quantity)).filter_by(user_id=user_id).scalar()
        return total_quantity or 0

def get_beer_by_user(user_id: str) -> list[dict]:
    """
    This function returns the list of beers and their quantities in a user's cart.

    Parameters:
    -----------
    user_id : str
        The ID of the user.

    Returns:
    --------
    list[dict]
        The list of beers with their quantities.
    """
    with Session() as session:
        cart_items = session.query(CartItem).filter_by(user_id=user_id).all()
        beers_data = [
            {
                "beer": session.query(Beers).filter_by(id=item.beer_id).first(),
                "quantity": item.quantity
            } for item in cart_items
        ]
        return beers_data
    
def drop_beer_panier(beer_id: str, user_id: str):
    """
    This function removes a beer from the user's cart.

    Parameters:
    -----------
    beer_id : str
        The ID of the beer to be removed.
    user_id : str
        The ID of the user.

    Returns:
    --------
    bool
        True if the beer was successfully removed, False otherwise.
    """
    with Session() as session:
        # Query to find the cart item
        cart_item = session.query(CartItem).filter_by(beer_id=beer_id, user_id=user_id).first()

        # If cart item exists, delete it
        if cart_item:
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
    """
    This function updates the quantity of a beer in the user's cart.

    Parameters:
    -----------
    beer_id : str
        The ID of the beer.
    user_id : str
        The ID of the user.
    quantity : int
        The new quantity of the beer.

    Returns:
    --------
    bool
        True if the quantity was successfully updated, False otherwise.
    """
    with Session() as session:
        cart_item = session.query(CartItem).filter_by(user_id=user_id, beer_id=beer_id).first()

        if cart_item is None:
            return False

        # Update the quantity
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

    Returns:
    --------
    bool
        True if the beer was successfully added to the cart, False otherwise.
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
    This function returns the total price of beers in a user's cart.

    Parameters:
    -----------
    user_id : str
        The ID of the user.

    Returns:
    --------
    float
        The total price of the beers in the user's cart.
    """
    with Session() as session:
        statement = select(Users).filter_by(id=user_id)
        user = session.scalar(statement)
        total_price = sum(beer.price for beer in user.beers)
        return total_price
    
def paid_cart(user_id: str):
    """
    This function handles the payment of the user's cart and adds the order to the history.

    Parameters:
    -----------
    user_id : str
        The ID of the user.

    Returns:
    --------
    bool
        True if the payment is successful, False otherwise.
    """
    with Session() as session:
        # Retrieve the items in the user's cart
        cart_items = session.query(CartItem).filter_by(user_id=user_id).all()
        
        if not cart_items:
            return False
        
        # Calculate the total price
        total_price = sum(item.quantity * item.beer.price for item in cart_items)
        
        # Create a new order
        new_order = Order(user_id=user_id, total_price=total_price)
        session.add(new_order)
        session.commit()
        session.refresh(new_order)
        
        # Add the items to the order and update the stock
        for item in cart_items:
            # Retrieve the corresponding beer
            beer = session.query(Beers).filter_by(id=item.beer_id).first()
            
            if beer:
                # Check if there is enough stock
                if beer.stock < item.quantity:
                    # If not enough stock, cancel the transaction
                    session.rollback()
                    return False
                
                # Decrease the stock
                beer.stock -= item.quantity
                session.add(beer)
                
                # Add the order item
                order_item = OrderItem(
                    order_id=new_order.id,
                    beer_id=item.beer_id,
                    quantity=item.quantity,
                    price=item.beer.price
                )
                session.add(order_item)
        
        # Remove the items from the cart
        for item in cart_items:
            session.delete(item)
        
        # Remove the records from the association table
        session.execute(association_table.delete().where(association_table.c.user_id == user_id))
        
        session.commit()
        
        return True
    
def get_orders_by_user(user_id: str) -> list[dict]:
    """
    This function returns the list of orders and their items for a given user.

    Parameters:
    -----------
    user_id : str
        The ID of the user.

    Returns:
    --------
    list[dict]
        The list of orders with their items and quantities.
    """
    with Session() as session:
        # Retrieve all orders associated with the user, including those with deleted beers
        orders = session.query(Order).filter_by(user_id=user_id).all()
        
        orders_data = [
            {
                "order_id": order.id,
                "total_price": order.total_price,
                "created_at": order.created_at,
                "items": [
                    {
                        "beer_id": item.beer_id,
                        "beer_name": item.beer.name if item.beer is not None else "Deleted Beer",
                        "quantity": item.quantity,
                        "price": item.price
                    }
                    for item in order.order_items
                ]
            }
            for order in orders
        ]
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
    dict or None
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