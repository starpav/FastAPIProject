from sqlalchemy import select
from src.repositories.mappers.items import ItemDataMapper
from src.repositories.base import BaseRepository
from src.models.items import Item
from src.schemas.items import SItem

class ItemRepository(BaseRepository):
    model = Item
    mapper = ItemDataMapper
    
    async def get_all(self, 
                      category_id,
                      name,
                      description,
                      price,
                      limit,
                      offset,
    ):
        query = select(Item)
        if category_id:
            query = query.filter(Item.category_id==category_id)
        if name:
            query = query.filter(Item.name.icontains(name))
        if description:
            query = query.filter(Item.description.icontains(description))
        if price:
            query = query.filter(Item.price==price)
        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(entity) for entity in result.scalars().all()]
        