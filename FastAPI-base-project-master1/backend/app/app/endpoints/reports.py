from fastapi import APIRouter, Query, Depends, Path, UploadFile, File
from sqlalchemy.orm import Session
import time
from app import crud, schemas, getters, deps, models
from app.exceptions import UnfoundEntity
from app.utils.response import get_responses_description_by_codes
from datetime import datetime

router = APIRouter()


@router.get(
    '/cp/reports/',
    tags=["Панель Управления / Отчеты"],
    name="Получить все Отчеты",
    response_model=schemas.response.ListOfEntityResponse[schemas.report.GettingReport],
    responses=get_responses_description_by_codes([400])
)
@router.get(
    '/reports/',
    tags=["Отчеты"],
    name="Получить все Отчеты",
    response_model=schemas.response.ListOfEntityResponse[schemas.report.GettingReport],
    responses=get_responses_description_by_codes([400])
)
def get_all(
        db: Session = Depends(deps.get_db),
        page: int | None = Query(None),
        order_id: int | None = Query(None)
):
    data, paginator = crud.crud_report.report.get_page(
        db=db, page=page, order_id=order_id)

    return schemas.response.ListOfEntityResponse(
        data=[
            getters.report.get_report(report=report)
            for report in data
        ],
        meta=schemas.response.Meta(paginator=paginator)
    )


@router.post(
    '/cp/reports/',
    tags=["Панель Управления / Отчеты"],
    name="Создать отчет",
    response_model=schemas.response.SingleEntityResponse[schemas.report.CreatingReport],
    responses=get_responses_description_by_codes([401, 403, 400]),
)
def create(
        data: schemas.report.CreatingReport,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_superuser),
):
    report = crud.crud_report.report.create(
        db=db, obj_in=data, created=round(time.time()))

    return schemas.response.SingleEntityResponse(
        data=getters.report.get_report(report=report)
    )


@router.delete(
    '/cp/reports/{report_id}/',
    tags=["Панель Управления / Отчеты"],
    name="Удалить отчет",
    response_model=schemas.response.OkResponse,
    responses=get_responses_description_by_codes([401, 403])
)
def delete(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_superuser),
        report_id: int = Path(...),
):

    crud.crud_report.report.remove_by_id(db=db, id=report_id)

    return schemas.response.OkResponse()


@router.put(
    '/cp/reports/{report_id}/',
    tags=["Панель Управления / Отчеты"],
    name="изменить отчет",
    response_model=schemas.response.SingleEntityResponse[schemas.UpdatingReport],
    responses=get_responses_description_by_codes([401, 403, 400, 404])
)
def edit(
        data: schemas.report.UpdatingReport,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_superuser),
        report_id: int = Path(...),
):
    report = crud.crud_report.report.get(db=db, id=report_id)
    if report is None:
        raise UnfoundEntity(message="Страна не найдена", num=1)

    report = crud.crud_report.report.update(db=db, db_obj=report, obj_in=data)

    return schemas.response.SingleEntityResponse(
        data=getters.report.get_report(report=report)
    )


@router.put(
    '/cp/reports/{report_id}/image/',
    tags=["Панель Управления / Отчеты"],
    name="изменить аву",
    response_model=schemas.response.SingleEntityResponse[schemas.GettingReport],
    responses=get_responses_description_by_codes([401, 403, 400, 404])
)
def edit(
        image: UploadFile | None = File(None),
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_superuser),
        report_id: int = Path(...),
):
    report = crud.crud_report.report.get(db=db, id=report_id)
    if report is None:
        raise UnfoundEntity(message="Страна не найдена", num=1)

    crud.crud_report.report.change_content(
        db=db,
        obj=report,
        content=image,
        content_path='reports/image/',
        content_column='img'
    )

    return schemas.response.SingleEntityResponse(
        data=getters.report.get_report(report=report)
    )
