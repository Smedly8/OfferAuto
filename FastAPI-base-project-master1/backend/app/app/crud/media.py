import os
import uuid
from typing import TypeVar, Generic, Type
from botocore.client import BaseClient
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.crud.base import ModelType

ModelAttachmentType = TypeVar("ModelAttachmentType", bound="BaseModel")


class MixinContent:
    _content_column: str | None = None
    s3_bucket_name: str | None = None
    s3_client: BaseClient | None = None

    def __init__(self, model: Type[ModelType]):
        self.model = model

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


class MixinAttachment(Generic[ModelType, ModelAttachmentType]):
    _attachment_column: str | None = None
    _attachment_foreign_key: str | None = None
    s3_bucket_name: str | None = None
    s3_client: BaseClient | None = None

    def __init__(self, model: Type[ModelType], model_attachment: Type[ModelAttachmentType]):
        self.model = model
        self.model_attachment = model_attachment

    def add_attachment(
            self,
            db: Session,
            *,
            attachment: UploadFile,
            obj: ModelType | None = None,
            content_path: str | None = None,
            attachment_column: str | None = _attachment_column,
            attachment_foreign_key: str | None = _attachment_foreign_key
    ) -> ModelAttachmentType | None:
        if attachment_column is None:
            return None
        host = self.s3_client._endpoint.host

        bucket_name = self.s3_bucket_name

        url_prefix = host + '/' + bucket_name + '/'

        if content_path is None:
            content_path = self.model.__name__.lower() + '/' + attachment_column + '/'
        name = content_path + uuid.uuid4().hex + \
               os.path.splitext(attachment.filename)[1]

        result = self.s3_client.put_object(
            Bucket=bucket_name,
            Key=name,
            Body=attachment.file,
            ContentType=attachment.content_type
        )
        url = url_prefix + name
        if not (200 <= result.get('ResponseMetadata', {}).get('HTTPStatusCode', 500) < 300):
            return None

        attachment = self.model_attachment()

        if attachment_foreign_key is not None or obj is not None:
            setattr(attachment, attachment_foreign_key, obj.id)
        setattr(attachment, attachment_column, url)
        db.add(attachment)
        db.commit()
        db.refresh(attachment)

        return attachment

    def get_attachment(
            self,
            db: Session,
            *,
            attachment_id: int
    ) -> ModelAttachmentType | None:
        attachment = db.query(self.model) \
            .get(attachment_id)
        return attachment

    def delete_attachment(
            self,
            db: Session,
            *,
            attachment: ModelAttachmentType
    ) -> None:
        db.delete(attachment)
        db.commit()