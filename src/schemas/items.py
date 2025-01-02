from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str
    price: float

class ItemUpdate(BaseModel):
    name: str | None = Field(None)
    price: float | None = Field(None)