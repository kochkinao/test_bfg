import pytest
from fastapi.testclient import TestClient

from test_task.infrastructure.in_memory import InMemoryJobRepository
from test_task.main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_repository():
    app.state.job_repository = InMemoryJobRepository()


def test_job_happy_path():
    response = client.post(
        "/jobs",
        json={"title": "Собрать заказ"},
    )

    assert response.status_code == 201

    job_id = response.json()["id"]

    response = client.post(
        f"/jobs/{job_id}/assign",
        json={"assignee": "Alex"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ASSIGNED"

    response = client.post(
        f"/jobs/{job_id}/status",
        json={"new_status": "IN_PROGRESS"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "IN_PROGRESS"

    response = client.post(
        f"/jobs/{job_id}/status",
        json={"new_status": "COMPLETED"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "COMPLETED"


def test_get_nonexistent_job_returns_404():
    response = client.get("/jobs/not-found")

    assert response.status_code == 404


def test_invalid_transition_returns_409():
    response = client.post(
        "/jobs",
        json={"title": "Собрать заказ"},
    )

    job_id = response.json()["id"]

    response = client.post(
        f"/jobs/{job_id}/status",
        json={"new_status": "COMPLETED"},
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Недопустимый переход: CREATED -> COMPLETED"
    }