from fastapi import APIRouter

from app.endpoints import login, users, countries, orders, reports

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(countries.router)
api_router.include_router(orders.router)
api_router.include_router(reports.router)