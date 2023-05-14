from app.schemas.base import BaseSchema


# Shared properties
class BaseCountry(BaseSchema):
    name: str


# Properties to receive via API on creation
class CreatingCountry(BaseCountry):
    pass


# Properties to receive via API on update
class UpdatingCountry(BaseCountry):
    pass


class GettingCountry(BaseCountry):
    id: int | None = None

