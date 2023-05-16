from typing import Any, Type

from sqlalchemy.orm import Session

from app import deps
from app.crud.base import CRUDBase
from app.models.report import Report
from app.schemas.report import CreatingReport, UpdatingReport
from app.crud.media import MixinContent


class CRUDReport(CRUDBase[Report, CreatingReport, UpdatingReport], MixinContent):

    def __init__(self, model: Type[Report],  bucket_name: str | None = None, s3_client=None):
        self.model = model
        self.s3_bucket_name = bucket_name if bucket_name is not None else deps.get_bucket_name()
        self.s3_client = s3_client if s3_client is not None else deps.get_s3_client()

    def get_by_order_id(self, db: Session, *, order_id: str) -> Report | None:
        return db.query(self.model).filter(self.model.order_id == order_id).all()


report = CRUDReport(Report)
