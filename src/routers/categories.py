from fastapi import APIRouter, Query, Path, Body
from sqlalchemy import insert, select
from src.schemas.categories import SCategory, SCategoryCreate
from src.dependencies.pagination import PaginationDep

from src.database import async_session_maker
from src.models.categories import Category
from repositories.categories import CategoryRepository


router = APIRouter(
    prefix="/categories",
    tags=["Категории"]
)

@router.get("", summary="Получить список категорий", description="Получить список всех категорий или результат поиска по названию")
async def get_categories(
        pagination: PaginationDep,
        name: str | None = Query(default=None, description="Название категории"),
):
    offset = (pagination.page - 1) * pagination.per_page
    async with async_session_maker() as session:
        try:
            query = select(Category)
            if name:
                query = query.filter(Category.name.icontains(name))
            query = query.offset(offset).limit(pagination.per_page)
            result = await session.execute(query)
            categories = result.scalars().all()
            return categories
        except Exception as e:
            return {"error": f"Categories not found: {str(e)}"}

@router.get("/{category_id}",  summary="Получить категорию по ID", description="Получить категорию по ее ID")
def get_category(
        category_id: int = Path(description="ID категории")
    ):
    return {"error": "Category not found"}

@router.post("", summary="Добавить категорию")
async def create_category(
        category_data: SCategoryCreate = Body(openapi_examples={
            "1": {
                "summary": "Пример 1",
                "value": {
                    "name": "Автомобили",
                }
            },
            "2": {
                "summary": "Пример 2",
                "value": {
                    "name": "Бытовая техника",
                }
            },
        })
):
    async with async_session_maker() as session:
            try:
                result = await CategoryRepository(session).add(name=category_data.name)
                await session.commit()
                schema = SCategory.model_validate(result)
                return {"message": f"Category created: {schema.model_dump()}"}
            except:
                await session.rollback()
                return {"message": "Category not created"}
    

@router.delete("/{category_id}",  summary="Удалить категорию", description="Удалить категорию по ее ID")
def delete_category(
        category_id: int = Path(description="ID категории")
):
    return {"error": "Category not found"}

@router.put("/{item_id}",  summary="Обновить категорию", description="Обновить полностью информацию о существующей категории по ее ID")
def update_category_put(
        category_id: int = Path(description="ID категории"),
        updated_category: SCategoryCreate = Body(description="Обновленная категория")
):
    return {"error": "Category not found"}
