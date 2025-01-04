from src.repositories.categories import CategoryRepository
from src.repositories.items import ItemRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory
        
        self.categories: CategoryRepository | None = None
        self.items: ItemRepository | None = None
        
    async def __aenter__(self):
        self.session = self.session_factory()
        
        self.categories = CategoryRepository(self.session)
        self.items = ItemRepository(self.session)
        
        return self
    
    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()
        
    async def commit(self):
        await self.session.commit()
        
    