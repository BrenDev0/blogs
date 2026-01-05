import strawberry
import logging
from uuid import UUID
from typing import List
from src.app.domain.exceptions import GraphQlException
from src.features.categories.dependencies.use_cases import get_category_collection_use_case
from src.features.categories.interface.strawberry.types import CategoryType
logger = logging.getLogger(__name__)


@strawberry.type
class CategoryQueries:
    @strawberry.field(
        description="Get all categories by user. **Uprotected route**"
    )
    def categories_collection(
        self,
        user_id: UUID
    ) -> List[CategoryType]:
        use_case = get_category_collection_use_case()
        try:
            return use_case.execute(
                user_id=user_id
            )
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()