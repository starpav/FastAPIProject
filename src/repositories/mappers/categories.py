from src.models.categories import Category
from src.schemas.categories import SCategoryRel
from src.repositories.mappers.base import DataMapper


class CategoryDataMapper(DataMapper):
    db_model = Category
    schema = SCategoryRel
