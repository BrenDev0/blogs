import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime
from src.security.domain.exceptions import PermissionsException
from src.features.posts.application.use_cases.collection import GetBlogPostCollection
from src.features.posts.domain.entities import BlogPost
from src.features.blogs.domain.entities import Blog


@pytest.fixture
def mock_repistory():
    return Mock()

@pytest.fixture
def use_case(
    mock_repistory
):
    return GetBlogPostCollection(
        post_repository=mock_repistory
    )

def test_success_no_drafts(
    mock_repistory,
    use_case: GetBlogPostCollection
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

    fake_collection = [
        BlogPost(
            post_id=uuid4(),
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
        ),
        BlogPost(
            post_id=uuid4(),
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
]
    mock_repistory.get_many.return_value = fake_collection
    
    result = use_case.execute(
        user_id=user_id,
        blog_id=blog_id,
        include_drafts=False
    )

    mock_repistory.get_many.assert_called_with(
        key="blog_id",
        value=blog_id
    )

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].title == "published"

def test_success_with_drafts(
    mock_repistory,
    use_case: GetBlogPostCollection
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

    fake_collection = [
        BlogPost(
            post_id=uuid4(),
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
        ),
        BlogPost(
            post_id=uuid4(),
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
]
    mock_repistory.get_many.return_value = fake_collection
    
    result = use_case.execute(
        user_id=user_id,
        blog_id=blog_id,
        include_drafts=True
    )

    mock_repistory.get_many.assert_called_with(
        key="blog_id",
        value=blog_id
    )

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].title == "published"
    assert result[1].title == "draft"


def test_no_results(
    mock_repistory,
    use_case: GetBlogPostCollection
):
    user_id = uuid4()
    blog_id = uuid4()

    mock_repistory.get_many.return_value = None
    
    result = use_case.execute(
        user_id=user_id,
        blog_id=blog_id,
        include_drafts=False
    )

    mock_repistory.get_many.assert_called_with(
        key="blog_id",
        value=blog_id
    )

    assert isinstance(result, list)
    assert len(result) == 0


def test_permission_error(
    mock_repistory,
    use_case: GetBlogPostCollection
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

    fake_collection = [
        BlogPost(
            post_id=uuid4(),
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
        ),
        BlogPost(
            post_id=uuid4(),
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
]
    mock_repistory.get_many.return_value = fake_collection
    
    with pytest.raises(PermissionsException) as exc_info:
        use_case.execute(
            user_id=user_id,
            blog_id=blog_id,
            include_drafts=False
        )

    mock_repistory.get_many.assert_called_with(
        key="blog_id",
        value=blog_id
    )

    assert "Forbidden" in str(exc_info)
