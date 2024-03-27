from fastapi_login import LoginManager
from datetime import timedelta

from app.services.users import get_user_by_id


SECRET = "SECRET"
login_manager = LoginManager(SECRET, '/login', use_cookie=True, default_expiry=timedelta(seconds = 10))
login_manager.cookie_name = "auth_cookie"


@login_manager.user_loader()
def query_user(user_id: str):
    return get_user_by_id(user_id)