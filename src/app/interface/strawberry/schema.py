import strawberry
from src.features.users.interface.strawberry.queries import UserQueries
from src.features.users.interface.strawberry.mutations import UserMutations
from src.features.email.interface.strawberry.mutations import EmailMutations

@strawberry.type
class Query():
    @strawberry.field
    def users(self) -> UserQueries:
        return UserQueries()


@strawberry.type
class Mutation():
    @strawberry.field
    def email(self) -> EmailMutations:
        return EmailMutations()

    @strawberry.field
    def users(self) -> UserMutations:
        return UserMutations()
    

schema = strawberry.Schema(query=Query, mutation=Mutation)