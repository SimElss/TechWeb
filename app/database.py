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

from app.models.models import Base, Users, Beers, Admins, association_table

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
        session.query(Admins).delete()
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
            beer_1 = Beers(id = str(uuid4()), name="Lager", brewery="Brewery A", price= 3.5, stock = 100, description = "A smooth and crisp lager.")
            beer_2 = Beers(id = str(uuid4()), name="IPA", brewery="Brewery B", price= 4.2, stock = 50, description = "A hoppy and bitter IPA.")
            beer_3 = Beers(id = str(uuid4()), name="Stout", brewery="Brewery C", price= 5.0, stock = 30, description = "A rich and creamy stout.")
            beer_4 = Beers(id = str(uuid4()), name="Pilsner", brewery="Brewery D", price= 3.8, stock = 80, description = "A light and refreshing pilsner.")
            beer_5 = Beers(id = str(uuid4()), name="Wheat Beer", brewery="Brewery E", price= 4.5, stock = 50, description = "A fruity and spicy wheat beer.")

            password_1="Admin!123"
            password_2 = "Password!123"
            encoded_password = password_1.encode()
            hashed_password = hashlib.sha3_256(encoded_password).hexdigest()

            encoded_password = password_2.encode()
            hashed_password_2 = hashlib.sha3_256(encoded_password).hexdigest()
            user_1 = Users(id= str(uuid4()),username= "admin", name= "admin", surname= "admin", password= hashed_password, email= "admin@juice-sh.op", group= "admin", whitelist= True)
            user_2 = Users(id= str(uuid4()),username= "User2", name= "Doe", surname= "John", password= hashed_password_2, email= "user@gmail.com", group= "client", whitelist= True)

            admin_1 = Admins(id=1, user_id=user_1.id)

            user_1.beer.append(beer_1)
            user_1.beer.append(beer_2)
            user_2.beer.append(beer_3)
            
            # Ajouter les nouveaux objets à la session
            session.add(beer_1)
            session.add(beer_2)
            session.add(beer_3)
            session.add(beer_4)
            session.add(beer_5)

            session.add(user_1)
            session.add(user_2)

            session.add(admin_1)
            
            # Commit la session pour sauvegarder les données dans la base de données
            session.commit()