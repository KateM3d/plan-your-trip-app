import uuid

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
def created_option(client, created_trip_request):
    payload = {
        **TRIP_OPTION_PAYLOAD,
        "trip_request_id": created_trip_request["id"],
    }
    response = client.post("/options/create-option", json=payload)
    assert response.status_code == 200
    return response.json()


@pytest.fixture(scope="module", autouse=True)
def cleanup_trip_option_test_data():
    yield
    db = SessionLocal()
    try:
        db.query(TripOption).delete()
        db.query(TripRequest).delete()
        db.commit()
    finally:
        db.close()


def test_create_option(client, created_trip_request):
    payload = {
        **TRIP_OPTION_PAYLOAD,
        "trip_request_id": created_trip_request["id"],
    }

    response = client.post("/options/create-option", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["id"] is not None
    assert body["trip_request_id"] == created_trip_request["id"]
    assert body["title"] == "Wine tour"
    assert body["short_description"] == "Visit vineyards"
    assert body["estimated_budget"] == 500
    assert body["created_at"] is not None
    assert body["is_saved"] is False
    assert body["is_deleted"] is False


def test_get_all_options(client, created_option):
    created_id = created_option["id"]

    response = client.get("/options/")
    assert response.status_code == 200

    body = response.json()
    assert isinstance(body, list)

    option = next((item for item in body if item["id"] == created_id), None)
    assert option is not None
    assert option["title"] == "Wine tour"
    assert option["estimated_budget"] == 500


def test_get_option_by_id(client, created_option):
    created_id = created_option["id"]

    response = client.get(f"/options/id/{created_id}")
    assert response.status_code == 200

    body = response.json()
    assert body["id"] == created_id
    assert body["title"] == "Wine tour"
    assert body["short_description"] == "Visit vineyards"
    assert body["trip_request_id"] == created_option["trip_request_id"]


def test_get_option_by_id_not_found(client):
    response = client.get(f"/options/id/{uuid.uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Option not found"


def test_get_options_by_trip_request_id(client, created_trip_request, created_option):
    trip_request_id = created_trip_request["id"]

    response = client.get(f"/options/trip-request/{trip_request_id}")
    assert response.status_code == 200

    body = response.json()
    assert isinstance(body, list)
    assert any(option["id"] == created_option["id"] for option in body)
    assert all(option["trip_request_id"] == trip_request_id for option in body)


def test_get_options_by_trip_request_id_not_found(client):
    response = client.get(f"/options/trip-request/{uuid.uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Options not found"


def test_delete_option(client, created_option):
    created_id = created_option["id"]

    response = client.put(f"/options/delete/{created_id}")
    assert response.status_code == 200

    body = response.json()
    assert body["id"] == created_id
    assert body["is_deleted"] is True
    assert body["is_saved"] is False

    get_response = client.get(f"/options/id/{created_id}")
    assert get_response.status_code == 200
    assert get_response.json()["is_deleted"] is True
