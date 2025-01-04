from pydantic import BaseModel

from src.schemas.subcategories import SSubcategory


class SCategoryCreate(BaseModel):
    name: str

class SCategory(SCategoryCreate):
    id: int

class SCategoryRel(SCategory):
    subcategories: list["SSubcategory"]
    