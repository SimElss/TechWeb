from pydantic import ValidationError
from sqlalchemy import select
import hashlib

from ..schemas.users import UserSchema, AdminSchema
from ..database import Session
from ..models.models import Users, Admins, Beers, association_table, CartItem
from ..errors import ChangeMdpError

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_confirmation_email(to_email: str):
    """
    This function sends a confirmation email to the user.

    Parameters:
    -----------
    to_email : The recipient's email address (str)
    """
    # Configuration des informations de connexion au serveur SMTP
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    sender_email = "buybeer3@outlook.fr"
    sender_password = "Buybeer!123"

    # Création du message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Confirmation de votre commande"
    message["From"] = sender_email
    message["To"] = to_email

    # Texte du message
    text = """\
    Bonjour,
    Merci pour votre commande. Votre commande a été confirmée.
    Cordialement,
    L'équipe de notre boutique
    """

    # Ajout du texte au message
    part = MIMEText(text, "plain")
    message.attach(part)

    try:
        # Connexion au serveur SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Utiliser TLS pour la sécurité
        server.login(sender_email, sender_password)

        # Envoi de l'e-mail
        server.sendmail(sender_email, to_email, message.as_string())

        # Fermeture de la connexion au serveur SMTP
        server.quit()

        print("E-mail envoyé avec succès")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")

def get_user_by_email(email: str):
    """
    This function retrieves a user by email.

    Parameters:
    -----------
    email : The email of the user (str)

    Returns:
    --------
    UserSchema.model_validate(user) : The user object if found (Object UserSchema)
    None : If no user is found (NoneTypeObject)
    """
    with Session() as session:
        statement = select(Users).filter_by(email=email)
        user = session.scalar(statement) 
        if user is not None:
            return user
    return None

def get_user_by_id(id: str):
    """
    This function retrieves a user by ID.

    Parameters:
    -----------
    id : The ID of the user (str)

    Returns:
    --------
    UserSchema.model_validate(user) : The user object if found (Object UserSchema)
    None : If no user is found (NoneTypeObject)
    """
    with Session() as session:
        statement = select(Users).filter_by(id=id)
        user = session.scalar(statement) 
        if user is not None:
            return user
    return None

def add_user(user: UserSchema):
    """
    This function adds a new user.

    Parameters:
    -----------
    user : The user object to be added (UserSchema Object)
    """
    # We encode the password using sha3_256
    encoded_password = user.password.encode()
    hashed_password = hashlib.sha3_256(encoded_password).hexdigest()
    with Session() as session:
        user_entity = Users(
            id=user.id,
            username=user.username,
            name=user.name,
            surname=user.surname,
            password=hashed_password,
            email=user.email,
            group=user.group,
            whitelist=user.whitelist,
        )
        session.add(user_entity)  # Add user to database
        session.commit()

def add_admin(admin: AdminSchema):
    """
    This function adds a new admin.

    Parameters:
    -----------
    admin : The admin object to be added (AdminSchema Object)
    """
    with Session() as session:
        admin_entity = Admins(
            id=admin.id,
            user_id=admin.user_id
        )
        session.add(admin_entity)  # Add admin to database
        session.commit()

def get_all_users() -> list[Users]:
    """
    This function retrieves all users.

    Returns:
    --------
    users_data : The list of all users (list of Object Users)
    """
    with Session() as session:
        statement = select(Users)  # Model beer
        users_data = session.scalars(statement).unique().all()
        # Schema UserSchema
        return [
            user
            for user in users_data
        ]

def set_user_group(id: str, group: str):
    """
    This function sets the group of a user.

    Parameters:
    -----------
    id : The ID of the user (str)
    group : The group to be assigned to the user (str)
    """
    with Session() as session:
        if group == "admin":
            # We add user in Admin table
            admin = Admins(
                user_id=id,
            )
            session.add(admin)
            session.commit()
        else:
            # We remove user from Admin table
            statement = select(Admins).filter_by(user_id=id)
            admin = session.scalar(statement)
            session.delete(admin)
            session.commit()

        # We also update group attribute in User table
        statement = select(Users).filter_by(id=id)
        user = session.scalar(statement)
        user.group = group
        session.commit()

def set_user_whitelist(id: str, whitelist: bool):
    """
    This function sets the whitelist status of a user.

    Parameters:
    -----------
    id : The ID of the user (str)
    whitelist : The whitelist status to be set (bool)
    """
    with Session() as session:
        statement = select(Users).filter_by(id=id)
        user = session.scalar(statement)
        # We update the whitelist attribute of the user to the wanted value
        user.whitelist = whitelist
        session.commit()

def change_user_password(id: str, password: str):
    """
    This function changes the password of a user.

    Parameters:
    -----------
    id : The ID of the user (str)
    password : The new password (str)
    """
    with Session() as session:
        statement = select(Users).filter_by(id=id)
        user = session.scalar(statement)
        new_user = {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "surname": user.surname,
            "password": password,
            "email": user.email,
            "group": user.group,
            "whitelist": user.whitelist
        }
        # We check if the new password has a valid format
        try:
            new_user = UserSchema.model_validate(new_user)
        except ValidationError as e:
            raise ChangeMdpError(e.errors()[0]['msg'])

        # We encode the password using sha3_256
        encoded_password = password.encode()
        hashed_password = hashlib.sha3_256(encoded_password).hexdigest()

        # We update the password attribute of the user to the wanted value
        user.password = hashed_password
        session.commit()

def modifify_user_profile(id: str, name: str, surname: str, username: str):
    """
    This function modifies the profile of a user.

    Parameters:
    -----------
    id : The ID of the user (str)
    name : The new name (str)
    surname : The new surname (str)
    username : The new username (str)

    Returns:
    --------
    new_user : The user object if found (Object Users model)
    None : If no user is found (NoneTypeObject)
    """
    name = name.strip(' ')
    name = name.strip('\t')
    surname = surname.strip(' ')
    surname = surname.strip('\t')
    username = username.strip(' ')
    username = username.strip('\t')

    if name == "" or surname == "" or username == "":
        return None

    with Session() as session:
        statement = select(Users).filter_by(id=id)
        user = session.scalar(statement)
        # We update the attributes of the user to the wanted values
        user.username = username
        user.name = name
        user.surname = surname
        session.commit()
        new_user = session.scalar(statement)
        return new_user

def drop_beer_panier(beer_id: str, user_id: str):
    """
    This function removes a beer from the user's cart.

    Parameters:
    -----------
    beer_id : str
        The ID of the beer.
    user_id : str
        The ID of the user.

    Returns:
    --------
    bool
        True if the operation was successful, False otherwise.
    """
    with Session() as session:
        try:
            # Fetch the CartItem to be removed
            statement = select(CartItem).filter_by(beer_id=beer_id, user_id=user_id)
            cart_item = session.scalar(statement)
            if cart_item:
                session.delete(cart_item)
                session.commit()
                return True
            else:
                print(f"No cart item found for beer_id={beer_id} and user_id={user_id}")
                return False
        except Exception as e:
            print(f"Error removing beer from cart: {e}")
            session.rollback()
            return False