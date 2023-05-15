from typing import Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import CreatingUser, UpdatingUser, ExistsRequest, ExistsResponse
from app.utils.security import get_password_hash, verify_password


class CRUDUser(CRUDBase[User, CreatingUser, UpdatingUser]):
    def get_by_email(self, db: Session, *, email: str) -> User | None:
        return db.query(self.model).filter(self.model.email == email).first()

    def create(self, db: Session, *, obj_in: CreatingUser | dict[str, Any], **kwargs) -> User:
        fields = self._adapt_fields(obj_in, **kwargs)
        fields['email'] = fields['email'].lower() if isinstance(
            fields['email'], str) else fields['email']
        fields['hashed_password'] = get_password_hash(fields.pop('password'))
        return super(CRUDUser, self).create(db=db, obj_in=fields)

    def update(
        self, db: Session, *, db_obj: User, obj_in: UpdatingUser | dict[str, Any], **kwargs
    ) -> User:
        fields = self._adapt_fields(obj_in, **kwargs)
        if 'email' in fields:
            fields['email'] = fields['email'].lower() if isinstance(
                fields['email'], str) else fields['email']
        if 'password' in fields:
            fields['hashed_password'] = get_password_hash(
                fields.pop('password'))
        return super().update(db, db_obj=db_obj, obj_in=fields)

    def authenticate(self, db: Session, *, email: str, password: str) -> User | None:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def exists(self, db: Session, *, data: ExistsRequest) -> ExistsResponse:
        return ExistsResponse(
            exists=db.query(self.model)
            .filter_by(**data.dict(exclude_unset=True, exclude_none=True))
            .first() is not None
        )


user = CRUDUser(User)
