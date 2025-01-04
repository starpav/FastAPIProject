from src.models.subcategories import Subcategory
from src.database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True,  autoincrement=True)
    name:  Mapped[str] = mapped_column(String(100), nullable=False,  unique=True)

    subcategories: Mapped[list[Subcategory]] = relationship(back_populates="category", cascade='all, delete', passive_deletes=True)

    