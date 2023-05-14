from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas, deps, getters
from app.config import settings
from app.utils import security
from app.utils.response import get_responses_description_by_codes

router = APIRouter()


@router.post(
    '/login/access-token',
    response_model=schemas.Token, tags=["Вход"],
    name="Войти по логину и паролю",
    responses=get_responses_description_by_codes([400, 401])
)
def login_access_token(
        db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        'access_token': security.create_token(
            user.id,
            expires_delta=access_token_expires,
            token_type="access"
        ),
        'token_type': 'bearer',
    }


@router.post(
    '/cp/sign-in/',
    response_model=schemas.response.SingleEntityResponse[schemas.user.TokenWithUser], tags=["Вход"],
    name="Войти по логину и паролю",
    responses=get_responses_description_by_codes([400, 401])
)
def login_access_token(
        data: schemas.user.LoginData, db: Session = Depends(deps.get_db)
) -> Any:
    user = crud.user.authenticate(
        db, email=data.email, password=data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return schemas.response.SingleEntityResponse(
        data={
            'token': security.create_token(
                user.id,
                expires_delta=access_token_expires,
                token_type="access"
            ),
            'user': getters.user.get_user(user)
        }
    )

@router.post(
    '/sign-up/',
    tags=["Вход"],
    name="Зарегаца",
    response_model=schemas.response.SingleEntityResponse[schemas.user.TokenWithUser],
    responses=get_responses_description_by_codes([400])
)
def create_user(
        data: schemas.user.SigningUser,
        db: Session = Depends(deps.get_db),
):
    user = crud.crud_user.user.create(db=db, obj_in=data)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return  schemas.response.SingleEntityResponse(
        data={
            'token': security.create_token(
                user.id,
                expires_delta=access_token_expires,
                token_type="access"
            ),
            'user': getters.user.get_user(user)
        }
    )