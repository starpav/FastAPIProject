from src.repositories.base import BaseRepository
from src.models.categories import Category
from src.schemas.categories import SCategory

class CategoryRepository(BaseRepository):
    model = Category
    schema = SCategory
    
    