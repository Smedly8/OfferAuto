from app.schemas.base import BaseSchema

# Shared properties


class BaseReport(BaseSchema):
    description: str | None = None
    order_id: int


# Properties to receive via API on creation
class CreatingReport(BaseReport):
    pass


# Properties to receive via API on update
class UpdatingReport(BaseReport):
    description: str | None = None
    order_id: int | None


class GettingReport(BaseReport):
    id: int | None = None
    created: int | None = None
    img: str | None = None
    # user: GettingUser | None = None
