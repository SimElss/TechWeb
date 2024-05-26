from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from uuid import uuid4
import hashlib

# Create an engine and session to connect to the SQLite database
engine = create_engine(
    "sqlite:///data/db.sqlite",  # Path to the database file
    echo=False,  # Show generated SQL code in the terminal
)
Session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

from app.models.models import Base, Users, Beers, Admins, association_table, CartItem, Order, OrderItem

def create_database():
    """
    Create all tables in the database.
    """
    Base.metadata.create_all(engine)

def delete_database():
    """
    Clear all table definitions from the metadata.
    """
    Base.metadata.clear()

def vider_db():
    """
    Delete all records from all tables in the database.
    """
    session = Session()
    try:
        # Delete all records from each table
        session.query(Users).delete()
        session.query(Beers).delete()
        session.query(Admins).delete()
        session.query(CartItem).delete()
        session.query(Order).delete()
        session.query(OrderItem).delete()
        session.query(association_table).delete()
        
        session.commit()
    except Exception as e:
        print(f"Error while emptying the database: {e}")
        session.rollback()
    finally:
        session.close()

def initialiser_db():
    """
    Initialize the database with initial data if the tables are empty.
    """
    with Session() as session:
        # Check if the Users table is already populated
        if session.query(Users).count() == 0:
            # Create beers
            beer_1 = Beers(id=str(uuid4()), name="Quantum Ale", brewery="Schrödinger's Brewery", price=4.7, stock=75, description="A light and refreshing beer infused with citrus and a touch of quantum mystery. Each sip is a unique experience.", image="./static/quantum_ale.jpg",isdeleted=False)
            beer_2 = Beers(id=str(uuid4()), name="Pixel Pils", brewery="Retro Brew Co.", price=3.9, stock=100, description="Relive the retro gaming era with this crisp and clear pilsner. Perfect for a classic video game night.", image="./static/pixel_pils.jpg",isdeleted=False)
            beer_3 = Beers(id=str(uuid4()), name="Hops of Hyrule", brewery="Triforce Brewery", price=5.3, stock=60, description="A bold and adventurous IPA brewed with rare hops from the lands of Hyrule. Perfect for heroes seeking an epic beer.", image="./static/hops_of_hyrule.jpg",isdeleted=False)
            beer_4 = Beers(id=str(uuid4()), name="Stark Stout", brewery="Iron Craft Brewery", price=5.5, stock=40, description="A rich and robust stout with notes of coffee and dark chocolate. As powerful as a certain iron man's armor.", image="./static/stark_stout.jpg",isdeleted=False)
            beer_5 = Beers(id=str(uuid4()), name="Warp Speed Wheat", brewery="Starfleet Brewery", price=4.8, stock=85, description="A smooth and spicy wheat beer brewed for space explorers. One sip and you'll be propelled to light speed.", image="./static/warp_speed_wheat.jpg",isdeleted=False)
            beer_6 = Beers(id=str(uuid4()), name="Dragonfire Doppelbock", brewery="Dragon's Den Brewery", price=6.0, stock=50, description="A rich and malty doppelbock infused with fiery spices. Perfect for adventurers and dragon enthusiasts.", image="./static/dragonfire_doppelbock.jpg",isdeleted=False)
            beer_7 = Beers(id=str(uuid4()), name="Galactic Porter", brewery="Nebula Brewing Co.", price=5.2, stock=70, description="A dark and mysterious porter with notes of caramel and cocoa. Embark on an interstellar journey with every sip.", image="./static/galactic_porter.jpg",isdeleted=False)
            beer_8 = Beers(id=str(uuid4()), name="Mana Potion Ale", brewery="Arcane Brewmasters", price=4.9, stock=90, description="A magical and energizing ale brewed with secret herbs and mystical essences. Recharge your mana with this delicious potion.", image="./static/mana_potion_ale.jpg",isdeleted=False)

            # Create passwords and hash them
            password_1 = "Admin!123"
            password_2 = "Password!123"
            password_3 = "Password!123"
            encoded_password_1 = password_1.encode()
            hashed_password_1 = hashlib.sha3_256(encoded_password_1).hexdigest()

            encoded_password_2 = password_2.encode()
            hashed_password_2 = hashlib.sha3_256(encoded_password_2).hexdigest()

            encoded_password_3 = password_3.encode()
            hashed_password_3 = hashlib.sha3_256(encoded_password_3).hexdigest()
            
            # Create users
            user_1 = Users(id=str(uuid4()), username="admin", name="admin", surname="admin", password=hashed_password_1, email="admin@juice-sh.op", group="admin", whitelist=True)
            user_2 = Users(id=str(uuid4()), username="User2", name="Doe", surname="John", password=hashed_password_2, email="user@gmail.com", group="client", whitelist=True)
            user_3 = Users(id=str(uuid4()), username="User3", name="Doe", surname="John", password=hashed_password_3, email="elicesimon06@gmail.com", group="client", whitelist=True)

            # Create admin
            admin_1 = Admins(id=1, user_id=user_1.id)

            # Associate beers with users via cart
            cart_item_1 = CartItem(user_id=user_1.id, beer_id=beer_1.id, quantity=7)
            cart_item_2 = CartItem(user_id=user_1.id, beer_id=beer_2.id, quantity=1)
            cart_item_3 = CartItem(user_id=user_2.id, beer_id=beer_3.id, quantity=2)
            cart_item_4 = CartItem(user_id=user_2.id, beer_id=beer_5.id, quantity=5)

            # Associate beers with users via association table
            user_1.beers.append(beer_1)
            user_1.beers.append(beer_2)
            user_2.beers.append(beer_3)
            user_2.beers.append(beer_5)

            # Add new objects to the session
            session.add(beer_1)
            session.add(beer_2)
            session.add(beer_3)
            session.add(beer_4)
            session.add(beer_5)
            session.add(beer_6)
            session.add(beer_7)
            session.add(beer_8)

            session.add(user_1)
            session.add(user_2)
            session.add(user_3)
            session.add(admin_1)

            session.add(cart_item_1)
            session.add(cart_item_2)
            session.add(cart_item_3)
            session.add(cart_item_4)            

            # Commit the session to save data to the database
            session.commit()
