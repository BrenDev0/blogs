import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime
from src.features.comments.application.use_cases.collection import CommentsCollection
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
    return CommentsCollection(
        comment_repository=mock_comment_repository,
        post_repositry=mock_post_repository
    )

def test_success_only_approved(
    mock_comment_repository,
    mock_post_repository,
    use_case: CommentsCollection
):
    post_id = uuid4()
    fake_comments = [
        Comment(
            comment_id=uuid4(),
            post_id=post_id,
            text="approved",
            approved=True,
            created_at=datetime.now()
        ),
        Comment(
            comment_id=uuid4(),
            post_id=post_id,
            text="not approved",
            approved=False,
            created_at=datetime.now()
        )
    ]
    mock_comment_repository.get_many.return_value = fake_comments

    result = use_case.execute(
        post_id=post_id,
        include_unapproved=False
    )

    mock_comment_repository.get_many.assert_called_with(
        key="post_id",
        value=post_id
    )
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].approved is True

def test_success_include_unapproved(
    mock_comment_repository,
    mock_post_repository,
    use_case: CommentsCollection
):
    post_id = uuid4()
    user_id = uuid4()
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
            text="approved",
            approved=True,
            created_at=datetime.now()
        ),
        Comment(
            comment_id=uuid4(),
            post_id=post_id,
            text="not approved",
            approved=False,
            created_at=datetime.now()
        )
    ]
    mock_comment_repository.get_many.return_value = fake_comments
    mock_post_repository.get_one.return_value = fake_post

    result = use_case.execute(
        post_id=post_id,
        user_id=user_id,
        include_unapproved=True
    )

    mock_comment_repository.get_many.assert_called_with(
        key="post_id",
        value=post_id
    )
    mock_post_repository.get_one.assert_called_with(
        key="post_id",
        value=post_id
    )
    assert isinstance(result, list)
    assert len(result) == 2

def test_no_results(
    mock_comment_repository,
    mock_post_repository,
    use_case: CommentsCollection
):
    post_id = uuid4()
    mock_comment_repository.get_many.return_value = None

    result = use_case.execute(
        post_id=post_id,
        include_unapproved=False
    )

    mock_comment_repository.get_many.assert_called_with(
        key="post_id",
        value=post_id
    )
    assert isinstance(result, list)
    assert len(result) == 0

def test_permission_error(
    mock_comment_repository,
    mock_post_repository,
    use_case: CommentsCollection
):
    post_id = uuid4()
    user_id = uuid4()
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

    fake_comments = [
        Comment(
            comment_id=uuid4(),
            post_id=post_id,
            text="approved",
            approved=True,
            created_at=datetime.now()
        )
    ]
    mock_comment_repository.get_many.return_value = fake_comments
    mock_post_repository.get_one.return_value = fake_post

    with pytest.raises(PermissionsException) as exc_info:
        use_case.execute(
            post_id=post_id,
            user_id=user_id,
            include_unapproved=True
        )

    mock_comment_repository.get_many.assert_called_with(
        key="post_id",
        value=post_id
    )
    mock_post_repository.get_one.assert_called_with(
        key="post_id",
        value=post_id
    )
    assert "Forbidden" in str(exc_info.value)

def test_post_not_found(
    mock_comment_repository,
    mock_post_repository,
    use_case: CommentsCollection
):
    post_id = uuid4()
    user_id = uuid4()
    fake_comments = [
        Comment(
            comment_id=uuid4(),
            post_id=post_id,
            text="approved",
            approved=True,
            created_at=datetime.now()
        )
    ]
    mock_comment_repository.get_many.return_value = fake_comments
    mock_post_repository.get_one.return_value = None

    with pytest.raises(Exception) as exc_info:
        use_case.execute(
            post_id=post_id,
            user_id=user_id,
            include_unapproved=True
        )

    mock_comment_repository.get_many.assert_called_with(
        key="post_id",
        value=post_id
    )
    mock_post_repository.get_one.assert_called_with(
        key="post_id",
        value=post_id
    )
    # Should have deleted all comments
    for comment in fake_comments:
        mock_comment_repository.delete.assert_any_call(
            key="comment_id",
            value=comment.comment_id
        )
    assert "Comments unavailbale" in str(exc_info.value)