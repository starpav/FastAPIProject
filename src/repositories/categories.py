from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from src.repositories.mappers.categories import CategoryDataMapper, CategoryRelDataMapper
from src.repositories.base import BaseRepository
from src.models.categories import Category
from src.schemas.categories import SCategory, SCategoryRel

class CategoryRepository(BaseRepository):
    model = Category
    mapper = CategoryDataMapper
        
    async def get_all_with_subcategories(self):
        query = select(self.model).options(joinedload(self.model.subcategories))
        result = await self.session.execute(query)
        return [CategoryRelDataMapper.map_to_domain_entity(entity) for entity in result.unique().scalars().all()]
    
    
    