import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.trip_request_service import TripRequestService
from app.repositories.trip_request import TripRequestRepository
from app.schemas.trip_request import TripRequestCreate, TripRequestResponse
from app.db.session import SessionLocal

router = APIRouter()

repo = TripRequestRepository()
service = TripRequestService(repo)

def get_db():
    if SessionLocal is None:
        raise RuntimeError("Database not configured")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# create 
@router.post("/create-trip", response_model=TripRequestResponse, status_code=201)
def create_trip(data: TripRequestCreate, db: Session = Depends(get_db)):
    trip = service.create_trip(data)
    return repo.create(db, trip)

# get all trips
@router.get("/", response_model=list[TripRequestResponse])
def get_all_trips(db: Session = Depends(get_db)):
    return service.get_all_trips(db)

# get by destination name
@router.get("/name/{trip_destination}", response_model=list[TripRequestResponse])
def get_trips_by_destination(trip_destination: str, db: Session = Depends(get_db)):
    trips = service.get_trips_by_destination(db, trip_destination)
    if not trips:
        raise HTTPException(status_code=404, detail="Trips not found")
    return trips

# get by trip id
@router.get("/id/{trip_id}", response_model=TripRequestResponse)
def get_trip_by_id(trip_id: uuid.UUID, db : Session = Depends(get_db)):
    trip = service.get_trip_by_id(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

# get by number of travelers
@router.get("/travelers/{travelers}", response_model=list[TripRequestResponse])
def get_trips_by_number_of_travelers(travelers: int, db: Session = Depends(get_db)):
    trips = service.get_trips_by_number_of_travelers(db, travelers)
    if not trips:
        raise HTTPException(status_code=404, detail="Trips with this number of travelers not found"
        )
    return trips

# get by starting location
@router.get("/starting-location/{starting_location}", response_model = list[TripRequestResponse])
def get_trips_by_starting_location(starting_location: str, db: Session =Depends(get_db)):
    trips = service.get_trips_by_starting_location(db, starting_location)
    if not trips:
        raise HTTPException(status_code=404, detail="Trips with this starting location not found")
    return trips

# soft delete for trip request
@router.put("/delete/{id}", response_model = TripRequestResponse) 
def delete_request(id: uuid.UUID, db: Session = Depends(get_db)):
    request = service.delete_request(db, id)
    if not request:
        raise HTTPException(status_code = 404, detail = "Trip request not found")
    return request