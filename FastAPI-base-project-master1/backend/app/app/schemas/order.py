from app.schemas.base import BaseSchema
from app.schemas.user import GettingUser

# Shared properties
class BaseOrder(BaseSchema):
    name: str | None = None
    description: str | None = None
    user_id: int 


# Properties to receive via API on creation
class CreatingOrder(BaseOrder):
    pass


# Properties to receive via API on update
class UpdatingOrder(BaseOrder):
    user_id: int | None = None


class GettingOrder(BaseOrder):
    id: int | None = None
    # user: GettingUser | None = None

