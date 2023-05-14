from fastapi import APIRouter, Query, Depends, Path
from sqlalchemy.orm import Session

from app import crud, schemas, getters, deps, models
from app.exceptions import UnfoundEntity
from app.utils.response import get_responses_description_by_codes

router = APIRouter()


@router.get(
    '/cp/orders/',
    tags=["Панель Управления / Заказы"],
    name="Получить все заказы",
    response_model=schemas.response.ListOfEntityResponse[schemas.order.GettingOrder],
    responses=get_responses_description_by_codes([400])
)
@router.get(
    '/orders/',
    tags=["Заказы"],
    name="Получить все Заказы",
    response_model=schemas.response.ListOfEntityResponse[schemas.order.GettingOrder],
    responses=get_responses_description_by_codes([400])
)
def get_all(
        db: Session = Depends(deps.get_db),
        page: int | None = Query(None)
):
    data, paginator = crud.crud_order.order.get_page(db=db, page=page)

    return schemas.response.ListOfEntityResponse(
        data=[
            getters.order.get_order(order=order)
            for order in data
        ],
        meta=schemas.response.Meta(paginator=paginator)
    )

@router.post(
    '/cp/orders/',
    tags=["Панель Управления / Заказы"],
    name="Создать заказ",   
    response_model=schemas.response.SingleEntityResponse[schemas.order.CreatingOrder],
    responses=get_responses_description_by_codes([401, 403, 400]),
)
def create(
        data: schemas.order.CreatingOrder,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_superuser),
):
    order = crud.crud_order.order.create(db=db, obj_in=data)

    return schemas.response.SingleEntityResponse(
        data=getters.order.get_order(order=order)
    )




@router.delete(
    '/cp/orders/{order_id}/',
    tags=["Панель Управления / Заказы"],
    name="Удалить заказ",
    response_model=schemas.response.OkResponse,
    responses=get_responses_description_by_codes([401, 403])
)
def delete(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_superuser),
        order_id: int = Path(...),
):

    crud.crud_order.order.remove_by_id(db=db, id=order_id)

    return schemas.response.OkResponse()

@router.put(
    '/cp/orders/{order_id}/',
    tags=["Панель Управления / Заказы"],
    name="изменить заказ",
    response_model=schemas.response.SingleEntityResponse[schemas.order.UpdatingOrder],
    responses=get_responses_description_by_codes([401, 403, 400, 404])
)
def edit(
        data: schemas.order.UpdatingOrder,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_superuser),
        order_id: int = Path(...),
):
    country = crud.crud_order.order.get(db=db, id=order_id)
    if country is None:
        raise UnfoundEntity(message="Страна не найдена", num=1)

    country = crud.crud_order.order.update(db=db, db_obj=country, obj_in=data)

    return schemas.response.SingleEntityResponse(
        data=getters.country.get_country(country=country)
    )











