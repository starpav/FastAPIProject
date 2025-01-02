from fastapi import APIRouter, Query, Path, Body
from src.schemas.items import Item, ItemUpdate
from src.dependencies.pagination import PaginationDep

items = [
    {"id": 1, "name": "Item 1", "price": 100.00},
    {"id": 2, "name": "Item 2", "price": 100.00},
    {"id": 3, "name": "Item 3", "price": 100.00},
    {"id": 4, "name": "Item 4", "price": 100.00},
    {"id": 5, "name": "Item 5", "price": 100.00},
    {"id": 6, "name": "Item 6", "price": 100.00},
    {"id": 7, "name": "Item 7", "price": 100.00},
    {"id": 8, "name": "Item 8", "price": 100.00},
    {"id": 9, "name": "Item 9", "price": 100.00},
    {"id": 10, "name": "Item 10", "price": 100.00}
]

router = APIRouter(
    prefix="/items",
    tags=["Товары"]
)

@router.get("", summary="Получить список товаров", description="Получить список всех товаров или результат поиска по цене/названию")
def get_items(
        pagination: PaginationDep,
        name: str | None = Query(default=None, description="Название товара"),
        price: float | None = Query(default=None, description="Цена товара"),
):
    # Фильтрация
    filtered_items = items
    if name:
        filtered_items = [item for item in filtered_items if name.lower() in item["name"].lower()]
    if price:
        filtered_items = [item for item in filtered_items if item["price"] == price]


    total = len(filtered_items)
    start = (pagination.page - 1) * pagination.per_page
    end = start + pagination.per_page
    if start >= total:
        return {"error": "Page not found"}
    items_page = items[start:end]
    return items_page

@router.get("/{item_id}",  summary="Получить товар по ID", description="Получить товар по его ID")
def get_item(
        item_id: int = Path(description="ID товара")
    ):
    for item in items:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}

@router.post("", summary="Добавить товар")
def create_item(
        item_data: Item = Body(openapi_examples={
            "1": {
                "summary": "Пример 1",
                "value": {
                    "name": "Item 11",
                    "price": 100.00,
                }
            },
            "2": {
                "summary": "Пример 2",
                "value": {
                    "name": "Item 12",
                    "price": 100.00,
                }
            },
        })
):
    new_item = {"id": items[-1]["id"] + 1, "name": item_data.name,  "price": item_data.price}
    items.append(new_item)
    return {"message": "Item created", "item": new_item}

@router.delete("/{item_id}",  summary="Удалить товар", description="Удалить товар по его ID")
def delete_item(
        item_id: int = Path(description="ID товара")
):
    for item in items:
        if item["id"] == item_id:
            items.remove(item)
            return {"message": "Item deleted"}
    return {"error": "Item not found"}

@router.put("/{item_id}",  summary="Обновить товар", description="Обновить полностью информацию о существующем товаре по его ID")
def update_item_put(
        item_id: int = Path(description="ID товара"),
            updated_item: Item = Body(description="Обновленный товар")
):
    for i, item in enumerate(items):
        if item["id"] == item_id:
            # Полностью обновляем элемент
            items[i] = {"id": item_id, "name": updated_item.name, "price": updated_item.price}
            return {"message": "Item updated"}
    return {"error": "Item not found"}

@router.patch("/{item_id}",  summary="Обновить товар", description="Обновить часть информации о существующем товаре по его ID")
def update_item_patch(
        item_id: int = Path(description="ID товара"),
        updated_item: ItemUpdate = Body(description="Обновленный товар")
):
    for i, item in enumerate(items):
        if item["id"] == item_id:
            # Обновляем только указанные поля
            if updated_item.name:
                items[i]["name"] = updated_item.name
            if updated_item.price:
                items[i]["price"] = updated_item.price
            return {"message": "Item updated"}
    return {"error": "Item not found"}