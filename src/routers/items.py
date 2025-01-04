from fastapi import APIRouter, Query, Path, Body
from src.repositories.items import ItemRepository
from src.schemas.items import SItem, SItemCreate, SItemUpdate
from src.dependencies.pagination import PaginationDep
from src.dependencies.database import DBDep



router = APIRouter(
    prefix="/items",
    tags=["Товары"]
)

@router.get("", summary="Получить список товаров", description="Получить список всех товаров или результат поиска по цене/названию")
async def get_items(
        pagination: PaginationDep,
        db: DBDep,
        category_id: int | None = Query(None),
        name: str | None = Query(None),
        description: str | None = Query(None),
        price: float | None = Query(None),
):
    
    return await db.items.get_all(
        category_id=category_id,
        name=name,
        description=description,
        price=price,
        offset=(pagination.page - 1) * pagination.per_page,
        limit=pagination.per_page
        )
        
@router.get("/{item_id}",  summary="Получить товар по ID", description="Получить товар по его ID")
async def get_item(
        db: DBDep,
        item_id: int = Path(description="ID товара")
    ):
    return await db.items.get_one_or_none(id=item_id)
        

@router.post("", summary="Добавить товар")
async def create_item(
        db: DBDep,
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
    result = await db.items.add(item_data)
    await db.commit()
    return {"message": "Item was created.", "id": result}


    

@router.delete("/{item_id}",  summary="Удалить товар", description="Удалить товар по его ID")
async def delete_item(
        db: DBDep,
        item_id: int = Path(description="ID товара")
):
    await db.items.delete(id=item_id)
    await db.commit()
    return {"message": "Item was deleted."}
        


@router.put("/{item_id}",  summary="Обновить товар", description="Обновить полностью информацию о существующем товаре по его ID")
async def update_item_put(
        db: DBDep,
        item_id: int = Path(description="ID товара"),
        updated_item: SItemUpdate = Body(description="Обновленный товар")
):
    await db.items.update(updated_item, id=item_id)
    await db.commit()
    return {"message": "Item was updated."}
        


@router.patch("/{item_id}",  summary="Обновить товар", description="Обновить часть информации о существующем товаре по его ID")
async def update_item_patch(
        db: DBDep,
        item_id: int = Path(description="ID товара"),
        updated_item: SItemUpdate = Body(description="Обновленный товар")
):
    await db.items.update(updated_item, id=item_id, exclude_unset=True)
    await db.commit()
    return {"message": "Item was updated."}
       