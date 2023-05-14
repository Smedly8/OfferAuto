from app.getters.universal import transform
from app.models import Country
from app.schemas import GettingCountry


def get_country(country: Country) -> GettingCountry:
    return transform(db_obj=country, target_schema=GettingCountry)