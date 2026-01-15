import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime
from src.features.categories.application.use_cases.collection import GetCategoryCollection
from src.features.categories.domain.entities import Category
from src.features.blogs.domain.entities import Blog
from src.persistence.domain.exceptions import NotFoundException

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
    return GetCategoryCollection(
        category_repository=mock_category_repository,
        blog_repository=mock_blog_repository
    )

def test_success(
    mock_category_repository,
    mock_blog_repository,
    use_case: GetCategoryCollection
):
    blog_id = uuid4()
    user_id = uuid4()
    fake_blog = Blog(
        blog_id=blog_id,
        user_id=user_id,
        name="blog",
        description="desc",
        created_at=datetime.now()
    )
    fake_collection = [
        Category(
            category_id=uuid4(),
            blog_id=blog_id,
            name="...n",
            created_at=datetime.now()
        ),
        Category(
            category_id=uuid4(),
            blog_id=blog_id,
            name="...n1",
            created_at=datetime.now()
        )
    ]

    mock_blog_repository.get_one.return_value = fake_blog
    mock_category_repository.get_many.return_value = fake_collection

    result = use_case.execute(
        blog_id=blog_id
    )

    mock_blog_repository.get_one.assert_called_once_with(
        key="blog_id",
        value=blog_id
    )
    mock_category_repository.get_many.assert_called_once_with(
        key="blog_id",
        value=blog_id
    )
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].blog_id == blog_id

def test_blog_not_found(
    mock_category_repository,
    mock_blog_repository,
    use_case: GetCategoryCollection
):
    blog_id = uuid4()
    mock_blog_repository.get_one.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
        use_case.execute(
            blog_id=blog_id
        )

    mock_blog_repository.get_one.assert_called_once_with(
        key="blog_id",
        value=blog_id
    )
    mock_category_repository.get_many.assert_not_called()
    assert "Blog not found" in str(exc_info.value)

def test_no_results(
    mock_category_repository,
    mock_blog_repository,
    use_case: GetCategoryCollection
):
    blog_id = uuid4()
    user_id = uuid4()
    fake_blog = Blog(
        blog_id=blog_id,
        user_id=user_id,
        name="blog",
        description="desc",
        created_at=datetime.now()
    )
    mock_blog_repository.get_one.return_value = fake_blog
    mock_category_repository.get_many.return_value = None

    result = use_case.execute(
        blog_id=blog_id
    )

    mock_blog_repository.get_one.assert_called_once_with(
        key="blog_id",
        value=blog_id
    )
    mock_category_repository.get_many.assert_called_once_with(
        key="blog_id",
        value=blog_id
    )
    assert isinstance(result, list)
    assert len(result) == 0
