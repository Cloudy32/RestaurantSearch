from sqlalchemy import String,Integer,Float

from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Restaurant(Base):
    __tablename__ = 'restaurant'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(15))
    description: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(15))
    address: Mapped[str] = mapped_column(String(70))
    average_check: Mapped[int | None] = mapped_column(Integer())