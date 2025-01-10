import json
from pathlib import Path
import pytest

from src.schemas.items import SItemCreate
from src.database import Base, engine_null_pool
from src.models import *
from src.config import settings

from src.schemas.categories import SCategoryCreate
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool




@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"
    
    
@pytest.fixture(scope="function")
async def db() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db
    

@pytest.fixture(scope="session", autouse=True)
async def setup_data_base(check_test_mode):    
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        print("Base dropped")
        await conn.run_sync(Base.metadata.create_all)
        print("Base created")


@pytest.fixture(scope="session", autouse=True)
async def add_test_categories(setup_data_base):
    """
    Фикстура для добавления тестовых категорий из JSON-файла.
    """
    # Путь к файлу с категориями
    base_path = Path(__file__).parent
    categories_file = base_path / "mock_categories.json"

    # Загрузка данных из файла
    with open(categories_file, "r", encoding="utf-8") as f:
        categories_data = json.load(f)

    # Создание сессии
    async with DBManager(session_factory=async_session_maker_null_pool) as _db:
        # Добавление категорий
        for category in categories_data:
            category_data = SCategoryCreate(**category)
            await _db.categories.add(category_data)
            await _db.commit()  # Сохранение для генерации `id` в категориях


@pytest.fixture(scope="session", autouse=True)
async def add_test_items(add_test_categories):
    """
    Фикстура для добавления тестовых товаров из JSON-файла.
    """
    # Путь к файлу с товарами
    base_path = Path(__file__).parent
    items_file = base_path / "mock_items.json"

    # Загрузка данных из файла
    with open(items_file, "r", encoding="utf-8") as f:
        items_data = json.load(f)

    # Создание сессии
    async with DBManager(session_factory=async_session_maker_null_pool) as _db:
        # Добавление товаров
        for item in items_data:
            item_data = SItemCreate(**item)
            await _db.items.add(item_data)
            await _db.commit()  # Подтверждение транзакции

 