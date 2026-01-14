import pytest
from uuid import uuid4
from datetime import datetime
from unittest.mock import Mock
from src.features.categories.application.use_cases.delete import DeleteCategory
from src.features.categories.domain.entities import Category
from src.features.blogs.domain.entities import Blog
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException

@pytest.fixture
def mock_category_repository():
    return Mock()

@pytest.fixture
def mock_blog_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_category_repository,
    mock_blog_repository
):
    return DeleteCategory(
        category_repository=mock_category_repository,
        blog_repository=mock_blog_repository
    )

def test_success(
    mock_category_repository,
    mock_blog_repository,
    use_case: DeleteCategory
):
    category_id = uuid4()
    blog_id = uuid4()
    user_id = uuid4()
    fake_category = Category(
        category_id=category_id,
        blog_id=blog_id,
        name="...n",
        created_at=datetime.now()
    )
    fake_blog = Blog(
        blog_id=blog_id,
        user_id=user_id,
        name="blog",
        description="desc",
        created_at=datetime.now()
    )

    mock_category_repository.get_one.return_value = fake_category
    mock_blog_repository.get_one.return_value = fake_blog
    mock_category_repository.delete.return_value = fake_category

    result = use_case.execute(
        user_id=user_id,
        category_id=category_id
    )

    mock_category_repository.get_one.assert_called_once_with(
        key="category_id",
        value=category_id
    )
    mock_blog_repository.get_one.assert_called_once_with(
        key="blog_id",
        value=blog_id
    )
    mock_category_repository.delete.assert_called_once_with(
        key="category_id",
        value=category_id
    )
    assert result.category_id == category_id
    assert result.blog_id == blog_id

def test_not_found(
    mock_category_repository,
    mock_blog_repository,
    use_case: DeleteCategory
):
    category_id = uuid4()
    user_id = uuid4()
    mock_category_repository.get_one.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
        use_case.execute(
            user_id=user_id,
            category_id=category_id
        )

    mock_category_repository.get_one.assert_called_once_with(
        key="category_id",
        value=category_id
    )
    mock_blog_repository.get_one.assert_not_called()
    mock_category_repository.delete.assert_not_called()
    assert "Category not found" in str(exc_info.value)

def test_permission_error(
    mock_category_repository,
    mock_blog_repository,
    use_case: DeleteCategory
):
    category_id = uuid4()
    blog_id = uuid4()
    user_id = uuid4()
    fake_category = Category(
        category_id=category_id,
        blog_id=blog_id,
        name="...n",
        created_at=datetime.now()
    )
    fake_blog = Blog(
        blog_id=blog_id,
        user_id=uuid4(),  # Not the same as user_id
        name="blog",
        description="desc",
        created_at=datetime.now()
    )

    mock_category_repository.get_one.return_value = fake_category
    mock_blog_repository.get_one.return_value = fake_blog

    with pytest.raises(PermissionsException) as exc_info:
        use_case.execute(
            user_id=user_id,
            category_id=category_id
        )

    mock_category_repository.get_one.assert_called_once_with(
        key="category_id",
        value=category_id
    )
    mock_blog_repository.get_one.assert_called_once_with(
        key="blog_id",
        value=blog_id
    )
    mock_category_repository.delete.assert_not_called()
    assert "Forbidden" in str(exc_info.value)