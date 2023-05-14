from typing import Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.country import Country
from app.schemas.country import CreatingCountry, UpdatingCountry

class CRUDCountry(CRUDBase[Country, CreatingCountry, UpdatingCountry]):
    pass

country = CRUDCountry(Country)