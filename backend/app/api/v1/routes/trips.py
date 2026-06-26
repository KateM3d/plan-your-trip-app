import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.trip_service import TripService
from app.repositories.trip_request import TripRequestRepository
from app.schemas.trip_request import TripRequestCreate, TripRequestResponse
from app.db.session import SessionLocal

router = APIRouter()

repo = TripRequestRepository()
service = TripService(repo)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# create 
@router.post("/create-trip", response_model=TripRequestResponse)
def create_trip(data: TripRequestCreate, db: Session = Depends(get_db)):
    trip = service.create_trip(data)
    return repo.create(db, trip)

# get all trips

@router.get("/", response_model=list[TripRequestResponse])
def get_all_trips(db: Session = Depends(get_db)):
    return service.get_all_trips(db)

@router.get("/{trip_id}", response_model=TripRequestResponse)
def get_trip_by_id(trip_id: uuid.UUID, db : Session = Depends(get_db)):
    trip = service.get_trip_by_id(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip
    