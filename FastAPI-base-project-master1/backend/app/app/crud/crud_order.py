from typing import Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.order import Order
from app.schemas.order import CreatingOrder, UpdatingOrder


class CRUDCountry(CRUDBase[Order, CreatingOrder, UpdatingOrder]):
    pass

order = CRUDCountry(Order)
