from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric, ForeignKey
from decimal import Decimal


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True,  autoincrement=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", name="fk_items_category_id"), nullable=False)
    # subcategory_id: Mapped[int] = mapped_column(ForeignKey("subcategories.id", name="fk_items_subcategory_id"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
