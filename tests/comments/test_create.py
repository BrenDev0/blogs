import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime
from src.features.comments.application.use_cases.create import CreateComment
from src.features.comments.domain.entities import Comment
from src.features.comments.domain.schemas import CreateCommentRequest, CommentPublic
from src.persistence.domain.exceptions import NotFoundException

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
    return CreateComment(
        comment_repository=mock_comment_repository,
        post_repository=mock_post_repository
    )

def test_success(
    mock_comment_repository,
    mock_post_repository,
    use_case: CreateComment
):
    post_id = uuid4()
    fake_post = Mock()
    mock_post_repository.get_one.return_value = fake_post

    req = CreateCommentRequest(
        post_id=post_id,
        text="Nice post!"
    )

    fake_comment = Comment(
        comment_id=uuid4(),
        post_id=post_id,
        text="Nice post!",
        approved=False,
        created_at=datetime.now()
    )
    mock_comment_repository.create.return_value = fake_comment

    result = use_case.execute(
        post_id=post_id,
        comment=req
    )

    mock_post_repository.get_one.assert_called_with(
        key="post_id",
        value=post_id
    )
    mock_comment_repository.create.assert_called_once()
    assert isinstance(result, CommentPublic)
    assert result.post_id == post_id
    assert result.text == "Nice post!"
    assert result.approved is False

def test_post_not_found(
    mock_comment_repository,
    mock_post_repository,
    use_case: CreateComment
):
    post_id = uuid4()
    mock_post_repository.get_one.return_value = None

    req = CreateCommentRequest(
        post_id=post_id,
        text="Missing post"
    )

    with pytest.raises(NotFoundException) as exc_info:
        use_case.execute(
            post_id=post_id,
            comment=req
        )

    mock_post_repository.get_one.assert_called_with(
        key="post_id",
        value=post_id
    )
    mock_comment_repository.create.assert_not_called()
    assert "Post not found" in str(exc_info.value)