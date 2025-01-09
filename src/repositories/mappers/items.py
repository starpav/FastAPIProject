from src.models.items import Item
from src.schemas.items import SItem
from src.repositories.mappers.base import DataMapper


class ItemDataMapper(DataMapper):
    db_model = Item
    schema = SItem
