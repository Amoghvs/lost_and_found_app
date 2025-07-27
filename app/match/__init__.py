from fastapi import APIRouter
from app.match.router import match_router

API_STR = "/match"

match_router = APIRouter(prefix="/match")
match_router.include_router(match_router)
