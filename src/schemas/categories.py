from pydantic import BaseModel


class SCategoryCreate(BaseModel):
    name: str

class SCategory(SCategoryCreate):
    id: int
