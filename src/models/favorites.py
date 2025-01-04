from src.database import Base
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class Favorite(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True,  autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", name="fk_favorites_user_id", ondelete="CASCADE"), nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", name="fk_favorites_item_id", ondelete="CASCADE"), nullable=False)
    
    __table_args__ = (
        UniqueConstraint("user_id", "item_id", name="uc_favorites_user_id_item_id"),
    )
    