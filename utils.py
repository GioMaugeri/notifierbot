from config import AUTHORIZED_USERS

def is_authorized(user_id: int) -> bool:
    return user_id in AUTHORIZED_USERS