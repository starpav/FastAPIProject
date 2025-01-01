import uvicorn
from fastapi import FastAPI, Query, Path, Body

app = FastAPI()

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

@app.get("/items")
def get_items():
    return items

@app.get("/items/search")
def search_items(
        name: str | None = Query(default=None, description="Название товара")
):
    if not name:
        return items
    return [item for item in items if name.lower() in item["name"].lower()]

@app.get("/items/{item_id}")
def get_item(
        item_id: int = Path(description="ID товара")
):
    for item in items:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}

@app.post("/items")
def create_item(
        name: str = Body(embed=True),
        price:  float = Body(embed=True)
):
    new_item = {"id": len(items) + 1, "name": name,  "price": price}
    items.append(new_item)
    return {"message": "Item created", "item": new_item}

@app.delete("/items/{item_id}")
def delete_item(
        item_id: int = Path(description="ID товара")
):
    for item in items:
        if item["id"] == item_id:
            items.remove(item)
            return {"message": "Item deleted"}
    return {"error": "Item not found"}

@app.put("/items/{item_id}")
def update_item_put(
        item_id: int = Path(description="ID товара"),
        name: str = Body(embed=True),
        price: float = Body(embed=True)
):
    for i, item in enumerate(items):
        if item["id"] == item_id:
            # Полностью обновляем элемент
            items[i] = {"id": item_id, "name": name, "price": price}
            return {"message": "Item updated"}
    return {"error": "Item not found"}

@app.patch("/items/{item_id}")
def update_item_patch(
        item_id: int = Path(description="ID товара"),
        name: str | None = Body(embed=True, default=None),
        price: float | None = Body(embed=True, default=None)
):
    for i, item in enumerate(items):
        if item["id"] == item_id:
            # Обновляем только указанные поля
            if name is not None:
                items[i]["name"] = name
            if price is not None:
                items[i]["price"] = price
            return {"message": "Item updated"}
    return {"error": "Item not found"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)