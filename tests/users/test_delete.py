import pytest
from uuid import uuid4
from datetime import datetime
from unittest.mock import Mock, call
from src.features.users.application.use_cases.delete import DeleteUser
from src.persistence.domain.exceptions import NotFoundException
from src.features.users.domain.entities import User


@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def encryption():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository,
    encryption
):
    return DeleteUser(
        repository=mock_repository,
        encryption=encryption
    )


def test_delete_success(
    mock_repository,
    encryption,
    use_case: DeleteUser
):
    user_id = uuid4()
    encryption.decrypt.return_value = "decrypted"
    fake_user = User(
        user_id=user_id,
        name="name",
        email="email",
        email_hash="hashed email",
        password="hashed password",
        created_at=datetime.now()
    )

    mock_repository.delete.return_value = fake_user

    result = use_case.execute(
        user_id=user_id
    )

    mock_repository.delete.assert_called_once_with(
        key="user_id",
        value=user_id
    )

    assert encryption.decrypt.call_count == 2
    encryption.decrypt.assert_has_calls([
        call("email"),
        call("name")
    ])

    assert result.name == "decrypted"
    assert result.email == "decrypted"
    assert result.user_id == user_id


def test_delete_not_found(
    mock_repository,
    use_case
):
    
    user_id = uuid4()
    mock_repository.delete.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
        result = use_case.execute(
            user_id=user_id
        )

    mock_repository.delete.assert_called_once_with(
        key="user_id",
        value=user_id
    )
    assert "User not found" in str(exc_info)
    
