import pytest
from unittest.mock import Mock
from uuid import uuid4
from src.features.blogs.application.use_cases.create import CreateBlog
from src.features.blogs.domain.entities import Blog
from src.features.blogs.domain.schemas import CreateBlogRequest
from datetime import datetime

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_repository
): 
    return CreateBlog(
        repository=mock_repository
    )

def test_success(
    mock_repository,
    use_case: CreateBlog
):
    user_id = uuid4()
    fake_blog = Blog(
        blog_id=uuid4(),
        user_id=user_id,
        name="...n",
        description="...d",
        created_at=datetime.now()
    )

    mock_repository.create.return_value = fake_blog

    req = CreateBlogRequest(
        name="...n",
        description="...d"
    )
    result = use_case.execute(
        user_id=user_id,
        req_data=req
    )

    mock_repository.create.assert_called_once()

    assert result.user_id == user_id