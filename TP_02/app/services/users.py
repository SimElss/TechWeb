from ..schemas.users import UserSchema
from ..models.models import Users, Admins
from pydantic import ValidationError
from ..database import Session
from sqlalchemy import select, update, delete, func



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
            return UserSchema(
                id=user.id,
                username=user.name,
                name=user.Author,
                surname=user.Editor,
                password=user.password,
                email=user.email,
                group=user.group,
                whitelist=user.whitelist,
            )
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
            return UserSchema(
                id=user.id,
                username=user.username,
                name=user.name,
                surname=user.surname,
                password=user.password,
                email=user.email,
                group=user.group,
                whitelist=user.whitelist,
            )
    return None


def add_user(user: UserSchema):
    """
    This function adds a new user.

    Parameters:
    -----------
    user : The user object to be added (Object UserSchema)
    """
    with Session() as session:
        user_entity = Users(
            id=user.id,
            username=user.username,
            name=user.name,
            surname=user.surname,
            password=user.password,
            email=user.email,
            group=user.group,
            whitelist=user.whitelist,
        )
        session.add(user_entity)#add user to database
        session.commit()


def get_all_users() -> list[UserSchema]:
    """
    This function retrieves all users.

    Returns:
    --------
    users_data : The list of all users (list of Object UserSchema)
    """
    with Session() as session:
        statement = select(Users) #Model Book
        users_data = session.scalars(statement).unique().all()
        #Schema UserSchema
        return [
            UserSchema(
                id=user.id,
                username=user.username,
                name=user.name,
                surname=user.surname,
                password=user.password,
                email=user.email,
                group=user.group,
                whitelist=user.whitelist,
            )
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
            admin = Session.scalars(statement)

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
        user = session.scalars(statement)

        #We update the witelist attribute of the user to the wanted value
        user.whitelist = whitelist

        session.commit()