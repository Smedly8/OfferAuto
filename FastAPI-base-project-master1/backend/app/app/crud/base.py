import logging
import os
import uuid
from typing import Any, Generic, Type, TypeVar

from app.models.base_model import BaseModel
from app.schemas.base import BaseSchema
from app.schemas.response import Paginator
from app.utils import pagination
from botocore.client import BaseClient
from fastapi import UploadFile
from sqlalchemy import inspect, orm
from sqlalchemy.orm import Session

ModelType = TypeVar('ModelType', bound=BaseModel)
CreatingSchemaType = TypeVar('CreatingSchemaType', bound=BaseSchema)
UpdatingSchemaType = TypeVar('UpdatingSchemaType', bound=BaseSchema)


class CRUDBase(Generic[ModelType, CreatingSchemaType, UpdatingSchemaType]):

    _content_column: str | None = None
    s3_bucket_name: str | None = None
    s3_client: BaseClient | None = None

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> ModelType | None:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_many(self, db: Session, ids: list[Any]) -> list[ModelType]:
        return db.query(self.model).filter(self.model.id.in_(ids)).all()

    def _filters(self, query: orm.Query, filters: dict[str, Any]) -> orm.Query:
        empty_filters = {}
        simple_filters = {}
        custom_filters = {}

        for name, value in filters.items():
            if value is None:
                empty_filters[name] = value
                continue
            model_info = inspect(self.model)
            if name in model_info.columns.keys() + model_info.relationships.keys():
                simple_filters[name] = value
            else:
                custom_filters[name] = value

        if len(simple_filters.keys()) > 0:
            logging.info(f'{simple_filters=}')
            query = query.filter_by(**simple_filters)
        return query

    def get_page(
            self,
            db: Session,
            order_by: Any | None = None,
            page: int | None = None,
            size: int = 30,
            **filers
    ) -> tuple[list[ModelType], Paginator]:
        query = db.query(self.model)
        if order_by is None:
            if hasattr(self.model, 'id'):
                query = query.order_by(self.model.id)
        else:
            query = query.order_by(order_by)
        query = self._filters(query, filers)
        return pagination.get_page(query, page, size=size)

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 30, order_by: Any | None = None, **filters
    ) -> list[ModelType]:
        query = db.query(self.model)
        if order_by is None:
            if hasattr(self.model, 'id'):
                query = query.order_by(self.model.id)
        else:
            query = query.order_by(order_by)
        query = query.offset(skip).limit(limit)
        query = self._filters(query, filters)
        return query.all()

    def _adapt_fields(self, obj: dict[str, Any] | BaseSchema, **kwargs) -> dict[str, Any]:
        if isinstance(obj, dict):
            data = obj
        else:
            data = obj.dict(exclude_unset=True)
        data.update(**kwargs)
        return data

    def _set_db_obj_fields(self, db_obj, fields):
        info = inspect(self.model)
        for field in info.columns.keys() + info.relationships.keys():
            if field in fields:
                setattr(db_obj, field, fields[field])
        return db_obj

    def create(self, db: Session, *, obj_in: CreatingSchemaType | dict[str, Any], **kwargs) -> ModelType:
        db_obj = self.model()
        fields = self._adapt_fields(obj_in, **kwargs)
        print(fields)
        db_obj = self._set_db_obj_fields(db_obj=db_obj, fields=fields)
        print('====================== ', db_obj)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdatingSchemaType | dict[str, Any],
        **kwargs
    ) -> ModelType:
        fields = self._adapt_fields(obj_in, **kwargs)
        db_obj = self._set_db_obj_fields(db_obj=db_obj, fields=fields)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def _remove(self, db: Session, *, obj: ModelType | None) -> ModelType | None:
        if obj is not None:
            db.delete(obj)
            return obj
        return None

    def remove_obj(self, db: Session, *, obj: ModelType | None):
        self._remove(db=db, obj=obj)
        db.commit()
        return None

    def remove_by_id(self, db: Session, *, id: Any) -> ModelType | None:
        return self.remove_obj(db=db, obj=self.get(db=db, id=id))

    def remove_many_obj(self, db: Session, *, objs: list[ModelType]) -> list[ModelType]:
        results = []
        for obj in objs:
            result = self._remove(db=db, obj=obj)
            if result is not None:
                results.append(result)
        db.commit()
        return results

    def remove_many_by_ids(self, db: Session, *, ids: list[Any]) -> list[ModelType]:
        return self.remove_many_obj(db=db, objs=self.get_many(db=db, ids=ids))

    def change_content(
            self,
            db: Session,
            *,
            obj: ModelType | None = None,
            content: UploadFile | None = None,
            content_path: str | None = None,
            content_column: str | None = _content_column
    ) -> int:
        """Изменить контент сущности

        При  :doc:`content == None` удаляет контент

        Args:
            db (Session): Сессия БД
            obj (ModelType | None, optional): Объект бд. По умолчанию None.
            content (UploadFile | None, optional): Контент. По умолчанию None.
            content_path (str | None, optional): Путь к объекту в сервисе.
            content_column (str | None, optional): Название столбца. По умолчанию _content_column.

        Returns:
            int: 0 - Выполнено
                -1 - content_column не задан
                -2 - сервис не отвечает
        """
        if content_column is None:
            return -1

        old_content = getattr(obj, content_column, None)

        host = self.s3_client._endpoint.host
        bucket_name = self.s3_bucket_name
        url_prefix = host + '/' + bucket_name + '/'
        new_url = None

        if content is not None:
            if content_path is None:
                content_path = self.model.__name__.lower() + '/' + content_column + '/'

            name = content_path + uuid.uuid4().hex + \
                os.path.splitext(content.filename)[1]  # type: ignore
            new_url = url_prefix + name

            result = self.s3_client.put_object(
                Bucket=bucket_name,
                Key=name,
                Body=content.file,
                ContentType=content.content_type
            )
            if not (200 <= result.get('ResponseMetadata', {}).get('HTTPStatusCode', 500) < 300):
                return -2

        setattr(obj, content_column, new_url)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        if old_content is not None and old_content.startswith(url_prefix):
            key = old_content[len(url_prefix):]
            self.s3_client.delete_object(
                Bucket=bucket_name,
                Key=key
            )
        return 0
