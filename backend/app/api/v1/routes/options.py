import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.repositories.trip_option import TripOptionRepository
from app.services.trip_option_service import TripOptionService
from app.db.session import SessionLocal
from app.schemas.trip_option import TripOptionCreate, TripOptionResponse


router =APIRouter()

repo = TripOptionRepository()
service = TripOptionService(repo)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  

@router.post("/create-option", response_model = TripOptionResponse)
def create_option(data: TripOptionCreate, db: Session = Depends(get_db)):
    option = service.create_option(data)
    return repo.create(db, option)

@router.get("/", response_model = list[TripOptionResponse])
def get_all_options(db: Session = Depends(get_db)):
    options = service.get_all_options(db)
    return options

@router.get("/id/{id}", response_model = TripOptionResponse)
def get_option_by_id(id: uuid.UUID, db: Session = Depends(get_db)):
    option = service.get_option_by_id(db, id)
    if not option:
        raise HTTPException(status_code=404, detail="Option not found")
    return option 

#  get options by trip request id
@router.get("/trip-request/{trip_request_id}", response_model = list[TripOptionResponse])
def get_all_options_by_trip_request_id(trip_request_id: uuid.UUID, db:Session = Depends(get_db)):
    options = service.get_all_options_by_trip_request_id(db, trip_request_id)
    if not options:
        raise HTTPException(status_code = 404, detail = "Options not found")
    return options