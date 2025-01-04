from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from src.repositories.base import BaseRepository
from src.models.categories import Category
from src.schemas.categories import SCategory, SCategoryRel

class CategoryRepository(BaseRepository):
    model = Category
    schema = SCategory
    
    async def get_all_with_subcategories(self):
        query = select(self.model).options(selectinload(self.model.subcategories))
        result = await self.session.execute(query)
        return [SCategoryRel.model_validate(entity, from_attributes=True) for entity in result.unique().scalars().all()]
    
    
    