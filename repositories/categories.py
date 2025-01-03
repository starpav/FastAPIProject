from repositories.base import BaseRepository
from src.models.categories import Category

class CategoryRepository(BaseRepository):
    model = Category
    
    