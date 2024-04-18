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

from app.models.models import Users, Books, Admins, association_table

def create_database():
    Base.metadata.create_all(engine)

def delete_database():
    Base.metadata.clear()

def vider_db():
    session = Session()
    try:
        # Pour chaque table, vous exécutez un delete()
        session.query(Users).delete()
        session.query(Books).delete()
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
            book_1 = Books(id = str(uuid4()), name="Animagus", Author="Alice", Editor = "John Doe", price= 10.0, bought = False)
            book_2 = Books(id = str(uuid4()), name="Les misérables", Author="Victor Hugo", Editor = "Marc Doe", price= 15.0, bought = False)
            book_3 = Books(id = str(uuid4()), name="The Hobbit", Author="J.R.R. Tolkien", Editor = "Bob Doe", price= 20.0, bought = False)

            password_1="Admin!123"
            password_2 = "Password!123"
            encoded_password = password_1.encode()
            hashed_password = hashlib.sha3_256(encoded_password).hexdigest()

            encoded_password = password_2.encode()
            hashed_password_2 = hashlib.sha3_256(encoded_password).hexdigest()
            user_1 = Users(id= str(uuid4()),username= "admin", name= "admin", surname= "admin", password= hashed_password, email= "admin@juice-sh.op", group= "admin", whitelist= True)
            user_2 = Users(id= str(uuid4()),username= "User2", name= "Doe", surname= "John", password= hashed_password_2, email= "test@gmail.com", group= "client", whitelist= True)

            admin_1 = Admins(id=1, user_id=user_1.id)

            user_1.book.append(book_1)
            user_1.book.append(book_2)
            user_2.book.append(book_3)
            
            # Ajouter les nouveaux objets à la session
            session.add(book_1)
            session.add(book_2)
            session.add(book_3)

            session.add(user_1)
            session.add(user_2)

            session.add(admin_1)
            
            # Commit la session pour sauvegarder les données dans la base de données
            session.commit()


'''database = {
    "books": [
        {
            "id": str(uuid4()),
            "name": "Animagus",
            "Author": "Alice",
            "Editor": "John Doe"
        },
        {
            "id": str(uuid4()),
            "name": "Les misérables",
            "Author": "Victor Hugo",
            "Editor": "Marc Doe"
        },
        {
            "id": str(uuid4()),
            "name": "The Hobbit",
            "Author": "J.R.R. Tolkien",
            "Editor": "Bob Doe"
       
        },
    ],
    "users" : [

        {
            "id": str(uuid4()),
            "username": "admin",
            "name": "admin",
            "surname": "admin",
            "password": "Admin!123",
            "email": "admin@juice-sh.op",
            "group": "admin",
            "whitelist": True
        },
        {
            "id": str(uuid4()),
            "username": "User2",
            "name": "John",
            "surname": "Doe",
            "password": "Test123!",
            "email": "test@gmail.com",
            "group": "client",
            "whitelist": True
        }

    ]

}
'''


