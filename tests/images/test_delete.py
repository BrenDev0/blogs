import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime
from src.features.images.application.use_cases.delete import DeleteImageUpload
from src.features.images.domain.entities import Image
from src.features.images.domain.schemas import ImagePublic
from src.features.posts.domain.entities import BlogPost
from src.features.blogs.domain.entities import Blog
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException

@pytest.fixture
def mock_image_file_repository():
    return Mock()

@pytest.fixture
def mock_image_data_repository():
    return Mock()

@pytest.fixture
def mock_post_data_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_image_file_repository,
    mock_image_data_repository,
    mock_post_data_repository
):
    return DeleteImageUpload(
        image_file_repository=mock_image_file_repository,
        image_data_repository=mock_image_data_repository,
        post_data_repository=mock_post_data_repository
    )

def test_success(
    mock_image_file_repository,
    mock_image_data_repository,
    mock_post_data_repository,
    use_case
):
    user_id = uuid4()
    blog_id = uuid4()
    post_id = uuid4()
    image_id = uuid4()

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
        title="test",
        content_1="...",
        content_2="...",
        images=None,
        published=True,
        published_at=datetime.now(),
        created_at=datetime.now(),
        blog=fake_blog
    )

    fake_image = Image(
        image_id=image_id,
        post_id=post_id,
        url="https://...",
        uploaded_at=datetime.now()
    )

    mock_image_data_repository.get_one.return_value = fake_image
    mock_post_data_repository.get_one.return_value = fake_post
    mock_image_data_repository.delete.return_value = fake_image

    result = use_case.execute(
        user_id=user_id,
        image_id=image_id
    )

    mock_image_data_repository.get_one.assert_called_once_with(
        key="image_id",
        value=image_id
    )
    mock_post_data_repository.get_one.assert_called_once_with(
        key="post_id",
        value=post_id
    )
    mock_image_file_repository.delete.assert_called_once()
    mock_image_data_repository.delete.assert_called_once_with(
        key="image_id",
        value=image_id
    )
    assert result.image_id == image_id

def test_not_found(
    mock_image_data_repository,
    use_case
):
    user_id = uuid4()
    image_id = uuid4()

    mock_image_data_repository.get_one.return_value = None

    with pytest.raises(NotFoundException):
        use_case.execute(
            user_id=user_id,
            image_id=image_id
        )

    mock_image_data_repository.get_one.assert_called_once_with(
        key="image_id",
        value=image_id
    )

def test_permission_error(
    mock_image_data_repository,
    mock_post_data_repository,
    use_case
):
    user_id = uuid4()
    blog_id = uuid4()
    post_id = uuid4()
    image_id = uuid4()

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
        title="test",
        content_1="...",
        content_2="...",
        images=None,
        published=True,
        published_at=datetime.now(),
        created_at=datetime.now(),
        blog=not_my_blog
    )

    fake_image = Image(
        image_id=image_id,
        post_id=post_id,
        url="https://...",
        uploaded_at=datetime.now()
    )

    mock_image_data_repository.get_one.return_value = fake_image
    mock_post_data_repository.get_one.return_value = fake_post

    with pytest.raises(PermissionsException):
        use_case.execute(
            user_id=user_id,
            image_id=image_id
        )

    mock_image_data_repository.get_one.assert_called_once_with(
        key="image_id",
        value=image_id
    )
    mock_post_data_repository.get_one.assert_called_once_with(
        key="post_id",
        value=post_id
    )