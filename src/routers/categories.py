from fastapi import APIRouter, Query, Path, Body
from src.schemas.categories import SCategory, SCategoryCreate
from src.dependencies.pagination import PaginationDep

from src.database import async_session_maker
from src.repositories.categories import CategoryRepository
from src.dependencies.database import DBDep


router = APIRouter(
    prefix="/categories",
    tags=["Категории"]
)

@router.get("", summary="Получить список категорий", description="Получить список всех категорий или результат поиска по названию")
async def get_categories(
    db: DBDep
):
    return await db.categories.get_all()
       

@router.get("/{category_id}",  summary="Получить категорию по ID", description="Получить категорию по ее ID")
async def get_category(
        db: DBDep,
        category_id: int = Path(description="ID категории")
):
    return await db.categories.get_one_or_none(id = category_id)


@router.post("", summary="Добавить категорию")
async def create_category(
        db: DBDep,
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
    result = await db.categories.add(category_data)
    await db.commit()
    return {"message": "Category created.", "date": result}

    
@router.delete("/{category_id}",  summary="Удалить категорию", description="Удалить категорию по ее ID")
async def delete_category(
        db: DBDep,
        category_id: int = Path(description="ID категории")
):
    await db.categories.delete(id = category_id)
    await db.commit()
    return {"message": "Category was deleted."}


@router.put("/{category_id}",  summary="Обновить категорию", description="Обновить полностью информацию о существующей категории по ее ID")
async def update_category_put(
        db: DBDep,
        category_id: int = Path(description="ID категории"),
        updated_category: SCategoryCreate = Body(description="Обновленная категория")
):
    await db.categories.update(updated_category, id = category_id)
    await db.commit()
    return {"message": "Category was updated."}
    
