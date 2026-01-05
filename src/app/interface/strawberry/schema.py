import strawberry
from src.features.users.interface.strawberry.queries import UserQueries
from src.features.users.interface.strawberry.mutations import UserMutations
from src.features.email.interface.strawberry.mutations import EmailMutations
from src.features.blogs.interface.strawberry.queries import BlogQueries
from src.features.blogs.interface.strawberry.mutations import BlogMutations
from src.features.categories.interface.strawberry.queries import CategoryQueries
from src.features.categories.interface.strawberry.mutations import CategoryMutation

@strawberry.type
class Query():
    @strawberry.field
    def users(self) -> UserQueries:
        return UserQueries()
    
    @strawberry.field
    def blogs(self) -> BlogQueries:
        return BlogQueries()
    
    @strawberry.field
    def categories(self) -> CategoryQueries:
        return CategoryQueries()


@strawberry.type
class Mutation():
    @strawberry.field
    def email(self) -> EmailMutations:
        return EmailMutations()

    @strawberry.field
    def users(self) -> UserMutations:
        return UserMutations()
    
    @strawberry.field
    def blogs(self) -> BlogMutations:
        return BlogMutations()
    
    @strawberry.field
    def categories(self) -> CategoryMutation:
        return CategoryMutation()
    

schema = strawberry.Schema(query=Query, mutation=Mutation)