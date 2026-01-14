import pytest
from uuid import uuid4
from datetime import datetime
from unittest.mock import Mock
from src.features.comments.application.use_cases.delete import DeleteComment
from src.features.comments.domain.entities import Comment
from src.features.posts.domain.entities import BlogPost, Blog
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException

@pytest.fixture
def mock_comment_repository():
    return Mock()

@pytest.fixture
def mock_post_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_comment_repository,
    mock_post_repository
):
    return DeleteComment(
        comment_repository=mock_comment_repository,
        post_repository=mock_post_repository
    )

def test_success(
    mock_comment_repository,
    mock_post_repository,
    use_case: DeleteComment
):
    user_id = uuid4()
    comment_id = uuid4()
    post_id = uuid4()
    blog_id = uuid4()

    fake_comment = Comment(
        comment_id=comment_id,
        post_id=post_id,
        text="test",
        approved=False,
        created_at=datetime.now()
    )
    fake_blog = Blog(
        blog_id=blog_id,
        user_id=user_id,
        name="blog",
        description="desc",
        created_at=datetime.now()
    )
    fake_post = BlogPost(
        post_id=post_id,
        blog_id=blog_id,
        category_id=None,
        author="author",
        title="title",
        content_1="c1",
        content_2="c2",
        images=None,
        published=True,
        published_at=datetime.now(),
        created_at=datetime.now()
    )
    fake_post.blog = fake_blog

    mock_comment_repository.get_one.return_value = fake_comment
    mock_post_repository.get_one.return_value = fake_post
    mock_comment_repository.delete.return_value = fake_comment

    result = use_case.execute(
        user_id=user_id,
        comment_id=comment_id
    )

    mock_comment_repository.get_one.assert_called_once_with(
        key="comment_id",
        value=comment_id
    )
    mock_post_repository.get_one.assert_called_once_with(
        key="post_id",
        value=post_id
    )
    mock_comment_repository.delete.assert_called_once_with(
        key="comment_id",
        value=comment_id
    )
    assert result.comment_id == comment_id
    assert result.post_id == post_id

def test_comment_not_found(
    mock_comment_repository,
    mock_post_repository,
    use_case: DeleteComment
):
    user_id = uuid4()
    comment_id = uuid4()
    mock_comment_repository.get_one.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
        use_case.execute(
            user_id=user_id,
            comment_id=comment_id
        )

    mock_comment_repository.get_one.assert_called_once_with(
        key="comment_id",
        value=comment_id
    )
    mock_post_repository.get_one.assert_not_called()
    mock_comment_repository.delete.assert_not_called()
    assert "Comment not found" in str(exc_info.value)

def test_post_not_found(
    mock_comment_repository,
    mock_post_repository,
    use_case: DeleteComment
):
    user_id = uuid4()
    comment_id = uuid4()
    post_id = uuid4()
    fake_comment = Comment(
        comment_id=comment_id,
        post_id=post_id,
        text="test",
        approved=False,
        created_at=datetime.now()
    )
    mock_comment_repository.get_one.return_value = fake_comment
    mock_post_repository.get_one.return_value = None

    result = None
    with pytest.raises(NotFoundException) as exc_info:
        use_case.execute(
            user_id=user_id,
            comment_id=comment_id
        )

    mock_comment_repository.get_one.assert_called_once_with(
        key="comment_id",
        value=comment_id
    )
    mock_post_repository.get_one.assert_called_once_with(
        key="post_id",
        value=post_id
    )
    mock_comment_repository.delete.assert_called_once_with(
        key=comment_id,
        value=comment_id
    )
    assert "Comment unavailable" in str(exc_info.value)

def test_permission_error(
    mock_comment_repository,
    mock_post_repository,
    use_case: DeleteComment
):
    user_id = uuid4()
    comment_id = uuid4()
    post_id = uuid4()
    blog_id = uuid4()

    fake_comment = Comment(
        comment_id=comment_id,
        post_id=post_id,
        text="test",
        approved=False,
        created_at=datetime.now()
    )
    fake_blog = Blog(
        blog_id=blog_id,
        user_id=uuid4(),  # not the same as user_id
        name="blog",
        description="desc",
        created_at=datetime.now()
    )
    fake_post = BlogPost(
        post_id=post_id,
        blog_id=blog_id,
        category_id=None,
        author="author",
        title="title",
        content_1="c1",
        content_2="c2",
        images=None,
        published=True,
        published_at=datetime.now(),
        created_at=datetime.now()
    )
    fake_post.blog = fake_blog

    mock_comment_repository.get_one.return_value = fake_comment
    mock_post_repository.get_one.return_value = fake_post

    with pytest.raises(PermissionsException) as exc_info:
        use_case.execute(
            user_id=user_id,
            comment_id=comment_id
        )

    mock_comment_repository.get_one.assert_called_once_with(
        key="comment_id",
        value=comment_id
    )
    mock_post_repository.get_one.assert_called_once_with(
        key="post_id",
        value=post_id
    )
    mock_comment_repository.delete.assert_not_called()
    assert "Forbidden" in str(exc_info.value)