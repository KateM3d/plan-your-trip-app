from fastapi import APIRouter
from app.api.v1.routes import trips
from app.api.v1.routes import options

api_router = APIRouter()
api_router.include_router(trips.router, prefix="/trips", tags=["Trips"])
api_router.include_router(options.router, prefix="/options", tags=["Options"])