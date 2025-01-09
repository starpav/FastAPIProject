from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update

from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None
    
    def __init__(self, session):
        self.session = session
        
    async def get_all(self, *args, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(entity) for entity in result.scalars().all()]
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        entity = result.scalars().one_or_none()
        if entity:
            return self.mapper.map_to_domain_entity(entity)
        else:
            return None
    
    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model.id)
        result = await self.session.execute(stmt)
        new_entity_id = result.scalar_one()
        return new_entity_id
    
    async def update(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset = exclude_unset))
        )
        await self.session.execute(update_stmt)

    
    async def delete(self, **filter_by):
        delete_stmt = (
            delete(self.model)
            .filter_by(**filter_by)
        )
        await self.session.execute(delete_stmt)


