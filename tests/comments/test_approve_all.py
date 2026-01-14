import pytest
from uuid import uuid4
from datetime import datetime
from unittest.mock import Mock
from src.features.comments.application.use_cases.approve_all import ApproveAllComments
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
    return ApproveAllComments(
        comment_repository=mock_comment_repository,
        post_repository=mock_post_repository
    )

def test_success_approve_all(
    mock_comment_repository,
    mock_post_repository,
    use_case: ApproveAllComments
):
    user_id = uuid4()
    post_id = uuid4()
    blog_id = uuid4()

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

    fake_comments = [
        Comment(
            comment_id=uuid4(),
            post_id=post_id,
            text="comment1",
            approved=True,
            created_at=datetime.now()
        ),
        Comment(
            comment_id=uuid4(),
            post_id=post_id,
            text="comment2",
            approved=True,
            created_at=datetime.now()
        )
    ]

    mock_post_repository.get_one.return_value = fake_post
    mock_comment_repository.update_many.return_value = fake_comments

    result = use_case.execute(
        post_id=post_id,
        user_id=user_id
    )

    mock_post_repository.get_one.assert_called_once_with(
        key="post_id",
        value=post_id
    )
    mock_comment_repository.update_many.assert_called_once_with(
        key="post_id",
        value=post_id,
        changes={"approved": True}
    )
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(c.approved for c in result)

def test_post_not_found(
    mock_comment_repository,
    mock_post_repository,
    use_case: ApproveAllComments
):
    user_id = uuid4()
    post_id = uuid4()
    mock_post_repository.get_one.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
        use_case.execute(
            post_id=post_id,
            user_id=user_id
        )

    mock_post_repository.get_one.assert_called_once_with(
        key="post_id",
        value=post_id
    )
    mock_comment_repository.update_many.assert_not_called()
    assert "Post not found" in str(exc_info.value)

def test_permission_error(
    mock_comment_repository,
    mock_post_repository,
    use_case: ApproveAllComments
):
    user_id = uuid4()
    post_id = uuid4()
    blog_id = uuid4()

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

    mock_post_repository.get_one.return_value = fake_post

    with pytest.raises(PermissionsException) as exc_info:
        use_case.execute(
            post_id=post_id,
            user_id=user_id
        )

    mock_post_repository.get_one.assert_called_once_with(
        key="post_id",
        value=post_id
    )
    mock_comment_repository.update_many.assert_not_called()
    assert "Forbidden" in str(exc_info.value)