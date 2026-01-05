import pytest
from uuid import uuid4
from datetime import datetime
from unittest.mock import Mock
from src.features.categories.application.use_cases.update import UpdateCategory
from src.features.categories.domain.entities import Category
from src.features.categories.domain.schemas import UpdateCategoryRequest
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository
):
    return UpdateCategory(
        repository=mock_repository
    )

@pytest.fixture
def mock_changes():
    return UpdateCategoryRequest(
        name="updated"
    )


def test_success(
    mock_repository,
    mock_changes,
    use_case: UpdateCategory
):
    category_id = uuid4()
    user_id = uuid4()
    fake_Category = Category(
        category_id=category_id,
        user_id=user_id,
        name="...n",
        created_at=datetime.now()
    )

    fake_updated_Category = Category(
        category_id=category_id,
        user_id=user_id,
        name="updated",
        created_at=datetime.now()
    )

    mock_repository.get_one.return_value = fake_Category
    mock_repository.update.return_value = fake_updated_Category

    result = use_case.execute(
        user_id=user_id,
        category_id=category_id,
        changes=mock_changes
    )

    mock_repository.get_one.assert_called_once_with(
        key="category_id",
        value=category_id
    )

    mock_repository.update.assert_called_once_with(
        key="category_id",
        value=category_id,
        changes=mock_changes.model_dump(exclude_none=True)
    )

    assert result.category_id == category_id
    assert result.user_id == user_id
    assert result.name == "updated"



def test_not_found(
    mock_repository,
    mock_changes,
    use_case: UpdateCategory
):
    category_id = uuid4()
    user_id = uuid4()
    mock_repository.get_one.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
        use_case.execute(
            user_id=user_id,
            category_id=category_id,
            changes=mock_changes
        )

    mock_repository.get_one.assert_called_once_with(
        key="category_id",
        value=category_id
    )

    mock_repository.update.assert_not_called()
    assert "Category not found" in str(exc_info)


def test_permission_error(
    mock_repository,
    mock_changes,
    use_case: UpdateCategory
):
    category_id = uuid4()
    user_id = uuid4()
    not_my_Category = Category(
        category_id=category_id,
        user_id=uuid4(),
        name="...n",
        description="...d",
        created_at=datetime.now()
    )

    mock_repository.get_one.return_value = not_my_Category

    with pytest.raises(PermissionsException) as exc_info:
        use_case.execute(
            user_id=user_id,
            category_id=category_id,
            changes=mock_changes
        )

    
    mock_repository.get_one.assert_called_once_with(
        key="category_id",
        value=category_id
    )
    mock_repository.update.assert_not_called()
    assert "Forbidden" in str(exc_info)

    