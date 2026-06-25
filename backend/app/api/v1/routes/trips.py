from fastapi import APIRouter

router = APIRouter()

@router.post("/create-trip")
def create_trip():
    return {
        "message": "Create trip endpoint works",
        "status": "not implemented yet"
    }
