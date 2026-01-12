import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime
from src.security.domain.exceptions import PermissionsException
from src.persistence.domain.exceptions import NotFoundException
from src.features.images.application.use_cases.collection import ImageCollection
from src.features.images.domain.entities import Image
from src.features.images.domain.schemas import ImagePublic
from src.features.posts.domain.entities import BlogPost
from src.features.blogs.domain.entities import Blog

@pytest.fixture
def mock_image_data_repository():
    return Mock()

@pytest.fixture
def mock_post_repository():
    return Mock()

@pytest.fixture
def use_case(
    mock_image_data_repository,
    mock_post_repository
):
    return ImageCollection(
        image_data_repository=mock_image_data_repository,
        post_repository=mock_post_repository
    )

def test_success_published(
    mock_image_data_repository,
    mock_post_repository,
    use_case
):
    user_id = uuid4()
    blog_id = uuid4()
    post_id = uuid4()

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
        title="published",
        content_1="...",
        content_2="...",
        images=None,
        published=True,
        published_at=datetime.now(),
        created_at=datetime.now(),
        blog=fake_blog
    )

    fake_images = [
        Image(
            image_id=uuid4(),
            post_id=post_id,
            url="https://...",
            uploaded_at=datetime.now()
        )
    ]

    mock_post_repository.get_one.return_value = fake_post
    mock_image_data_repository.get_many.return_value = fake_images

    result = use_case.execte(
        post_id=post_id,
        include_drafts=False
    )

    mock_post_repository.get_one.assert_called_once_with(
        key="post_id",
        value=post_id
    )
    mock_image_data_repository.get_many.assert_called_once_with(
        key="post_id",
        value=post_id
    )
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], ImagePublic)

def test_success_drafts(
    mock_image_data_repository,
    mock_post_repository,
    use_case
):
    user_id = uuid4()
    blog_id = uuid4()
    post_id = uuid4()

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
        title="draft",
        content_1="...",
        content_2="...",
        images=None,
        published=False,
        published_at=datetime.now(),
        created_at=datetime.now(),
        blog=fake_blog
    )

    fake_images = [
        Image(
            image_id=uuid4(),
            post_id=post_id,
            url="https://...",
            uploaded_at=datetime.now()
        )
    ]

    mock_post_repository.get_one.return_value = fake_post
    mock_image_data_repository.get_many.return_value = fake_images

    result = use_case.execte(
        post_id=post_id,
        user_id=user_id,
        include_drafts=True
    )

    mock_post_repository.get_one.assert_called_once_with(
        key="post_id",
        value=post_id
    )
    mock_image_data_repository.get_many.assert_called_once_with(
        key="post_id",
        value=post_id
    )
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], ImagePublic)

def test_not_found(
    mock_post_repository,
    mock_image_data_repository,
    use_case
):
    post_id = uuid4()
    mock_post_repository.get_one.return_value = None

    with pytest.raises(NotFoundException):
        use_case.execte(
            post_id=post_id,
            include_drafts=False
        )

    mock_post_repository.get_one.assert_called_once_with(
        key="post_id",
        value=post_id
    )

    mock_image_data_repository.get_many.assert_not_called()

def test_permission_error_draft(
    mock_post_repository,
    mock_image_data_repository,
    use_case
):
    user_id = uuid4()
    blog_id = uuid4()
    post_id = uuid4()

    fake_blog = Blog(
        blog_id=blog_id,
        user_id=uuid4(),  # Not the same as user_id
        name="...",
        description="...",
        created_at=datetime.now()
    )

    fake_post = BlogPost(
        post_id=post_id,
        blog_id=blog_id,
        category_id=None,
        author="me",
        title="draft",
        content_1="...",
        content_2="...",
        images=None,
        published=False,
        published_at=datetime.now(),
        created_at=datetime.now(),
        blog=fake_blog
    )

    mock_post_repository.get_one.return_value = fake_post

    with pytest.raises(PermissionsException):
        use_case.execte(
            post_id=post_id,
            user_id=user_id,
            include_drafts=True
        )

    mock_post_repository.get_one.assert_called_once_with(
        key="post_id",
        value=post_id
    )

    mock_image_data_repository.get_many.assert_not_called()

def test_permission_error_unpublished(
    mock_post_repository,
    mock_image_data_repository,
    use_case
):
    post_id = uuid4()
    blog_id = uuid4()
    user_id = uuid4()

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
        title="unpublished",
        content_1="...",
        content_2="...",
        images=None,
        published=False,
        published_at=datetime.now(),
        created_at=datetime.now(),
        blog=fake_blog
    )

    mock_post_repository.get_one.return_value = fake_post

    with pytest.raises(PermissionsException):
        use_case.execte(
            post_id=post_id,
            include_drafts=False
        )

    mock_post_repository.get_one.assert_called_once_with(
        key="post_id",
        value=post_id
    )

    mock_image_data_repository.get_many.assert_not_called()
    