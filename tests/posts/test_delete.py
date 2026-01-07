import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException
from src.features.posts.application.use_cases.delete import DeleteBlogPost
from src.features.posts.domain.entities import BlogPost
from src.features.blogs.domain.entities import Blog


@pytest.fixture
def mock_repistory():
    return Mock()

@pytest.fixture
def use_case(
    mock_repistory
):
    return DeleteBlogPost(
        post_repository=mock_repistory
    )

def test_success(
    mock_repistory,
    use_case: DeleteBlogPost
):
    user_id = uuid4()
    post_id = uuid4()
    blog_id = uuid4()

    fake_blog = Blog(
        blog_id=blog_id,
        user_id=user_id,
        name="...",
        description="....",
        created_at=datetime.now()
    )

    fake_post = BlogPost(
        post_id=post_id,
        blog_id=blog_id,
        category_id=None,
        author="me",
        title="test",
        content_1="...",
        content_2="...",
        images=None,
        published=True,
        published_at=datetime.now(),
        created_at=datetime.now(),
        blog=fake_blog
    )

    mock_repistory.get_one.return_value = fake_post
    mock_repistory.delete.return_value = fake_post

    result = use_case.execute(
        user_id=user_id,
        post_id=post_id
    )

    mock_repistory.get_one.assert_called_with(
        key="post_id",
        value=post_id
    )

    mock_repistory.delete.assert_called_once_with(
        key="post_id",
        value=post_id
    )

    assert result.post_id == post_id


def test_not_found(
    mock_repistory,
    use_case: DeleteBlogPost
):
    user_id = uuid4()
    post_id = uuid4()
    blog_id = uuid4()


    mock_repistory.get_one.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
        use_case.execute(
            user_id=user_id,
            post_id=post_id
        )

    mock_repistory.get_one.assert_called_with(
        key="post_id",
        value=post_id
    )

    mock_repistory.delete.assert_not_called()

    assert "Post not found" in str(exc_info)

def test_permission_error(
    mock_repistory,
    use_case: DeleteBlogPost
):
    user_id = uuid4()
    post_id = uuid4()
    blog_id = uuid4()

    not_my_fake_blog = Blog(
        blog_id=blog_id,
        user_id=uuid4(),
        name="...",
        description="....",
        created_at=datetime.now()
    )

    fake_post = BlogPost(
        post_id=post_id,
        blog_id=blog_id,
        category_id=None,
        author="me",
        title="test",
        content_1="...",
        content_2="...",
        images=None,
        published=True,
        published_at=datetime.now(),
        created_at=datetime.now(),
        blog=not_my_fake_blog
    )

    mock_repistory.get_one.return_value = fake_post

    with pytest.raises(PermissionsException) as exc_info:
        use_case.execute(
            user_id=user_id,
            post_id=post_id
        )

    mock_repistory.get_one.assert_called_with(
        key="post_id",
        value=post_id
    )

    mock_repistory.delete.assert_not_called()

    assert "Forbidden" in str(exc_info)