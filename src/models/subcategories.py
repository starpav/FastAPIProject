from src.database import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Subcategory(Base):
    __tablename__ = "subcategories"

    id: Mapped[int] = mapped_column(primary_key=True,  autoincrement=True)
    name:  Mapped[str] = mapped_column(String(100), nullable=False,  unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", name="fk_subcategories_category_id", ondelete="CASCADE"), nullable=False)
