import pytest
from uuid import uuid4
from datetime import datetime
from unittest.mock import Mock
from src.features.blogs.application.use_cases.delete import DeleteBlog
from src.features.blogs.domain.entities import Blog
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository
):
    return DeleteBlog(
        repository=mock_repository
    )


def test_success(
    mock_repository,
    use_case: DeleteBlog
):
    blog_id = uuid4()
    user_id = uuid4()
    fake_blog = Blog(
        blog_id=blog_id,
        user_id=user_id,
        name="...n",
        description="...d",
        created_at=datetime.now()
    )

    mock_repository.get_one.return_value = fake_blog
    mock_repository.delete.return_value = fake_blog

    result = use_case.execute(
        user_id=user_id,
        blog_id=blog_id
    )

    mock_repository.get_one.assert_called_once_with(
        key="blog_id",
        value=blog_id
    )

    mock_repository.delete.assert_called_once_with(
        key="blog_id",
        value=blog_id
    )

    assert result.blog_id == blog_id
    assert result.user_id == user_id



def test_not_found(
    mock_repository,
    use_case: DeleteBlog
):
    blog_id = uuid4()
    user_id = uuid4()
    mock_repository.get_one.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
        use_case.execute(
            user_id=user_id,
            blog_id=blog_id
        )

    mock_repository.get_one.assert_called_once_with(
        key="blog_id",
        value=blog_id
    )

    mock_repository.delete.assert_not_called()
    assert "Blog not found" in str(exc_info)


def test_permission_error(
    mock_repository,
    use_case: DeleteBlog
):
    blog_id = uuid4()
    user_id = uuid4()
    not_my_blog = Blog(
        blog_id=blog_id,
        user_id=uuid4(),
        name="...n",
        description="...d",
        created_at=datetime.now()
    )

    mock_repository.get_one.return_value = not_my_blog

    with pytest.raises(PermissionsException) as exc_info:
        use_case.execute(
            user_id=user_id,
            blog_id=blog_id
        )

    
    mock_repository.get_one.assert_called_once_with(
        key="blog_id",
        value=blog_id
    )
    mock_repository.delete.assert_not_called()
    assert "Forbidden" in str(exc_info)

    