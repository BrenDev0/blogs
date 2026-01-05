import pytest
from unittest.mock import Mock
from uuid import uuid4
from src.features.categories.application.use_cases.create import CreateCategory
from src.features.categories.domain.entities import Category
from src.features.categories.domain.schemas import CreateCategoryRequest
from datetime import datetime

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository
): 
    return CreateCategory(
        repository=mock_repository
    )

def test_success(
    mock_repository,
    use_case: CreateCategory
):
    user_id = uuid4()
    fake_category = Category(
        category_id=uuid4(),
        user_id=user_id,
        name="...n",
        created_at=datetime.now()
    )

    mock_repository.create.return_value = fake_category

    req = CreateCategoryRequest(
        name="...n"
    )
    result = use_case.execute(
        user_id=user_id,
        req_data=req
    )

    mock_repository.create.assert_called_once()

    assert result.user_id == user_id