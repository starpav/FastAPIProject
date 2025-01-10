from src.schemas.categories import SCategory, SCategoryCreate, SCategoryRel
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool


async def test_create_category(db):
    category_data = SCategoryCreate(name="Test Category")
    
    new_id: int = await db.categories.add(category_data)
    print("Добавлена новая категория с id: ", new_id)
    categories: SCategory = await db.categories.get_all()
    print(categories)
    category_data = SCategoryCreate(name="Updated Test Category")
    await db.categories.update(category_data, id=new_id, exclude_unset=True)
    new_category: SCategory = await db.categories.get_one_or_none(id=new_id)
    print(new_category)
    await db.categories.delete(id=new_id)
    categories: SCategoryRel = await db.categories.get_all_with_subcategories()
    print(categories)
    await db.commit()