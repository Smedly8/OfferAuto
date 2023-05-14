from fastapi import APIRouter, Query, Depends, Path
from sqlalchemy.orm import Session

from app import crud, schemas, getters, deps, models
from app.exceptions import UnfoundEntity
from app.utils.response import get_responses_description_by_codes

router = APIRouter()


@router.get(
    '/cp/countries/',
    tags=["Панель Управления / Страны"],
    name="Получить все страны",
    response_model=schemas.response.ListOfEntityResponse[schemas.country.GettingCountry],
    responses=get_responses_description_by_codes([400])
)
@router.get(
    '/countries/',
    tags=["Страны"],
    name="Получить все страны",
    response_model=schemas.response.ListOfEntityResponse[schemas.country.GettingCountry],
    responses=get_responses_description_by_codes([400])
)
def get_all_countries(
        db: Session = Depends(deps.get_db),
        page: int | None = Query(None)
):
    data, paginator = crud.crud_country.country.get_page(db=db, page=page)

    return schemas.response.ListOfEntityResponse(
        data=[
            getters.country.get_country(country=country)
            for country in data
        ],
        meta=schemas.response.Meta(paginator=paginator)
    )

@router.post(
    '/cp/countries/',
    tags=["Панель Управления / Страны"],
    name="создать страну",
    response_model=schemas.response.SingleEntityResponse[schemas.country.GettingCountry],
    responses=get_responses_description_by_codes([401, 403, 400]),
)
def create_country(
        data: schemas.country.CreatingCountry,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_superuser),
):
    country = crud.crud_country.country.create(db=db, obj_in=data)

    return schemas.response.SingleEntityResponse(
        data=getters.country.get_country(country=country)
    )




@router.delete(
    '/cp/countries/{country_id}/',
    tags=["Панель Управления / Страны"],
    name="удалить страну",
    response_model=schemas.response.OkResponse,
    responses=get_responses_description_by_codes([401, 403])
)
def delete_country(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_superuser),
        country_id: int = Path(...),
):

    crud.crud_country.country.remove_by_id(db=db, id=country_id)

    return schemas.response.OkResponse()

@router.put(
    '/cp/countries/{country_id}/',
    tags=["Панель Управления / Страны"],
    name="изменить страну",
    response_model=schemas.response.SingleEntityResponse[schemas.country.GettingCountry],
    responses=get_responses_description_by_codes([401, 403, 400, 404])
)
def edit_country(
        data: schemas.country.UpdatingCountry,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_superuser),
        country_id: int = Path(...),
):
    country = crud.crud_country.country.get(db=db, id=country_id)
    if country is None:
        raise UnfoundEntity(message="Страна не найдена", num=1)

    country = crud.crud_country.country.update(db=db, db_obj=country, obj_in=data)

    return schemas.response.SingleEntityResponse(
        data=getters.country.get_country(country=country)
    )











