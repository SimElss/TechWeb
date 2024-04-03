from ..database import database
from ..schemas.users import UserSchema
from pydantic import ValidationError
from fastapi import status


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
    for user in database['users']:
        if user['email'] == email:
            return UserSchema.model_validate(user)
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
    for user in database['users']:
        if user['id'] == id:
            return UserSchema.model_validate(user)
    return None


def add_user(user: UserSchema):
    """
    This function adds a new user.

    Parameters:
    -----------
    user : The user object to be added (Object UserSchema)
    """
    new_user = UserSchema.model_validate(user)
    database['users'].append(user)


def get_all_users() -> list[UserSchema]:
    """
    This function retrieves all users.

    Returns:
    --------
    users_data : The list of all users (list of Object UserSchema)
    """
    users_data = database["users"]
    return users_data


def set_user_group(id: str, group: str):
    """
    This function sets the group of a user.

    Parameters:
    -----------
    id : The ID of the user (str)
    group : The group to be assigned to the user (str)
    """
    for user in database['users']:
        if user['id'] == id:
            user['group'] = group
            return
    return None


def set_user_whitelist(id: str, whitelist: bool):
    """
    This function sets the whitelist status of a user.

    Parameters:
    -----------
    id : The ID of the user (str)
    whitelist : The whitelist status to be set (bool)
    """
    for user in database['users']:
        if user['id'] == id:
            user['whitelist'] = whitelist
            return
    return None
