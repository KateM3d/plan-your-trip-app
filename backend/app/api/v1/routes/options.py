from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.trip_option import TripOption
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