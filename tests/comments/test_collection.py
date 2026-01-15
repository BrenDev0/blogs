import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime
from src.features.comments.application.use_cases.collection import CommentsCollection
from src.features.comments.domain.entities import Comment
from src.features.posts.domain.entities import BlogPost, Blog
from src.persistence.domain.exceptions import NotFoundException, InvalidScopeException, PagationException, InvalidFilterException
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
        post_repository=mock_post_repository
    )

def test_success_public_post_scope(
    mock_comment_repository,
    mock_post_repository,
    use_case: CommentsCollection
):
    post_id = uuid4()
    fake_comments = [
        Comment(
            comment_id=uuid4(),
            post_id=post_id,
            text="approved comment 1",
            approved=True,
            created_at=datetime.now()
        ),
        Comment(
            comment_id=uuid4(),
            post_id=post_id,
            text="approved comment 2",
            approved=True,
            created_at=datetime.now()
        )
    ]
    mock_comment_repository.get_many.return_value = fake_comments

    result = use_case.execute(
        per_page=10,
        page_number=1,
        scope="post",
        scope_id=post_id,
        protected=False
    )

    mock_comment_repository.get_many.assert_called_with(
        key="post_id",
        value=post_id,
        limit=10,
        offset=0,
        secondary_key="approved",
        secondary_value=True
    )
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(comment.approved for comment in result)

def test_success_protected_post_scope_no_filter(
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
    mock_post_repository.get_one.return_value = fake_post
    mock_comment_repository.get_many.return_value = fake_comments

    result = use_case.execute(
        per_page=10,
        page_number=1,
        scope="post",
        scope_id=post_id,
        user_id=user_id,
        protected=True,
        filter_results=False
    )

    mock_post_repository.get_one.assert_called_with(
        key="post_id",
        value=post_id
    )
    mock_comment_repository.get_many.assert_called_with(
        key="post_id",
        value=post_id,
        limit=10,
        offset=0
    )
    assert isinstance(result, list)
    assert len(result) == 2

def test_success_protected_post_scope_with_filter(
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
        )
    ]
    mock_post_repository.get_one.return_value = fake_post
    mock_comment_repository.get_many.return_value = fake_comments

    result = use_case.execute(
        per_page=10,
        page_number=1,
        scope="post",
        scope_id=post_id,
        user_id=user_id,
        protected=True,
        filter_results=True,
        filter="approved",
        filter_value=True
    )

    mock_post_repository.get_one.assert_called_with(
        key="post_id",
        value=post_id
    )
    mock_comment_repository.get_many.assert_called_with(
        key="post_id",
        value=post_id,
        limit=10,
        offset=0,
        secondary_key="approved",
        secondary_value=True
    )
    assert isinstance(result, list)
    assert len(result) == 1

def test_success_blog_scope_no_filter(
    mock_comment_repository,
    mock_post_repository,
    use_case: CommentsCollection
):
    blog_id = uuid4()
    user_id = uuid4()
    post1_id = uuid4()
    post2_id = uuid4()
    
    fake_posts = [
        BlogPost(
            post_id=post1_id,
            blog_id=blog_id,
            category_id=None,
            author="author",
            title="title 1",
            content_1="c1",
            content_2="c2",
            images=None,
            published=True,
            published_at=datetime.now(),
            created_at=datetime.now()
        ),
        BlogPost(
            post_id=post2_id,
            blog_id=blog_id,
            category_id=None,
            author="author",
            title="title 2",
            content_1="c1",
            content_2="c2",
            images=None,
            published=True,
            published_at=datetime.now(),
            created_at=datetime.now()
        )
    ]

    fake_comments = [
        Comment(
            comment_id=uuid4(),
            post_id=post1_id,
            text="comment 1",
            approved=True,
            created_at=datetime.now()
        ),
        Comment(
            comment_id=uuid4(),
            post_id=post2_id,
            text="comment 2",
            approved=False,
            created_at=datetime.now()
        )
    ]
    
    mock_post_repository.get_many.return_value = fake_posts
    mock_comment_repository.get_many.return_value = fake_comments

    result = use_case.execute(
        per_page=10,
        page_number=1,
        scope="blog",
        scope_id=blog_id,
        user_id=user_id,
        protected=True,
        filter_results=False
    )

    mock_post_repository.get_many.assert_called_with(
        key="blog_id",
        value=blog_id
    )
    mock_comment_repository.get_many.assert_called_with(
        key="post_id",
        value=[post1_id, post2_id],
        limit=10,
        offset=0
    )
    assert isinstance(result, list)
    assert len(result) == 2

def test_success_blog_scope_with_filter(
    mock_comment_repository,
    mock_post_repository,
    use_case: CommentsCollection
):
    blog_id = uuid4()
    user_id = uuid4()
    post1_id = uuid4()
    post2_id = uuid4()
    
    fake_posts = [
        BlogPost(
            post_id=post1_id,
            blog_id=blog_id,
            category_id=None,
            author="author",
            title="title 1",
            content_1="c1",
            content_2="c2",
            images=None,
            published=True,
            published_at=datetime.now(),
            created_at=datetime.now()
        ),
        BlogPost(
            post_id=post2_id,
            blog_id=blog_id,
            category_id=None,
            author="author",
            title="title 2",
            content_1="c1",
            content_2="c2",
            images=None,
            published=True,
            published_at=datetime.now(),
            created_at=datetime.now()
        )
    ]

    fake_comments = [
        Comment(
            comment_id=uuid4(),
            post_id=post1_id,
            text="comment 1",
            approved=True,
            created_at=datetime.now()
        )
    ]
    
    mock_post_repository.get_many.return_value = fake_posts
    mock_comment_repository.get_many.return_value = fake_comments

    result = use_case.execute(
        per_page=10,
        page_number=1,
        scope="blog",
        scope_id=blog_id,
        user_id=user_id,
        protected=True,
        filter_results=True,
        filter="approved",
        filter_value=True
    )

    mock_post_repository.get_many.assert_called_with(
        key="blog_id",
        value=blog_id
    )
    mock_comment_repository.get_many.assert_called_with(
        key="post_id",
        value=[post1_id, post2_id],
        limit=10,
        offset=0,
        secondary_key="approved",
        secondary_value=True
    )
    assert isinstance(result, list)
    assert len(result) == 1

def test_pagination_offset_calculation(
    mock_comment_repository,
    mock_post_repository,
    use_case: CommentsCollection
):
    post_id = uuid4()
    mock_comment_repository.get_many.return_value = []

    use_case.execute(
        per_page=10,
        page_number=3,
        scope="post",
        scope_id=post_id,
        protected=False
    )

    mock_comment_repository.get_many.assert_called_with(
        key="post_id",
        value=post_id,
        limit=10,
        offset=20,  # (3-1) * 10
        secondary_key="approved",
        secondary_value=True
    )

def test_invalid_scope(
    mock_comment_repository,
    mock_post_repository,
    use_case: CommentsCollection
):
    post_id = uuid4()

    with pytest.raises(InvalidScopeException) as exc_info:
        use_case.execute(
            per_page=10,
            page_number=1,
            scope="invalid_scope",
            scope_id=post_id,
            protected=False
        )

    assert "not  allowed" in str(exc_info.value)

def test_invalid_page_number(
    mock_comment_repository,
    mock_post_repository,
    use_case: CommentsCollection
):
    post_id = uuid4()

    with pytest.raises(PagationException) as exc_info:
        use_case.execute(
            per_page=10,
            page_number=0,
            scope="post",
            scope_id=post_id,
            protected=False
        )

    assert "cannot be lower than 1" in str(exc_info.value)

def test_protected_without_user_id(
    mock_comment_repository,
    mock_post_repository,
    use_case: CommentsCollection
):
    post_id = uuid4()

    with pytest.raises(ValueError) as exc_info:
        use_case.execute(
            per_page=10,
            page_number=1,
            scope="post",
            scope_id=post_id,
            protected=True
        )

    assert "User id required" in str(exc_info.value)

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
        user_id=uuid4(),  # Different user
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

    with pytest.raises(PermissionsException):
        use_case.execute(
            per_page=10,
            page_number=1,
            scope="post",
            scope_id=post_id,
            user_id=user_id,
            protected=True
        )

def test_invalid_filter(
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

    mock_post_repository.get_one.return_value = fake_post

    with pytest.raises(InvalidFilterException) as exc_info:
        use_case.execute(
            per_page=10,
            page_number=1,
            scope="post",
            scope_id=post_id,
            user_id=user_id,
            protected=True,
            filter_results=True,
            filter="invalid_filter",
            filter_value="value"
        )

    assert "not availbe" in str(exc_info.value)