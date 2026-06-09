from datetime import datetime

from sqlalchemy import DateTime, UniqueConstraint, ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Favorite(Base):
    __tablename__ = 'favorites'

    __table_args__ = (
        UniqueConstraint(
            'user_id', 'restaurant_id',
            name='uq_favorites_user_id_restaurant_id'),
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="favorites",
    )

    restaurant: Mapped["Restaurant"] = relationship(
        "Restaurant",
        back_populates="favorites",
    )

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )
    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey('restaurants.id', ondelete='CASCADE'),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )