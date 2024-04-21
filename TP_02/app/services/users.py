from pydantic import ValidationError
from sqlalchemy import select
import hashlib

from ..schemas.users import UserSchema, AdminSchema
from ..database import Session
from ..models.models import Users, Admins, Books, association_table
from ..errors import ChangeMdpError



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
    #We encode the password using sha3_256
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
        session.add(user_entity)#add user to database
        session.commit()

def add_admin(admin: AdminSchema):
    with Session() as session:
        admin_entity = Admins(
            id = admin.id,
            user_id = admin.user_id
        )

        session.add(admin_entity)
        session.commit()

def get_all_users() -> list[Users]:
    """
    This function retrieves all users.

    Returns:
    --------
    users_data : The list of all users (list of Object Users)
    """
    with Session() as session:
        statement = select(Users) #Model Book
        users_data = session.scalars(statement).unique().all()
        #Schema UserSchema
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
            #We add user in Admin table
            admin= Admins(
                user_id=id,
            )
            
            session.add(admin)
            session.commit()

        else:
            #We remove user from Admin table
            statement = select(Admins).filter_by(user_id=id)
            admin = session.scalar(statement)

            session.delete(admin)
            session.commit()

        #We alse update group attribute in User table 
        statement = select(Users).filter_by(id=id)
        user = session.scalar(statement)

        user.group=group
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

        #We update the witelist attribute of the user to the wanted value
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

        new_user= {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "surname": user.surname,
            "password": password,
            "email": user.email,
            "group": user.group,
            "whitelist": user.whitelist
        }

        #We check if the new password has a valid format
        try:
            new_user = UserSchema.model_validate(new_user)
        except ValidationError as e:
            raise ChangeMdpError(e.errors()[0]['msg'])

        #We encode the password using sha3_256
        encoded_password = password.encode()
        hashed_password = hashlib.sha3_256(encoded_password).hexdigest()

        #We update the password attribute of the user to the wanted value
        user.password = hashed_password

        session.commit()

def modifify_user_profile(id:str, name:str, surname:str, username:str):
    """
    This function modifies the profile of a user.

    Parameters:
    -----------
    id : The ID of the user (str)
    email : The new email (str)
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

        #We update the attributes of the user to the wanted values
        user.username = username
        user.name = name
        user.surname = surname

        session.commit()

        new_user = session.scalar(statement)
        return new_user
    
def get_book_owners():
    """
    This function retrieves a user by book ID.

    Parameters:
    -----------
    book_id : The ID of the book (str)

    Returns:
    --------
    UserSchema.model_validate(user) : The user object if found (Object UserSchema)
    None : If no user is found (NoneTypeObject)
    """
    with Session() as session:
        book_with_owners = (
        session.query(Books, Users)
        .select_from(Books)
        .join(association_table, Books.id == association_table.c.book_id)
        .join(Users, Users.id == association_table.c.user_id)
        .all()
    )
    print(book_with_owners)

    return book_with_owners
    
def get_user_by_book(book_id:str):
    """
    This function retrieves a user by book ID.

    Parameters:
    -----------
    book_id : The ID of the book (str)

    Returns:
    --------
    UserSchema.model_validate(user) : The user object if found (Object UserSchema)
    None : If no user is found (NoneTypeObject)
    """
    with Session() as session:
        statement = select(Books).filter_by(id= book_id)
        book = session.scalar(statement) 
        
        
        user = book.user

        if user is not None:
            return user[0]
    return None