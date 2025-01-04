from pydantic import BaseModel, Field
from decimal import Decimal

class SItemCreate(BaseModel):
    category_id: int
    name: str
    description: str | None = Field(None)
    price: Decimal = Field(max_digits=10, decimal_places=2)

class SItem(SItemCreate):
    id: int
    
class SItemUpdate(BaseModel):
    name: str | None = Field(None)
    description: str | None = Field(None)
    price: Decimal | None = Field(None, max_digits=10, decimal_places=2)