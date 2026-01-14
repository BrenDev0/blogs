import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime
from src.features.categories.application.use_cases.create import CreateCategory
from src.features.categories.domain.entities import Category
from src.features.categories.domain.schemas import CreateCategoryRequest
from src.features.blogs.domain.entities import Blog
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException

@pytest.fixture
def mock_category_repository():
    return Mock()

@pytest.fixture
def mock_blogs_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_category_repository,
    mock_blogs_repository
):
    return CreateCategory(
        category_repository=mock_category_repository,
        blogs_repository=mock_blogs_repository
    )

def test_success(
    mock_category_repository,
    mock_blogs_repository,
    use_case: CreateCategory
):
    user_id = uuid4()
    blog_id = uuid4()
    fake_blog = Blog(
        blog_id=blog_id,
        user_id=user_id,
        name="blog",
        description="desc",
        created_at=datetime.now()
    )
    fake_category = Category(
        category_id=uuid4(),
        blog_id=blog_id,
        name="...n",
        created_at=datetime.now()
    )

    mock_blogs_repository.get_one.return_value = fake_blog
    mock_category_repository.create.return_value = fake_category

    req = CreateCategoryRequest(
        name="...n"
    )
    result = use_case.execute(
        blog_id=blog_id,
        user_id=user_id,
        req_data=req
    )

    mock_blogs_repository.get_one.assert_called_once_with(
        key="blog_id",
        value=blog_id
    )
    mock_category_repository.create.assert_called_once()
    assert result.blog_id == blog_id
    assert result.name == "...n"

def test_blog_not_found(
    mock_category_repository,
    mock_blogs_repository,
    use_case: CreateCategory
):
    user_id = uuid4()
    blog_id = uuid4()
    mock_blogs_repository.get_one.return_value = None

    req = CreateCategoryRequest(
        name="...n"
    )

    with pytest.raises(NotFoundException):
        use_case.execute(
            blog_id=blog_id,
            user_id=user_id,
            req_data=req
        )

    mock_blogs_repository.get_one.assert_called_once_with(
        key="blog_id",
        value=blog_id
    )
    mock_category_repository.create.assert_not_called()

def test_permission_error(
    mock_category_repository,
    mock_blogs_repository,
    use_case: CreateCategory
):
    user_id = uuid4()
    blog_id = uuid4()
    fake_blog = Blog(
        blog_id=blog_id,
        user_id=uuid4(),  # Not the same as user_id
        name="blog",
        description="desc",
        created_at=datetime.now()
    )
    mock_blogs_repository.get_one.return_value = fake_blog

    req = CreateCategoryRequest(
        name="...n"
    )

    with pytest.raises(PermissionsException):
        use_case.execute(
            blog_id=blog_id,
            user_id=user_id,
            req_data=req
        )

    mock_blogs_repository.get_one.assert_called_once_with(
        key="blog_id",
        value=blog_id
    )
    mock_category_repository.create.assert_not_called()