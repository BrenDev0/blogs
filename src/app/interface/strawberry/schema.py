import strawberry
from starlette.datastructures import UploadFile
from strawberry.file_uploads import Upload
from src.features.users.interface.strawberry import queries as user_queries, mutations as user_mutations
from src.features.email.interface.strawberry.mutations import EmailMutations
from src.features.blogs.interface.strawberry import queries as blog_queries, mutations as blog_mutations
from src.features.categories.interface.strawberry import queries as category_queries, mutations as category_mutations
from src.features.posts.interface.strawberry import mutations as blog_post_mutations

@strawberry.type
class Query():
    @strawberry.field
    def users(self) -> user_queries.UserQueries:
        return user_queries.UserQueries()
    
    @strawberry.field
    def blogs(self) -> blog_queries.BlogQueries:
        return blog_queries.BlogQueries()
    
    @strawberry.field
    def categories(self) -> category_queries.CategoryQueries:
        return category_queries.CategoryQueries()


@strawberry.type
class Mutation():
    @strawberry.field
    def email(self) -> EmailMutations:
        return EmailMutations()

    @strawberry.field
    def users(self) -> user_mutations.UserMutations:
        return user_mutations.UserMutations()
    
    @strawberry.field
    def blogs(self) -> blog_mutations.BlogMutations:
        return blog_mutations.BlogMutations()
    
    @strawberry.field
    def categories(self) -> category_mutations.CategoryMutation:
        return category_mutations.CategoryMutation()
    
    @strawberry.field
    def blog_posts(self) -> blog_post_mutations.BlogPostMutations:
        return blog_post_mutations.BlogPostMutations()
    

schema = strawberry.Schema(
    query=Query, 
    mutation=Mutation,
    scalar_overrides={UploadFile: Upload}
)