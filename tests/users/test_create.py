import pytest
from unittest.mock import Mock, call
from uuid import uuid4
from datetime import datetime
from src.features.users.application.use_cases.create import CreateUser
from src.features.users.domain.schemas import CreateUserRequest
from src.features.users.domain.entities import User
from src.security.domain.services.encryption import EncryptionService
from src.security.domain.services.hashing import HashingService

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def mock_encryption():
    return Mock()

@pytest.fixture
def mock_hash():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository,
    mock_hash,
    mock_encryption
):
    return CreateUser(
        repository=mock_repository,
        encryption=mock_encryption,
        hashing=mock_hash
    )

def test_success(
    mock_repository,
    mock_encryption: EncryptionService,
    mock_hash: HashingService,
    use_case: CreateUser
):
    mock_user = User(
        user_id=uuid4(),
        name="encrypted",
        email="encrypted",
        email_hash="hashed_for_search",
        password="hashed",
        is_admin=True,
        created_at=datetime.now()
    )

    request = CreateUserRequest(
        code=123,
        name="Test",
        email="test_email",
        password="pass"
    )

    mock_encryption.encrypt.return_value = "encrypted"
    mock_hash.hash_for_search.return_value = "hashed_for_search"
    mock_hash.hash_password.return_value = "hashed"
    mock_repository.create.return_value = mock_user
    mock_encryption.decrypt.return_value = "decrypted"

    result = use_case.execute(
        req_data=request,
        is_admin=True
    )


    mock_hash.hash_for_search.assert_called_once_with(
        data="test_email"
    )  

    mock_hash.hash_password.assert_called_once_with(
        password="pass"
    )

    assert mock_encryption.encrypt.call_count == 2
    mock_encryption.encrypt.assert_has_calls([
        call("Test"),
        call("test_email")
    ])

    assert result.name == "decrypted"

    

