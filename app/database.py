from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from uuid import uuid4
import hashlib

engine = create_engine(
    "sqlite:///data/db.sqlite",  # Path to the database file
    echo=False,  # Show generated SQL code in the terminal
)
Session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass

from app.models.models import Base, Users, Beers, Admins, association_table, CartItem, Order, OrderItem

def create_database():
    Base.metadata.create_all(engine)

def delete_database():
    Base.metadata.clear()

def vider_db():
    session = Session()
    try:
        # Pour chaque table, vous exécutez un delete()
        session.query(Users).delete()
        session.query(Beers).delete()
        session.query(Admins).delete()
        session.query(CartItem).delete()
        session.query(Order).delete()
        session.query(OrderItem).delete()
        session.query(association_table).delete()
        # Ajoutez des lignes similaires pour d'autres tables si nécessaire
        
        session.commit()
    except Exception as e:
        print(f"Erreur lors de la vidange de la base de données: {e}")
        session.rollback()
    finally:
        session.close()

def initialiser_db():
    with Session() as session:
        # Vérifie si la table est déjà peuplée
        if session.query(Users).count() == 0:
            # Créer des instances de vos modèles
            beer_1 = Beers(id=str(uuid4()), name="Quantum Ale", brewery="Schrödinger's Brewery", price=4.7, stock=75, description="Une bière légère et rafraîchissante infusée avec des agrumes et une touche de mystère quantique. Chaque gorgée est une expérience unique.", image="./static/quantum_ale.jpg")
            beer_2 = Beers(id=str(uuid4()), name="Pixel Pils", brewery="Retro Brew Co.", price=3.9, stock=100, description="Revivez l'ère des jeux rétro avec cette pilsner croustillante et claire. Parfaite pour accompagner une soirée de jeux vidéo classique.", image="./static/pixel_pils.jpg")
            beer_3 = Beers(id=str(uuid4()), name="Hops of Hyrule", brewery="Triforce Brewery", price=5.3, stock=60, description="Une IPA audacieuse et aventureuse, brassée avec des houblons rares des terres d'Hyrule. Parfaite pour les héros en quête d'une bière épique.", image="./static/hops_of_hyrule.jpg")
            beer_4 = Beers(id=str(uuid4()), name="Stark Stout", brewery="Iron Craft Brewery", price=5.5, stock=40, description="Un stout riche et robuste avec des notes de café et de chocolat noir. Aussi puissant que l'armure d'un certain homme de fer.", image="./static/stark_stout.jpg")
            beer_5 = Beers(id=str(uuid4()), name="Warp Speed Wheat", brewery="Starfleet Brewery", price=4.8, stock=85, description="Une bière de blé douce et épicée, brassée pour les explorateurs de l'espace. Une gorgée et vous serez propulsé à la vitesse de la lumière.", image="./static/warp_speed_wheat.jpg")
            beer_6 = Beers(id=str(uuid4()), name="Dragonfire Doppelbock", brewery="Dragon's Den Brewery", price=6.0, stock=50, description="Une doppelbock riche et maltée, infusée avec des épices de feu. Parfaite pour les aventuriers et les amateurs de dragons.", image="./static/dragonfire_doppelbock.jpg")
            beer_7 = Beers(id=str(uuid4()), name="Galactic Porter", brewery="Nebula Brewing Co.", price=5.2, stock=70, description="Un porter sombre et mystérieux avec des notes de caramel et de cacao. Embarquez pour un voyage interstellaire avec chaque gorgée.", image="./static/galactic_porter.jpg")
            beer_8 = Beers(id=str(uuid4()), name="Mana Potion Ale", brewery="Arcane Brewmasters", price=4.9, stock=90, description="Une ale magique et énergisante, brassée avec des herbes secrètes et des essences mystiques. Rechargez votre mana avec cette potion délicieuse.", image="./static/mana_potion_ale.jpg")

            password_1 = "Admin!123"
            password_2 = "Password!123"
            encoded_password_1 = password_1.encode()
            hashed_password_1 = hashlib.sha3_256(encoded_password_1).hexdigest()

            encoded_password_2 = password_2.encode()
            hashed_password_2 = hashlib.sha3_256(encoded_password_2).hexdigest()
            user_1 = Users(id=str(uuid4()), username="admin", name="admin", surname="admin", password=hashed_password_1, email="admin@juice-sh.op", group="admin", whitelist=True)
            user_2 = Users(id=str(uuid4()), username="User2", name="Doe", surname="John", password=hashed_password_2, email="user@gmail.com", group="client", whitelist=True)

            admin_1 = Admins(id=1, user_id=user_1.id)
            # Associez les bières aux utilisateurs via le panier
            cart_item_1 = CartItem(user_id=user_1.id, beer_id=beer_1.id, quantity=7)
            cart_item_2 = CartItem(user_id=user_1.id, beer_id=beer_2.id, quantity=1)
            cart_item_3 = CartItem(user_id=user_2.id, beer_id=beer_3.id, quantity=2)
            cart_item_4 = CartItem(user_id=user_2.id, beer_id=beer_5.id, quantity=5)

            # Associez les bières aux utilisateurs via le panier
            user_1.beers.append(beer_1)
            user_1.beers.append(beer_2)
            user_2.beers.append(beer_3)
            user_2.beers.append(beer_5)

            # Ajouter les nouveaux objets à la session
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
            session.add(admin_1)

            session.add(cart_item_1)
            session.add(cart_item_2)
            session.add(cart_item_3)
            session.add(cart_item_4)            
            # Commit la session pour sauvegarder les données dans la base de données
            session.commit()
