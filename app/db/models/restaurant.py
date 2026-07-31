from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, Integer, Numeric, DateTime, Text, UniqueConstraint
from sqlalchemy import CheckConstraint
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Restaurant(Base):
    __tablename__ = 'restaurants'

    __table_args__ = (
        CheckConstraint(
            'average_check >= 0',
            name='ck_restaurants_average_check_non_negative'
        ),
        CheckConstraint(
            'rating >= 0 AND rating <= 5',
            name="ck_restaurants_rating_range",
        ),
        UniqueConstraint(
            'source',
            'external_id',
            name='uq_restaurants_source_external_id'
        ),
    )

    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite",
        back_populates="restaurant",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str | None] = mapped_column(String(20), nullable=True)
    external_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    city: Mapped[str] = mapped_column(String(75))
    address: Mapped[str] = mapped_column(String(255))
    average_check: Mapped[int | None] = mapped_column(Integer(), nullable=True)
    rating: Mapped[Decimal | None] = mapped_column(Numeric(2, 1), nullable=True)
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )