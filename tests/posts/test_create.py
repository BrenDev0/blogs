import pytest
from unittest.mock import Mock
from uuid import uuid4 
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException
from src.features.posts.domain.entities import BlogPost
from src.features.posts.domain.schemas import CreateBlogPostRequest
from src.features.blogs.domain.entities import Blog
from src.features.posts.application.use_cases.create import CreateBlogPost
from datetime import datetime


@pytest.fixture
def mock_blog_repository():
    return Mock()

@pytest.fixture
def mock_post_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_blog_repository,
    mock_post_repository
):
    return CreateBlogPost(
        post_repository=mock_post_repository,
        blog_repositroy=mock_blog_repository
    )


def test_success(
    mock_blog_repository,
    mock_post_repository,
    use_case: CreateBlogPost
):
    
    user_id = uuid4()
    blog_id = uuid4()

    fake_blog = Blog(
        blog_id=blog_id,
        user_id=user_id,
        name="...",
        description="....",
        created_at=datetime.now()
    )

    fake_post = BlogPost(
        post_id=uuid4(),
        blog_id=blog_id,
        category_id=None,
        author="me",
        title="test",
        content_1="...",
        content_2="...",
        images=None,
        published=True,
        published_at=datetime.now(),
        created_at=datetime.now()
    )

    mock_blog_repository.get_one.return_value = fake_blog
    mock_post_repository.create.return_value = fake_post

    fake_req = CreateBlogPostRequest(
        author="me",
        title="test",
        content_1="...",
        content_2="...",
        published=True
    )

    result = use_case.execute(
        user_id=user_id,
        blog_id=blog_id,
        req_data=fake_req
    )
    
    mock_blog_repository.get_one.assert_called_with(
        key="blog_id",
        value=blog_id
    )

    mock_post_repository.create.assert_called_once()
    

    assert result.blog_id == blog_id


def test_not_found(
    mock_blog_repository,
    mock_post_repository,
    use_case: CreateBlogPost
):
    
    user_id = uuid4()
    blog_id = uuid4()

   

    mock_blog_repository.get_one.return_value = None

    fake_req = CreateBlogPostRequest(
        author="me",
        title="test",
        content_1="...",
        content_2="...",
        published=True
    )

    with pytest.raises(NotFoundException) as exc_info:
        use_case.execute(
            user_id=user_id,
            blog_id=blog_id,
            req_data=fake_req
        )
    
    mock_blog_repository.get_one.assert_called_with(
        key="blog_id",
        value=blog_id
    )

    mock_post_repository.create.assert_not_called()
    assert "Blog not found" in str(exc_info)


def test_permission_error(
    mock_blog_repository,
    mock_post_repository,
    use_case: CreateBlogPost
):
    
    user_id = uuid4()
    blog_id = uuid4()

    fake_blog = Blog(
        blog_id=blog_id,
        user_id=uuid4(),
        name="...",
        description="....",
        created_at=datetime.now()
    )

 

    mock_blog_repository.get_one.return_value = fake_blog

    fake_req = CreateBlogPostRequest(
        author="me",
        title="test",
        content_1="...",
        content_2="...",
        published=True
    )


    with pytest.raises(PermissionsException) as exc_info:
        use_case.execute(
            user_id=user_id,
            blog_id=blog_id,
            req_data=fake_req
        )
    
    mock_blog_repository.get_one.assert_called_with(
        key="blog_id",
        value=blog_id
    )

    mock_post_repository.create.assert_not_called()
    

    assert "Forbidden" in str(exc_info)