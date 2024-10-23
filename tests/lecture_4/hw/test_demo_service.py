import pytest
from fastapi.testclient import TestClient
from http import HTTPStatus

from lecture_4.demo_service.api.main import create_app

@pytest.fixture
def client():
    app = create_app()
    with TestClient(app) as instance:
        yield instance


@pytest.fixture
def user_request() -> dict[str, str]:
    return {
        "username": "user",
        "name": "User Name",
        "birthdate": "1990-01-01T00:00:00",
        "password": "UserPassword123",
    }


def test_admin_registration(client: TestClient):
    response = client.post(
        "/user-register",
        json={
            "username": "cool",
            "name": "user",
            "birthdate": "1970-01-01T00:00:00",
            "role" : "ADMIN",
            "password": "superPassword123",
        },
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["username"] == "cool"
    assert response_data["role"] == "user"

@pytest.mark.usefixtures(
    "client",
)
def test_register_user(client: TestClient):
    response = client.post(
        "/user-register",
        json={
            "username": "newuser",
            "name": "New User",
            "birthdate": "2000-01-01T00:00:00",
            "password": "Password123",
        },
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data["username"] == "newuser"
    assert data["name"] == "New User"


def test_get_user(client: TestClient, user_request:dict[str, str]):
    response = client.post(
        "/user-register",
        json=user_request
    )
    assert response.status_code == HTTPStatus.OK
    response = client.post(
        "/user-get", params={"username": "user"},
        auth= ("user","UserPassword123"),
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["username"] == "user"

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    response = client.post(
        "/user-get", params={"id": data["uid"]},
        auth= ("user","UserPassword123"),
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["username"] == "user"

def test_get_user_failed_both_provided(client: TestClient, user_request:dict[str, str]):
    response = client.post(
        "/user-register",
        json=user_request
    )
    assert response.status_code == HTTPStatus.OK
    response = client.post(
        "/user-get", params={"id" : 1, "username": "user"},
        auth= ("user","UserPassword123"),
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST

def test_get_failed_invalid_name(client: TestClient, user_request:dict[str, str]):
    response = client.post(
        "/user-register",
        json=user_request
    )
    assert response.status_code == HTTPStatus.OK
    response = client.post(
        "/user-get", params={"username": "lol"},
        auth= ("user","UserPassword123"),
    )
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_get_failed_no_params(client: TestClient, user_request:dict[str, str]):
    response = client.post(
        "/user-register",
        json=user_request
    )
    assert response.status_code == HTTPStatus.OK
    response = client.post(
        "/user-get", params={},
        auth= ("user","UserPassword123"),
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST

@pytest.mark.usefixtures(
    "client",
)
def test_promote_user(client: TestClient):
    resp = client.post(
        "/user-register",
        json={
            "username": "normaluser",
            "name": "Normal User",
            "birthdate": "1995-01-01T00:00:00",
            "password": "Password1234",
        },
    )

    assert resp.status_code == HTTPStatus.OK

    resp = client.post(
        "/user-promote", params={"id": 2}, auth=("admin", "superSecretAdminPassword123")
    )
    assert resp.status_code == HTTPStatus.OK


@pytest.mark.usefixtures(
    "client",
)
def test_promote_user_unauth(client: TestClient):
    resp = client.post(
        "/user-register",
        json={
            "username": "normaluser",
            "name": "Normal User",
            "birthdate": "1995-01-01T00:00:00",
            "password": "Password1234",
        },
    )

    response = client.post(
        "/user-promote", params={"id": 1}, auth=("normaluser", "Password123")
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_promote_user_forbidden(client: TestClient):
    client.post(
        "/user-register",
        json={
            "username": "normaluser",
            "name": "Normal User",
            "birthdate": "1995-01-01T00:00:00",
            "password": "Password1234",
        },
    )

    response = client.post(
        "/user-promote", params={"id": 1}, auth=("normaluser", "Password1234")
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_promote_user_not_admin(client: TestClient):
    client.post(
        "/user-register",
        json={
            "username": "normaluser",
            "name": "Normal User",
            "birthdate": "1995-01-01T00:00:00",
            "password": "Password1234",
        },
    )

    response = client.post(
        "/user-promote", params={"id": 1}, auth=("normaluser", "Password1234")
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_client_create():
    app = create_app()
    return app is not None
