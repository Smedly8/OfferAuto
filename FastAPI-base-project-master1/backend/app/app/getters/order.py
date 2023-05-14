from app.getters.universal import transform
from app.models import Order
from app.schemas import GettingOrder
from app.getters.user import get_user

def get_order(order: Order) -> GettingOrder:
    # return transform(db_obj=order, target_schema=GettingOrder, user=get_user(order.user) if order.user is not None else None)
    return transform(db_obj=order, target_schema=GettingOrder)