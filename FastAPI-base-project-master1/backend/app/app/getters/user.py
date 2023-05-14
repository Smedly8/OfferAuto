from app.getters.universal import transform
from app.models import User
from app.schemas import GettingUser


def get_user(user: User) -> GettingUser:
    return transform(db_obj=user, target_schema=GettingUser)
