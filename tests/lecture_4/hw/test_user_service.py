import pytest
from lecture_4.demo_service.core.users import UserService, UserInfo, UserRole


@pytest.fixture
def user_service():
    service = UserService(
        password_validators=[
            lambda pwd: len(pwd) > 8,
            lambda pwd: any(char.isdigit() for char in pwd),
        ]
    )

    service.register(
        UserInfo(
            username="admin",
            name="Administrator",
            birthdate="1970-01-01",
            role=UserRole.ADMIN,
            password="superAdminPassword123",
        )
    )

    return service


def test_register_user(user_service: UserService):
    user_info = UserInfo(
        username="new_user",
        name="New User",
        birthdate="2000-01-01",
        role=UserRole.USER,
        password="newUserPassword123",
    )

    user_entity = user_service.register(user_info)

    assert user_entity.uid is not None
    assert user_entity.info.username == "new_user"
    assert user_entity.info.role == UserRole.USER


def test_get_user_by_id(user_service: UserService):
    user_info = UserInfo(
        username="test_user",
        name="Test User",
        birthdate="1990-01-01",
        role=UserRole.USER,
        password="testPassword123",
    )
    user_entity = user_service.register(user_info)

    found_user = user_service.get_by_id(user_entity.uid)

    assert found_user is not None
    assert found_user.uid == user_entity.uid
    assert found_user.info.username == "test_user"


def test_get_user_by_username(user_service: UserService):
    user_info = UserInfo(
        username="test_user2",
        name="Test User 2",
        birthdate="1985-01-01",
        role=UserRole.USER,
        password="password456",
    )
    user_entity = user_service.register(user_info)

    found_user = user_service.get_by_username("test_user2")

    assert found_user is not None
    assert found_user.info.username == "test_user2"


def test_promote_user_to_admin(user_service: UserService):
    user_info = UserInfo(
        username="regular_user",
        name="Regular User",
        birthdate="1995-01-01",
        role=UserRole.USER,
        password="regularUserPassword1111",
    )
    user_entity = user_service.register(user_info)

    user_service.grant_admin(user_entity.uid)

    promoted_user = user_service.get_by_id(user_entity.uid)
    assert promoted_user.info.role == UserRole.ADMIN

def test_grant_nil(user_service: UserService):
    with pytest.raises(ValueError, match="user not found"):
        user_service.grant_admin(None)

def test_get_by_use(user_service: UserService):
    assert user_service.get_by_username(None) == None

def test_grant_тще_ащгтв_гыук(user_service: UserService):

    user_info = UserInfo(
        username="regular_user",
        name="Regular User",
        birthdate="1995-01-01",
        role=UserRole.USER,
        password="regularUserPassword1111",
    )

    user_entity = user_service.register(user_info)

    with pytest.raises(ValueError, match="user not found"):
        user_service.grant_admin(34323423)

def test_register_username_already_taken(user_service: UserService):
    user_info_1 = UserInfo(
        username="testuser",
        name="Test User",
        birthdate="2000-01-01T00:00:00",
        role=UserRole.USER,
        password="ValidPass1",
    )
    user_service.register(user_info_1)

    user_info_2 = UserInfo(
        username="testuser",
        name="Another User",
        birthdate="1995-01-01T00:00:00",
        role=UserRole.USER,
        password="AnotherPass1",
    )

    with pytest.raises(ValueError, match="username is already taken"):
        user_service.register(user_info_2)


def test_register_invalid_password(user_service: UserService):
    user_info = UserInfo(
        username="newuser",
        name="New User",
        birthdate="2000-01-01T00:00:00",
        role=UserRole.USER,
        password="short",
    )

    with pytest.raises(ValueError, match="invalid password"):
        user_service.register(user_info)

    user_info_invalid_digit = UserInfo(
        username="newuser2",
        name="Another User",
        birthdate="1990-05-05T00:00:00",
        role=UserRole.USER,
        password="NoDigitsHere",
    )

    with pytest.raises(ValueError, match="invalid password"):
        user_service.register(user_info_invalid_digit)