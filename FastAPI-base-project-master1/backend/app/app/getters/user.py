from app.getters.universal import transform
from app.models import User
from app.schemas import GettingUser
from app.getters.order import get_order


def get_user(user: User) -> GettingUser:
    orders = [get_order(order) for order in user.orders]
    return transform(
        db_obj=user, 
        target_schema=GettingUser,
        orders=orders,
    )
