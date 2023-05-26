from typing import Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.order import Order
from app.schemas.order import CreatingOrder, UpdatingOrder


class CRUDCountry(CRUDBase[Order, CreatingOrder, UpdatingOrder]):
    def get_by_user_id(self, db: Session, *, user_id: str) -> Order | None:
        return db.query(self.model).filter(self.model.user_id == user_id).all()


order = CRUDCountry(Order)
