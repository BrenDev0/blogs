import pytest
from uuid import uuid4
from datetime import datetime
from unittest.mock import Mock
from src.features.categories.application.use_cases.delete import DeleteCategory
from src.features.categories.domain.entities import Category
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository
):
    return DeleteCategory(
        repository=mock_repository
    )


def test_success(
    mock_repository,
    use_case: DeleteCategory
):
    category_id = uuid4()
    user_id = uuid4()
    fake_category = Category(
        category_id=category_id,
        user_id=user_id,
        name="...n",
        created_at=datetime.now()
    )

    mock_repository.get_one.return_value = fake_category
    mock_repository.delete.return_value = fake_category

    result = use_case.execute(
        user_id=user_id,
        category_id=category_id
    )

    mock_repository.get_one.assert_called_once_with(
        key="category_id",
        value=category_id
    )

    mock_repository.delete.assert_called_once_with(
        key="category_id",
        value=category_id
    )

    assert result.category_id == category_id
    assert result.user_id == user_id



def test_not_found(
    mock_repository,
    use_case: DeleteCategory
):
    category_id = uuid4()
    user_id = uuid4()
    mock_repository.get_one.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
        use_case.execute(
            user_id=user_id,
            category_id=category_id
        )

    mock_repository.get_one.assert_called_once_with(
        key="category_id",
        value=category_id
    )

    mock_repository.delete.assert_not_called()
    assert "Category not found" in str(exc_info)


def test_permission_error(
    mock_repository,
    use_case: DeleteCategory
):
    category_id = uuid4()
    user_id = uuid4()
    not_my_category = Category(
        category_id=category_id,
        user_id=uuid4(),
        name="...n",
        created_at=datetime.now()
    )

    mock_repository.get_one.return_value = not_my_category

    with pytest.raises(PermissionsException) as exc_info:
        use_case.execute(
            user_id=user_id,
            category_id=category_id
        )

    
    mock_repository.get_one.assert_called_once_with(
        key="category_id",
        value=category_id
    )
    mock_repository.delete.assert_not_called()
    assert "Forbidden" in str(exc_info)

    