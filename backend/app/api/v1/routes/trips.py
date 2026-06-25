from fastapi import APIRouter
from app.services.trip_service import TripService

router = APIRouter()
service = TripService()

@router.post("/create-trip")
def create_trip(data: dict):
    return service.create_trip(data.get("prompt"))
