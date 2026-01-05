import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime
from src.features.categories.application.use_cases.collection import GetCategoryCollection
from src.features.categories.domain.entities import Category


@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository
):
    return GetCategoryCollection(
        repository=mock_repository
    )

def test_success(
    mock_repository,
    use_case: GetCategoryCollection
):
    user_id = uuid4()

    fake_collection = [
        Category(
            category_id=uuid4(),
            user_id=user_id,
            name="...n",
            created_at=datetime.now()
        ),

        Category(
            category_id=uuid4(),
            user_id=user_id,
            name="...n1",
            created_at=datetime.now()
        )
    ]

    mock_repository.get_many.return_value = fake_collection

    result = use_case.execute(
        user_id=user_id
    )

    assert isinstance(result, list)

    assert len(result)  == 2

    assert result[0].user_id == user_id


def test_not_found(
    mock_repository,
    use_case: GetCategoryCollection
):
    user_id = uuid4()

    mock_repository.get_many.return_value = None

    result = use_case.execute(
        user_id=user_id
    )

    assert isinstance(result, list)

    assert len(result) == 0

    