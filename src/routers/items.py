from fastapi import APIRouter, Query, Path, Body
from src.repositories.items import ItemRepository
from src.schemas.items import SItem, SItemCreate, SItemUpdate
from src.dependencies.pagination import PaginationDep
from src.database import async_session_maker



router = APIRouter(
    prefix="/items",
    tags=["Товары"]
)

@router.get("", summary="Получить список товаров", description="Получить список всех товаров или результат поиска по цене/названию")
async def get_items(
        pagination: PaginationDep,
        category_id: int | None = Query(None),
        name: str | None = Query(None),
        description: str | None = Query(None),
        price: float | None = Query(None),
):
    async with async_session_maker() as session:
        try:
            return await ItemRepository(session).get_all(
                category_id=category_id,
                name=name,
                description=description,
                price=price,
                offset=(pagination.page - 1) * pagination.per_page,
                limit=pagination.per_page
                )
        except Exception as e:
            return {"error": f"Items not found: {str(e)}"}

@router.get("/{item_id}",  summary="Получить товар по ID", description="Получить товар по его ID")
async def get_item(
        item_id: int = Path(description="ID товара")
    ):
    async with async_session_maker() as session:
        try:
            return await ItemRepository(session).get_one_or_none(id=item_id)
        except:
            return {"error": "Item not found"}

@router.post("", summary="Добавить товар")
async def create_item(
        item_data: SItemCreate = Body(openapi_examples={
            "1": {
                "summary": "Пример 1",
                "value": {
                    "category_id": 1,
                    "name": "Item 11",
                    "price": 100.00,
                }
            },
            "2": {
                "summary": "Пример 2",
                "value": {
                    "category_id": 1,
                    "name": "Item 12",
                    "price": 100.00,
                }
            },
        })
):
    async with async_session_maker() as session:
        try:
            result = await ItemRepository(session).add(item_data)
            await session.commit()
            return {"message": "Item was created.", "id": result}
        except Exception as e:
            await session.rollback()
            return {"error": f"Item not created: {str(e)}"}

    

@router.delete("/{item_id}",  summary="Удалить товар", description="Удалить товар по его ID")
async def delete_item(
        item_id: int = Path(description="ID товара")
):
    async with async_session_maker() as session:
        try:
            await ItemRepository(session).delete(id=item_id)
            await session.commit()
            return {"message": "Item was deleted."}
        except:
            return {"error": "Item not found"}


@router.put("/{item_id}",  summary="Обновить товар", description="Обновить полностью информацию о существующем товаре по его ID")
async def update_item_put(
        item_id: int = Path(description="ID товара"),
        updated_item: SItemUpdate = Body(description="Обновленный товар")
):
    async with async_session_maker() as session:
        try:
            await ItemRepository(session).update(updated_item, id=item_id)
            await session.commit()
            return {"message": "Item was updated."}
        except:
            return {"error": "Item not found"}


@router.patch("/{item_id}",  summary="Обновить товар", description="Обновить часть информации о существующем товаре по его ID")
async def update_item_patch(
        item_id: int = Path(description="ID товара"),
        updated_item: SItemUpdate = Body(description="Обновленный товар")
):
    async with async_session_maker() as session:
        try:
            await ItemRepository(session).update(updated_item, id=item_id, exclude_unset=True)
            await session.commit()
            return {"message": "Item was updated."}
        except:
            return {"error": "Item not found"}
