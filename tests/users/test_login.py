import pytest
from uuid import uuid4
from unittest.mock import Mock, call
from datetime import datetime
from src.features.users.application.use_cases.login import UserLogin
from src.features.users.domain.entities import User
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.services.encryption import EncryptionService
from src.security.domain.services.hashing import HashingService
from src.security.domain.exceptions import IncorrectPassword

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def mock_encryption():
    return Mock(spec=EncryptionService)

@pytest.fixture
def mock_hashing():
    return Mock(spec=HashingService)

@pytest.fixture
def use_case(
    mock_repository,
    mock_encryption,
    mock_hashing
):
    return UserLogin(
        repository=mock_repository,
        encryption=mock_encryption,
        hashing=mock_hashing
    )

def test_login_success(
    mock_repository,
    mock_encryption,
    mock_hashing,
    use_case: UserLogin
):
    user_id = uuid4()
    
    fake_user = User(
        user_id=user_id,
        name="name",
        email="email",
        email_hash="hashed_email",
        password="hashed_password",
        created_at=datetime.now()
    )

    fake_updated_user = User(
        user_id=user_id,
        name="name",
        email="email",
        email_hash="hashed_email",
        password="hashed_password",
        created_at=datetime.now()
    )


    mock_hashing.hash_for_search.return_value = "hashed_email"
    mock_repository.get_one.return_value = fake_user
    mock_repository.update.return_value = fake_updated_user

    mock_hashing.compare_password.return_value = True
    mock_encryption.decrypt.return_value = "decrypted"

    result = use_case.execute(
        email="email",
        password="pswd"
    )

    mock_hashing.hash_for_search.assert_called_once_with("email")
    mock_repository.get_one.assert_called_once_with(
        key="email_hash",
        value="hashed_email"
    )

    mock_encryption.decrypt.assert_has_calls([
        call("email"),
        call("name")
    ])

    assert result.email == "decrypted"
    assert result.name == "decrypted"
    assert result.user_id == user_id


def test_login_user_not_found(
    mock_repository,
    use_case: UserLogin,
    mock_encryption,
    mock_hashing
):
    mock_repository.get_one.return_value = None
    mock_hashing.hash_for_search.return_value = "hashed_email"

    with pytest.raises(NotFoundException) as exc_info:
        result = use_case.execute(
            email="email",
            password="password"
        )

    mock_repository.get_one.assert_called_once_with(
        key="email_hash",
        value="hashed_email"
    )
    
    assert "User not found" in str(exc_info)


def test_login_incorrect_password(
    mock_repository,
    use_case: UserLogin,
    mock_hashing
):
    user_id = uuid4()
    
    fake_user = User(
        user_id=user_id,
        name="name",
        email="email",
        email_hash="hashed_email",
        password="hashed_password",
        created_at=datetime.now()
    )

    mock_hashing.hash_for_search.return_value = "hashed_email"
    mock_repository.get_one.return_value = fake_user
    mock_hashing.compare_password.side_effect = IncorrectPassword("Incorrect email or password")

    
    with pytest.raises(IncorrectPassword) as exc_info:
        result = use_case.execute(
            email="email",
            password="hashed_password"
        )

    mock_repository.get_one.assert_called_once_with(
        key="email_hash",
        value="hashed_email"
    )

    assert "Incorrect email or password" in str(exc_info)






