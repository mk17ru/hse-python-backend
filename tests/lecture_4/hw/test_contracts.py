from pydantic import ValidationError
from datetime import datetime
import pytest

from lecture_4.demo_service.api.contracts import RegisterUserRequest, UserResponse
from pydantic import SecretStr

from lecture_4.demo_service.api.utils import requires_admin
from lecture_4.demo_service.core.users import UserInfo, UserRole, UserEntity


def test_register_user_request_valid():
    request = RegisterUserRequest(
        username="testuser",
        name="Test User",
        birthdate=datetime(2000, 1, 1),
        password=SecretStr("Password123")
    )

    assert request.username == "testuser"
    assert request.name == "Test User"
    assert request.birthdate == datetime(2000, 1, 1)
    assert request.password.get_secret_value() == "Password123"


def test_register_user_request_invalid():
    with pytest.raises(ValidationError):
        RegisterUserRequest(
            username="testuser",
            name="Test User",
            birthdate="invalid_date",
            password=SecretStr("Password123")
        )

def test_user_response_missing_fields():
    user_info = UserInfo(
        username="testuser",
        name="Test User",
        birthdate=datetime(2000, 1, 1),
        role=UserRole.USER,
        password="Password123"
    )
    entity = UserEntity(uid=1, info=user_info)

    response = UserResponse.from_user_entity(entity)

    assert hasattr(response, 'username')
    assert hasattr(response, 'role')

def test_requires_admin_valid():
    admin_user = UserEntity(
        uid=1,
        info=UserInfo(
            username="admin",
            name="Admin User",
            birthdate=datetime(2000, 1, 1),
            role=UserRole.ADMIN,
            password="AdminPassword"
        )
    )

    result = requires_admin(admin_user)
    assert result == admin_user
    assert result.info.role == UserRole.ADMIN
