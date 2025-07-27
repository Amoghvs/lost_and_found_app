from fastapi import APIRouter
from app.lost_found.router import router

API_STR = "/lost_found"

lost_found_router = APIRouter(prefix=API_STR)
lost_found_router.include_router(router)
