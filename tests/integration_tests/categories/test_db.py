from src.schemas.categories import SCategoryCreate
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool


async def test_create_category():
    category_data = SCategoryCreate(name="Test Category")
    
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.categories.add(category_data)
        await db.commit()