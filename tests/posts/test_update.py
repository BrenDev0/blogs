import pytest
from uuid import uuid4
from datetime import datetime
from unittest.mock import Mock
from src.features.posts.application.use_cases.update import UpdateBlogPost
from src.features.posts.domain.entities import BlogPost
from src.features.posts.domain.schemas import UpdateBlogPostRequest
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
    return UpdateBlogPost(
        post_repository=mock_repository
    )

@pytest.fixture
def mock_changes():
    return UpdateBlogPostRequest(
        title="updated title"
    )

def test_success(
    mock_repository,
    mock_changes,
    use_case: UpdateBlogPost
):
    post_id = uuid4()
    user_id = uuid4()
    blog_id = uuid4()
    fake_blog = Blog(
        blog_id=blog_id,
        user_id=user_id,
        name="...",
        description="...",
        created_at=datetime.now()
    )
    fake_post = BlogPost(
        post_id=post_id,
        blog_id=blog_id,
        category_id=None,
        author="me",
        title="old title",
        content_1="...",
        content_2="...",
        images=None,
        published=True,
        published_at=datetime.now(),
        created_at=datetime.now(),
        blog=fake_blog
    )
    fake_updated_post = BlogPost(
        post_id=post_id,
        blog_id=blog_id,
        category_id=None,
        author="me",
        title="updated title",
        content_1="...",
        content_2="...",
        images=None,
        published=True,
        published_at=datetime.now(),
        created_at=datetime.now(),
        blog=fake_blog
    )

    mock_repository.get_one.return_value = fake_post
    mock_repository.update.return_value = fake_updated_post

    result = use_case.execute(
        user_id=user_id,
        post_id=post_id,
        changes=mock_changes
    )

    mock_repository.get_one.assert_called_once_with(
        key="post_id",
        value=post_id
    )

    mock_repository.update.assert_called_once_with(
        key="post_id",
        value=post_id,
        changes=mock_changes.model_dump(exclude_none=True)
    )

    assert result.post_id == post_id
    assert result.title == "updated title"

def test_not_found(
    mock_repository,
    mock_changes,
    use_case: UpdateBlogPost
):
    post_id = uuid4()
    user_id = uuid4()
    mock_repository.get_one.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
        use_case.execute(
            user_id=user_id,
            post_id=post_id,
            changes=mock_changes
        )

    mock_repository.get_one.assert_called_once_with(
        key="post_id",
        value=post_id
    )
    mock_repository.update.assert_not_called()
    assert "Post not found" in str(exc_info)

def test_permission_error(
    mock_repository,
    mock_changes,
    use_case: UpdateBlogPost
):
    post_id = uuid4()
    user_id = uuid4()
    blog_id = uuid4()
    not_my_blog = Blog(
        blog_id=blog_id,
        user_id=uuid4(),
        name="...",
        description="...",
        created_at=datetime.now()
    )
    fake_post = BlogPost(
        post_id=post_id,
        blog_id=blog_id,
        category_id=None,
        author="me",
        title="old title",
        content_1="...",
        content_2="...",
        images=None,
        published=True,
        published_at=datetime.now(),
        created_at=datetime.now(),
        blog=not_my_blog
    )

    mock_repository.get_one.return_value = fake_post

    with pytest.raises(PermissionsException) as exc_info:
        use_case.execute(
            user_id=user_id,
            post_id=post_id,
            changes=mock_changes
        )

    mock_repository.get_one.assert_called_once_with(
        key="post_id",
        value=post_id
    )
    mock_repository.update.assert_not_called()
    assert "Forbidden" in str(exc_info)