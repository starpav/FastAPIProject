from pydantic import BaseModel


class SSubcategoryCreate(BaseModel):
    category_id: int
    name: str

class SSubcategory(SSubcategoryCreate):
    id: int


    