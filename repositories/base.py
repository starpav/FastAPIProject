from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update


class BaseRepository:
    model = None
    
    def __init__(self, session):
        self.session = session
        
    async def get_all(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
    
    async def add(self, data: BaseModel):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().one()
    
    async def update(self, id: int, data: BaseModel):
        # Преобразуем данные из Pydantic-схемы, исключая unset (непереданные значения)
        data_dict = data.model_dump(exclude_unset=True)

        # Проверяем, что есть данные для обновления
        if not data_dict:
            return {"error": "No data provided for update"}

        # Поиск сущности по id
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        entity = result.scalar_one_or_none()

        if not entity:
            return {"error": "Item not found"}

        # Выполняем обновление
        update_stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**data_dict)
            .returning(self.model)
        )
        update_result = await self.session.execute(update_stmt)

        # Возвращаем обновленную запись
        return update_result.scalars().one_or_none()
    
    async def delete(self, id: int):
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        entity = result.scalar_one_or_none()

        if not entity:
            return {"error": "Item not found"}

        delete_stmt = (
            delete(self.model)
            .where(self.model.id == id)
        )
        await self.session.execute(delete_stmt)


