from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, Integer, Numeric, DateTime, Text
from sqlalchemy import CheckConstraint
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

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
    )

    id: Mapped[int] = mapped_column(primary_key=True)
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