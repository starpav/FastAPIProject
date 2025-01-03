from pydantic import BaseModel, Field

class SCategory(BaseModel):
    id: int
    name: str
    
    model_config = {
        "from_attributes": True
    }

class SCategoryCreate(BaseModel):
    name: str
