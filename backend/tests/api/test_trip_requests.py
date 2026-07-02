import pytest
from app.db.session import SessionLocal
from app.models.trip_option import TripOption
from app.models.trip_request import TripRequest


TRIP_REQUEST_PAYLOAD = {
    "destination": "Paris",
    "starting_location": "Berlin",
    "budget": 300,
    "currency": "EUR",
    "travelers": 2,
    "departure_datetime": "2026-08-01T08:00:00+00:00",
    "return_datetime": "2026-08-03T18:00:00+00:00",
    "user_preferences": "wine and food",
}


TRIP_OPTION_PAYLOAD = {
    "title": "Wine tour",
    "short_description": "Visit vineyards",
    "estimated_budget": 500,
}


@pytest.fixture
def created_trip_request(client):
    response = client.post("/trips/create-trip", json=TRIP_REQUEST_PAYLOAD)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def created_trip_request_with_options(client, created_trip_request):
    trip_request_id = created_trip_request["id"]
    options = []
    for title_suffix in ("A", "B"):
        payload = {
            **TRIP_OPTION_PAYLOAD,
            "title": f"{TRIP_OPTION_PAYLOAD['title']} {title_suffix}",
            "trip_request_id": trip_request_id,
        }
        response = client.post("/options/create-option", json=payload)
        assert response.status_code == 200
        options.append(response.json())
    return {"trip_request": created_trip_request, "options": options}


@pytest.fixture(scope="module", autouse=True)
def cleanup_trip_request_test_data():
    yield
    db = SessionLocal()
    try:
        db.query(TripOption).delete()
        db.query(TripRequest).delete()
        db.commit()
    finally:
        db.close()


def test_create_trip_request(client):
    response = client.post("/trips/create-trip", json=TRIP_REQUEST_PAYLOAD)
    assert response.status_code == 201

    body = response.json()
    
    assert body["destination"] == "Paris"
    assert body["starting_location"] == "Berlin"
    assert body["budget"] == 300
    assert body["currency"] == "EUR"
    assert body["travelers"] == 2
    assert body["departure_datetime"] == "2026-08-01T08:00:00Z"
    assert body["return_datetime"] == "2026-08-03T18:00:00Z"
    assert body["user_preferences"] == "wine and food"
    assert body["id"] is not None
    assert body["is_active"] is True
    assert body["is_completed"] is False
    assert body["is_deleted"] is False


def test_get_all_trip_requests(client, created_trip_request):
    created_id = created_trip_request["id"]

    response = client.get("/trips/")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)

    trip = next((item for item in body if item["id"] == created_id), None)
    assert trip is not None
    assert trip["destination"] == "Paris"
    assert trip["starting_location"] == "Berlin"
    assert trip["budget"] == 300
    assert trip["currency"] == "EUR"


def test_get_trip_request_by_id(client, created_trip_request):
    created_id = created_trip_request["id"]

    response = client.get(f"/trips/id/{created_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == created_id
    assert body["destination"] == "Paris"
    assert body["starting_location"] == "Berlin"


def test_delete_trip_request(client, created_trip_request_with_options):
    created_id = created_trip_request_with_options["trip_request"]["id"]
    option_ids = {option["id"] for option in created_trip_request_with_options["options"]}

    response = client.put(f"/trips/delete/{created_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == created_id
    assert body["is_deleted"] is True
    assert body["is_active"] is False
    assert body["is_completed"] is False

    options_response = client.get(f"/options/trip-request/{created_id}")
    assert options_response.status_code == 200
    options = options_response.json()
    assert len(options) == len(option_ids)
    for option in options:
        assert option["id"] in option_ids
        assert option["is_deleted"] is True
        assert option["is_saved"] is False