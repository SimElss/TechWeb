from ..database import database
from ..schemas.users import UserSchema
from pydantic import ValidationError
from fastapi import status


def get_user_by_username(username: str):
    for user in database['users']:
        if user['username'] == username:
            return UserSchema.model_validate(user)
    return None

def get_user_by_email(email: str):
    for user in database['users']:
        if user['email'] == email:
            return UserSchema.model_validate(user)
    return None

def get_user_by_id(id: str):
    for user in database['users']:
        if user['id'] == id:
            return UserSchema.model_validate(user)
    return None

def add_user(user: UserSchema):
    new_user = UserSchema.model_validate(user)
    database['users'].append(user)

def get_all_users() -> list[UserSchema]:
    users_data = database["users"]
    return users_data

def set_user_group(id: str, group: str):
    for user in database['users']:
        if user['id'] == id:
            user['group'] = group
            return
    return None

def set_user_whitelist(id: str, whitelist: bool):
    for user in database['users']:
        if user['id'] == id:
            user['whitelist'] = whitelist
            return
    return None