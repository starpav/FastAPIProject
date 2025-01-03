"""del subcategories

Revision ID: 0ead459cdb44
Revises: 5ea0cc83c04a
Create Date: 2025-01-03 12:18:32.254493

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0ead459cdb44"
down_revision: Union[str, None] = "5ea0cc83c04a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Удаляем внешний ключ и колонку subcategory_id
    op.drop_constraint(
        "items_subcategory_id_fkey", "items", type_="foreignkey"
    )
    op.drop_column("items", "subcategory_id")

    # Удаляем таблицу subcategories
    op.drop_table("subcategories")


def downgrade() -> None:
    # Восстанавливаем таблицу subcategories
    op.create_table(
        "subcategories",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(length=100), nullable=False),
        sa.Column("category_id", sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
            name="subcategories_category_id_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="subcategories_pkey"),
        sa.UniqueConstraint("name", name="subcategories_name_key"),
    )

    # Восстанавливаем колонку subcategory_id в таблице items
    op.add_column(
        "items",
        sa.Column(
            "subcategory_id",
            sa.INTEGER(),
            autoincrement=False,
            nullable=True,  # Сначала делаем колонку nullable
        ),
    )

    # Добавляем внешний ключ к subcategories
    op.create_foreign_key(
        "items_subcategory_id_fkey",
        "items",
        "subcategories",
        ["subcategory_id"],
        ["id"],
    )

    # После добавления данных в subcategory_id можно сделать ее NOT NULL,
    # если требуется, с помощью отдельной миграции или команды.
