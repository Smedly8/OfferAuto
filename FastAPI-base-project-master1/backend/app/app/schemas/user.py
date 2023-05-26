from app.schemas.base import BaseSchema
from app.schemas.order import GettingOrder

# Shared properties
class BaseUser(BaseSchema):
    email: str | None = None
    is_active: bool | None = True
    is_superuser: bool = False
    full_name: str | None = None
    vin: str | None = None
    phone: int | None = None


# Properties to receive via API on creation
class CreatingUser(BaseUser):
    email: str
    password: str
    


# Properties to receive via API on update
class UpdatingUser(BaseUser):
    password: str | None = None


class GettingUser(BaseUser):
    id: int | None = None
    orders: list[GettingOrder] = []


class LoginData(BaseSchema):
    email: str
    password: str


class TokenWithUser(BaseSchema):
    user: GettingUser
    token: str


class ExistsRequest(BaseSchema):
    email: str | None


class ExistsResponse(BaseSchema):
    exists: bool

class SigningUser(BaseSchema):
    email: str
    password: str