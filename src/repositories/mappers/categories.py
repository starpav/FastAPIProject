from src.models.categories import Category
from src.schemas.categories import SCategory, SCategoryRel
from src.repositories.mappers.base import DataMapper


class CategoryDataMapper(DataMapper):
    db_model = Category
    schema = SCategory
    
class CategoryRelDataMapper(DataMapper):
    db_model = Category
    schema = SCategoryRel
