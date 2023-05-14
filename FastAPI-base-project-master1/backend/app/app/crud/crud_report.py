from typing import Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.report import Report
from app.schemas.report import CreatingReport, UpdatingReport


class CRUDReport(CRUDBase[Report, CreatingReport, UpdatingReport]):
    def get_by_order_id(self, db: Session, *, order_id: str) -> Report | None:
        return db.query(self.model).filter(self.model.order_id == order_id).all()

report = CRUDReport(Report)
