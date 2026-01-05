import pytest
from uuid import uuid4
from unittest.mock import Mock, call
from datetime import datetime
from src.features.users.application.use_cases.update import UpdateUser
from src.features.users.domain.entities import User
from src.security.domain.services.encryption import EncryptionService
from src.security.domain.services.hashing import HashingService
from src.persistence.domain.repositories import DataRepository
from src.persistence.domain.exceptions import NotFoundException
from src.features.users.domain.schemas import UpdateUserSchema


@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def mock_encryption():
    return Mock()

@pytest.fixture
def mock_hashing():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository,
    mock_encryption,
    mock_hashing
):
    return UpdateUser(
        repository=mock_repository,
        encryption=mock_encryption,
        hashing=mock_hashing
    )


def test_user_update_success(
    mock_repository,
    mock_encryption:EncryptionService,
    mock_hashing: HashingService,
    use_case: UpdateUser
):
    changes = UpdateUserSchema(
        name="updated_name",
        email="updated_email"
    )

    user_id = uuid4()
    
    fake_updated_user = User(
        user_id=user_id,
        name="updated_name",
        email="updated_email",
        email_hash="hashed_email",
        password="password",
        created_at=datetime.now()
    )

    mock_encryption.decrypt.return_value = "decrypted"
    mock_repository.update.return_value = fake_updated_user
    mock_hashing.hash_for_search.return_value = "hashed_for_search"

    result = use_case.execute(
        user_id=user_id,
        changes=changes
    )

    assert mock_encryption.encrypt.call_count == 2
    mock_encryption.encrypt.assert_has_calls([
        call("updated_name"),
        call("updated_email")
    ])

    mock_hashing.hash_for_search.assert_called_once_with(
        "updated_email"
    )

    assert result.name == "decrypted"
    assert result.email == "decrypted"
    assert result.user_id == user_id



def test_update_user_not_found(
    mock_repository,
    mock_encryption:EncryptionService,
    mock_hashing: HashingService,
    use_case: UpdateUser
):
    changes = UpdateUserSchema(
        name="updated_name",
        email="updated_email"
    )

    user_id = uuid4()

    mock_repository.update.return_value = None
    mock_hashing.hash_for_search.return_value = "hashed_for_search"
    with pytest.raises(NotFoundException) as exc_info:
        result = use_case.execute(
            user_id=user_id,
            changes=changes
        )


    assert mock_encryption.encrypt.call_count == 2
    mock_encryption.encrypt.assert_has_calls([
        call("updated_name"),
        call("updated_email")
    ])

    mock_hashing.hash_for_search.assert_called_once_with(
        "updated_email"
    )

    assert "User not found" in str(exc_info)